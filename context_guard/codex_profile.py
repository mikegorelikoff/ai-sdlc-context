"""Lease-safe, explicit Codex skill profile generation and restoration."""

from __future__ import annotations

import base64
import hashlib
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

try:  # pragma: no cover - selected by the interpreter version
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    import tomli as tomllib

from context_guard import inventory, receipts
from context_guard.claude_profile import (
    ClaudeProfileError,
    _create_exclusive_json,
    _digest,
    _ensure_profile_root,
    _fsync_dir,
    _pid_alive,
    _read_json,
    _write_bytes_atomic,
    _write_json_atomic,
)


STATE_SCHEMA = "context-guard-codex-profile/v1"
PROFILE_RELATIVE = Path(".context-guard") / "profiles" / "codex"
_PROFILE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z")
_RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_CLASSIFICATIONS = {"safety-critical", "required", "irrelevant", "uncertain"}


class CodexProfileError(ValueError):
    """Invalid or unsafe Codex profile operation."""


@dataclass(frozen=True)
class CodexProfileResult:
    status: str
    reason_code: str
    run_id: str
    profile: str
    disabled_count: int
    fresh_process_required: bool = False
    recovery_action: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def plan_disabled_paths(
    classifications: Mapping[str, str],
    skill_paths: Mapping[str, str | Path],
    *,
    explicit_invocations: Iterable[str] = (),
) -> tuple[Path, ...]:
    """Return sorted exact paths for irrelevant, non-explicit skills."""
    explicit = set(explicit_invocations)
    if set(classifications) != set(skill_paths):
        raise CodexProfileError("classifications and skill paths must name the same skills")
    result = []
    for name, classification in sorted(classifications.items()):
        if not isinstance(name, str) or not name:
            raise CodexProfileError("skill names must be non-empty strings")
        if classification not in _CLASSIFICATIONS:
            raise CodexProfileError(f"invalid classification for {name}")
        path = Path(skill_paths[name]).expanduser()
        if not path.is_absolute() or path.name != "SKILL.md":
            raise CodexProfileError(f"skill path for {name} must be an absolute SKILL.md path")
        if classification == "irrelevant" and name not in explicit:
            result.append(path.resolve(strict=False))
    if len(set(result)) != len(result):
        raise CodexProfileError("duplicate skill path")
    return tuple(sorted(result, key=str))


def apply_profile(
    repo_root: Path,
    home: Path,
    *,
    profile: str,
    run_id: str,
    version: str,
    surface: str,
    classifications: Mapping[str, str],
    skill_paths: Mapping[str, str | Path],
    explicit_invocations: Iterable[str] = (),
    inventory_fingerprint: str | None = None,
    bypass: bool = False,
    pid: int | None = None,
    verify_hook: Callable[[Path], None] | None = None,
) -> CodexProfileResult:
    """Create and verify a dedicated explicit Codex profile."""
    _validate_run_id(run_id)
    profile_path = _profile_path(home, profile)
    eligibility = inventory.preflight("codex", version, surface)
    if bypass:
        return _result(repo_root, run_id, version, surface, profile, "full-load", "bypass", 0)
    if eligibility.status != "supported":
        return _result(
            repo_root, run_id, version, surface, profile, "full-load",
            eligibility.reason_code, 0
        )
    if not inventory_fingerprint:
        return _result(
            repo_root, run_id, version, surface, profile, "full-load",
            "missing-inventory-fingerprint", 0
        )
    current_inventory = inventory.read_inventory(
        Path(home), provider="codex", version=version, surface=surface
    )
    if current_inventory.status != "supported":
        return _result(
            repo_root, run_id, version, surface, profile, "full-load",
            current_inventory.reason_code, 0
        )
    if current_inventory.fingerprint != inventory_fingerprint:
        return _result(
            repo_root, run_id, version, surface, profile, "full-load",
            "inventory-fingerprint-mismatch", 0
        )
    expected_paths = {
        record.name: Path(record.locator) for record in current_inventory.records
    }
    supplied_paths = {
        name: Path(path).expanduser().resolve(strict=False)
        for name, path in skill_paths.items()
    }
    if set(classifications) != set(expected_paths) or supplied_paths != expected_paths:
        return _result(
            repo_root, run_id, version, surface, profile, "full-load",
            "inventory-correlation-mismatch", 0,
            inventory_fingerprint=inventory_fingerprint
        )
    planned = plan_disabled_paths(
        classifications, supplied_paths, explicit_invocations=explicit_invocations
    )
    if not planned:
        return _result(
            repo_root, run_id, version, surface, profile, "full-load",
            "no-eligible-skills", 0, inventory_fingerprint=inventory_fingerprint
        )

    paths = _state_paths(repo_root, profile_path)
    try:
        _ensure_profile_root(repo_root, paths["root"])
    except (OSError, ClaudeProfileError) as exc:
        raise CodexProfileError("unsafe private profile storage") from exc
    if paths["disabled"].exists():
        return _result(
            repo_root, run_id, version, surface, profile, "full-load",
            "profile-disabled", 0, inventory_fingerprint=inventory_fingerprint,
            recovery_action="inspect the preserved profile and run codex-profile recover"
        )
    owner_pid = pid if pid is not None else os.getpid()
    lease = {"schema": STATE_SCHEMA, "run_id": run_id, "pid": owner_pid}
    if not _create_exclusive_json(paths["lease"], lease):
        alive = _pid_alive(_read_json(paths["lease"]).get("pid"))
        return _result(
            repo_root, run_id, version, surface, profile, "full-load",
            "lease-contention" if alive else "abandoned-lease", 0,
            inventory_fingerprint=inventory_fingerprint,
            recovery_action=None if alive else "run codex-profile recover"
        )

    try:
        baseline_exists = profile_path.is_file()
        baseline = profile_path.read_bytes() if baseline_exists else b""
        if baseline_exists:
            _parse_toml(baseline)
        generated = _render_profile(planned)
        state = {
            "schema": STATE_SCHEMA,
            "owner_run_id": run_id,
            "owner_pid": owner_pid,
            "profile_path": str(profile_path),
            "baseline_exists": baseline_exists,
            "baseline_digest": _digest(baseline),
            "baseline_bytes": base64.b64encode(baseline).decode("ascii"),
            "applied_digest": _digest(generated),
        }
        _write_json_atomic(paths["state"], state)
        _write_bytes_atomic(profile_path, generated, private_parent=True)
        if verify_hook is not None:
            verify_hook(profile_path)
        actual = profile_path.read_bytes()
        parsed = _parse_toml(actual)
        if actual != generated or _disabled_paths(parsed) != tuple(str(path) for path in planned):
            raise CodexProfileError("actual-state-mismatch")
        try:
            return _result(
                repo_root, run_id, version, surface, profile, "reduced",
                "verified-profile", len(planned),
                inventory_fingerprint=inventory_fingerprint,
                fresh_process_required=True
            )
        except receipts.ReceiptError:
            _rollback(profile_path, paths)
            raise
    except (OSError, UnicodeDecodeError, ValueError, CodexProfileError) as exc:
        reason = str(exc) or "profile-apply-failed"
        _rollback(profile_path, paths)
        return _result(
            repo_root, run_id, version, surface, profile, "full-load", reason, 0,
            inventory_fingerprint=inventory_fingerprint
        )


def restore_profile(
    repo_root: Path,
    home: Path,
    *,
    profile: str,
    run_id: str,
    version: str,
    surface: str = "cli",
) -> CodexProfileResult:
    _validate_run_id(run_id)
    path = _profile_path(home, profile)
    return _restore(repo_root, path, profile, run_id, version, surface, require_dead=False)


def recover_profile(
    repo_root: Path,
    home: Path,
    *,
    profile: str,
    run_id: str,
    version: str,
    surface: str = "cli",
    liveness: Callable[[int], bool] | None = None,
) -> CodexProfileResult:
    _validate_run_id(run_id)
    path = _profile_path(home, profile)
    paths = _state_paths(repo_root, path)
    if not paths["lease"].is_file():
        return _result(
            repo_root, run_id, version, surface, profile, "restored",
            "already-restored", 0, restoration_status="already-restored"
        )
    owner = _read_json(paths["lease"]).get("pid")
    if isinstance(owner, int) and (liveness or _pid_alive)(owner):
        return _result(
            repo_root, run_id, version, surface, profile, "full-load",
            "lease-owner-alive", 0, restoration_status="not-restored"
        )
    return _restore(repo_root, path, profile, run_id, version, surface, require_dead=True)


def profile_status(repo_root: Path, home: Path, profile: str) -> dict[str, object]:
    path = _profile_path(home, profile)
    paths = _state_paths(repo_root, path)
    lease = _read_json(paths["lease"]) if paths["lease"].is_file() else {}
    return {
        "profile": profile,
        "selector": ["--profile", profile],
        "leased": paths["lease"].is_file(),
        "owner_alive": _pid_alive(lease.get("pid")) if lease else None,
        "state_present": paths["state"].is_file(),
        "disabled": paths["disabled"].is_file(),
    }


def _restore(
    repo_root: Path,
    path: Path,
    profile: str,
    run_id: str,
    version: str,
    surface: str,
    *,
    require_dead: bool,
) -> CodexProfileResult:
    paths = _state_paths(repo_root, path)
    if not paths["state"].is_file():
        if not paths["lease"].exists():
            return _result(
                repo_root, run_id, version, surface, profile, "restored",
                "already-restored", 0, restoration_status="already-restored"
            )
        return _disable(repo_root, paths, run_id, version, surface, profile, "missing-profile-state")
    state = _read_json(paths["state"])
    if state.get("schema") != STATE_SCHEMA or state.get("profile_path") != str(path):
        return _disable(repo_root, paths, run_id, version, surface, profile, "invalid-profile-state")
    if require_dead and _pid_alive(state.get("owner_pid")):
        return _result(
            repo_root, run_id, version, surface, profile, "full-load",
            "lease-owner-alive", 0, restoration_status="not-restored"
        )
    current = path.read_bytes() if path.is_file() else b""
    if _digest(current) != state.get("applied_digest"):
        return _disable(repo_root, paths, run_id, version, surface, profile, "user-edit-detected")
    try:
        baseline = base64.b64decode(state["baseline_bytes"], validate=True)
        if _digest(baseline) != state.get("baseline_digest"):
            raise CodexProfileError("baseline-digest-mismatch")
        if state.get("baseline_exists"):
            _write_bytes_atomic(path, baseline, private_parent=True)
        elif path.exists():
            path.unlink()
            _fsync_dir(path.parent)
        for key in ("state", "lease", "disabled"):
            paths[key].unlink(missing_ok=True)
        _fsync_dir(paths["root"])
    except (OSError, ValueError, KeyError, CodexProfileError):
        return _disable(repo_root, paths, run_id, version, surface, profile, "restore-failed")
    return _result(
        repo_root, run_id, version, surface, profile, "restored",
        "baseline-restored", 0, restoration_status="restored"
    )


def _rollback(path: Path, paths: Mapping[str, Path]) -> None:
    state = _read_json(paths["state"]) if paths["state"].is_file() else {}
    current = path.read_bytes() if path.is_file() else b""
    if state and _digest(current) in {
        state.get("applied_digest"), state.get("baseline_digest")
    }:
        baseline = base64.b64decode(state.get("baseline_bytes", ""))
        if state.get("baseline_exists"):
            _write_bytes_atomic(path, baseline, private_parent=True)
        elif path.exists():
            path.unlink()
        paths["state"].unlink(missing_ok=True)
        paths["lease"].unlink(missing_ok=True)
    elif state:
        _write_json_atomic(
            paths["disabled"], {"schema": STATE_SCHEMA, "reason_code": "rollback-cas-mismatch"}
        )
    else:
        paths["lease"].unlink(missing_ok=True)


def _disable(
    repo_root: Path,
    paths: Mapping[str, Path],
    run_id: str,
    version: str,
    surface: str,
    profile: str,
    reason: str,
) -> CodexProfileResult:
    _write_json_atomic(paths["disabled"], {"schema": STATE_SCHEMA, "reason_code": reason})
    return _result(
        repo_root, run_id, version, surface, profile, "full-load", reason, 0,
        restoration_status="recovery-required",
        recovery_action="inspect the preserved profile and state before manual recovery"
    )


def _result(
    repo_root: Path,
    run_id: str,
    version: str,
    surface: str,
    profile: str,
    status: str,
    reason: str,
    count: int,
    *,
    inventory_fingerprint: str | None = None,
    fresh_process_required: bool = False,
    restoration_status: str | None = None,
    recovery_action: str | None = None,
) -> CodexProfileResult:
    payload: dict[str, Any] = {
        "schema": receipts.SCHEMA,
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": "codex",
        "provider_version": version,
        "surface": surface,
        "status": status,
        "completed": True,
        "referenced": False,
        "reason_codes": [reason],
        "classifications": ["irrelevant"] if count else ["none"],
        "requested_action": "disable-irrelevant-skills" if count else "full-load",
        "actual_action": status,
    }
    if inventory_fingerprint:
        payload["inventory_fingerprint"] = inventory_fingerprint
    if restoration_status:
        payload["restoration_status"] = restoration_status
    receipts.write_receipt(repo_root, payload)
    return CodexProfileResult(
        status, reason, run_id, profile, count, fresh_process_required, recovery_action
    )


def _profile_path(home: Path, profile: str) -> Path:
    if not isinstance(profile, str) or not _PROFILE_NAME.fullmatch(profile):
        raise CodexProfileError("profile name is invalid")
    home_path = Path(home).expanduser().resolve(strict=False)
    return home_path / ".codex" / f"{profile}.config.toml"


def _validate_run_id(run_id: str) -> None:
    if not isinstance(run_id, str) or not _RUN_ID.fullmatch(run_id):
        raise CodexProfileError("run_id is invalid")


def _state_paths(repo_root: Path, profile_path: Path) -> dict[str, Path]:
    key = hashlib.sha256(str(profile_path).encode("utf-8")).hexdigest()[:24]
    root = Path(repo_root) / PROFILE_RELATIVE / key
    return {
        "root": root,
        "lease": root / "lease.json",
        "state": root / "state.json",
        "disabled": root / "disabled.json",
    }


def _render_profile(paths: tuple[Path, ...]) -> bytes:
    chunks = []
    for path in paths:
        escaped = str(path).replace("\\", "\\\\").replace('"', '\\"')
        chunks.append(f'[[skills.config]]\npath = "{escaped}"\nenabled = false\n')
    return ("\n".join(chunks)).encode("utf-8")


def _parse_toml(raw: bytes) -> dict[str, Any]:
    value = tomllib.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise CodexProfileError("profile must be a TOML table")
    return value


def _disabled_paths(value: Mapping[str, Any]) -> tuple[str, ...]:
    skills = value.get("skills")
    if not isinstance(skills, dict) or not isinstance(skills.get("config"), list):
        raise CodexProfileError("skills.config must be an array of tables")
    result = []
    for item in skills["config"]:
        if (
            not isinstance(item, dict)
            or set(item) != {"path", "enabled"}
            or not isinstance(item.get("path"), str)
            or item.get("enabled") is not False
        ):
            raise CodexProfileError("profile contains an invalid skills.config entry")
        result.append(item["path"])
    return tuple(result)
