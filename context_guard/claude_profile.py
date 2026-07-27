"""Lease-safe Claude Code guarded profile application and restoration."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

from context_guard import inventory, receipts


STATE_SCHEMA = "context-guard-claude-profile/v1"
PROFILE_RELATIVE = Path(".context-guard") / "profiles" / "claude"
USER_INVOKABLE_ONLY = "user-invocable-only"


@dataclass(frozen=True)
class ClaudeProfileResult:
    status: str
    reason_code: str
    run_id: str
    requested_overrides: dict[str, str]
    fresh_session_required: bool = False
    recovery_action: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class ClaudeProfileError(ValueError):
    """Invalid or unsafe Claude profile operation."""


def plan_overrides(
    classifications: Mapping[str, str],
    *,
    explicit_invocations: Iterable[str] = (),
) -> dict[str, str]:
    """Map only exact irrelevant, non-explicit skills to Claude's safe override."""
    explicit = set(explicit_invocations)
    planned: dict[str, str] = {}
    for name, classification in sorted(classifications.items()):
        if not isinstance(name, str) or not name:
            raise ClaudeProfileError("skill names must be non-empty strings")
        if classification not in {"safety-critical", "required", "irrelevant", "uncertain"}:
            raise ClaudeProfileError(f"invalid classification for {name}")
        if classification == "irrelevant" and name not in explicit:
            planned[name] = USER_INVOKABLE_ONLY
    return planned


def apply_profile(
    repo_root: Path,
    settings_path: Path,
    *,
    run_id: str,
    version: str,
    surface: str,
    classifications: Mapping[str, str],
    explicit_invocations: Iterable[str] = (),
    inventory_fingerprint: str | None = None,
    bypass: bool = False,
    pid: int | None = None,
    verify_hook: Callable[[Path], None] | None = None,
) -> ClaudeProfileResult:
    """Apply and verify a bounded Claude skillOverrides profile."""
    planned = plan_overrides(classifications, explicit_invocations=explicit_invocations)
    eligibility = inventory.preflight("claude", version, surface)
    if bypass:
        return _result_with_receipt(
            repo_root, run_id, version, surface, "full-load", "bypass", planned,
            inventory_fingerprint=inventory_fingerprint,
        )
    if eligibility.status != "supported":
        return _result_with_receipt(
            repo_root, run_id, version, surface, "full-load", eligibility.reason_code, planned,
            inventory_fingerprint=inventory_fingerprint,
        )
    if not inventory_fingerprint:
        return _result_with_receipt(
            repo_root,
            run_id,
            version,
            surface,
            "full-load",
            "missing-inventory-fingerprint",
            planned,
        )
    if not planned:
        return _result_with_receipt(
            repo_root, run_id, version, surface, "full-load", "no-eligible-skills", planned,
            inventory_fingerprint=inventory_fingerprint,
        )

    resolved = settings_path.expanduser().resolve(strict=False)
    paths = _profile_paths(repo_root, resolved)
    _ensure_profile_root(repo_root, paths["root"])
    if paths["disabled"].exists():
        return _result_with_receipt(
            repo_root, run_id, version, surface, "full-load", "profile-disabled", planned,
            inventory_fingerprint=inventory_fingerprint,
            recovery_action="inspect the preserved settings and run claude-profile recover",
        )

    owner_pid = pid if pid is not None else os.getpid()
    lease = {
        "schema": STATE_SCHEMA,
        "run_id": run_id,
        "pid": owner_pid,
        "settings_key": _settings_key(resolved),
    }
    if not _create_exclusive_json(paths["lease"], lease):
        reason = "lease-contention" if _lease_owner_alive(paths["lease"]) else "abandoned-lease"
        action = None if reason == "lease-contention" else "run claude-profile recover"
        return _result_with_receipt(
            repo_root, run_id, version, surface, "full-load", reason, planned,
            inventory_fingerprint=inventory_fingerprint,
            recovery_action=action,
        )

    try:
        baseline_exists = resolved.is_file()
        baseline = resolved.read_bytes() if baseline_exists else b""
        settings = _decode_settings(baseline) if baseline_exists else {}
        current_overrides = settings.get("skillOverrides", {})
        if not isinstance(current_overrides, dict):
            raise ClaudeProfileError("skillOverrides must be an object")
        conflicts = sorted(name for name in planned if name in current_overrides)
        if conflicts:
            raise ClaudeProfileError("baseline-override-conflict")

        state = {
            "schema": STATE_SCHEMA,
            "owner_run_id": run_id,
            "owner_pid": owner_pid,
            "settings_path": str(resolved),
            "baseline_exists": baseline_exists,
            "baseline_digest": _digest(baseline),
            "baseline_bytes": base64.b64encode(baseline).decode("ascii"),
            "applied_digest": None,
        }
        _write_json_atomic(paths["state"], state)

        updated = dict(settings)
        updated_overrides = dict(current_overrides)
        updated_overrides.update(planned)
        updated["skillOverrides"] = updated_overrides
        applied = (json.dumps(updated, indent=2, sort_keys=True) + "\n").encode("utf-8")
        _write_bytes_atomic(resolved, applied, private_parent=False)
        state["applied_digest"] = _digest(applied)
        _write_json_atomic(paths["state"], state)
        if verify_hook is not None:
            verify_hook(resolved)
        actual = resolved.read_bytes()
        actual_settings = _decode_settings(actual)
        actual_overrides = actual_settings.get("skillOverrides", {})
        if any(actual_overrides.get(name) != value for name, value in planned.items()):
            raise ClaudeProfileError("actual-state-mismatch")

        state["applied_digest"] = _digest(actual)
        _write_json_atomic(paths["state"], state)
        try:
            return _result_with_receipt(
                repo_root, run_id, version, surface, "reduced", "verified-profile", planned,
                inventory_fingerprint=inventory_fingerprint,
                fresh_session_required=True,
            )
        except receipts.ReceiptError:
            _rollback_failed_apply(resolved, paths)
            raise
    except (OSError, json.JSONDecodeError, ClaudeProfileError) as exc:
        reason = str(exc) or "profile-apply-failed"
        _rollback_failed_apply(resolved, paths)
        return _result_with_receipt(
            repo_root, run_id, version, surface, "full-load", reason, planned,
            inventory_fingerprint=inventory_fingerprint,
        )


def restore_profile(
    repo_root: Path,
    settings_path: Path,
    *,
    run_id: str,
    version: str,
    surface: str = "cli",
) -> ClaudeProfileResult:
    """Restore an unchanged applied profile using compare-and-swap."""
    resolved = settings_path.expanduser().resolve(strict=False)
    paths = _profile_paths(repo_root, resolved)
    return _restore(repo_root, resolved, paths, run_id, version, surface, require_dead_owner=False)


def recover_profile(
    repo_root: Path,
    settings_path: Path,
    *,
    run_id: str,
    version: str,
    surface: str = "cli",
    liveness: Callable[[int], bool] | None = None,
) -> ClaudeProfileResult:
    """Recover an abandoned lease without overwriting live or edited state."""
    resolved = settings_path.expanduser().resolve(strict=False)
    paths = _profile_paths(repo_root, resolved)
    if not paths["lease"].is_file():
        return _result_with_receipt(
            repo_root, run_id, version, surface, "restored", "already-restored", {},
            restoration_status="already-restored",
        )
    lease = _read_json(paths["lease"])
    owner_pid = lease.get("pid")
    alive = (liveness or _pid_alive)(owner_pid) if isinstance(owner_pid, int) else True
    if alive:
        return _result_with_receipt(
            repo_root, run_id, version, surface, "full-load", "lease-owner-alive", {},
            restoration_status="not-restored",
        )
    return _restore(repo_root, resolved, paths, run_id, version, surface, require_dead_owner=True)


def profile_status(repo_root: Path, settings_path: Path) -> dict[str, object]:
    """Return minimized profile coordination state without baseline content."""
    resolved = settings_path.expanduser().resolve(strict=False)
    paths = _profile_paths(repo_root, resolved)
    lease = _read_json(paths["lease"]) if paths["lease"].is_file() else {}
    return {
        "settings_key": _settings_key(resolved),
        "leased": paths["lease"].is_file(),
        "owner_alive": _pid_alive(lease.get("pid")) if isinstance(lease.get("pid"), int) else None,
        "state_present": paths["state"].is_file(),
        "disabled": paths["disabled"].is_file(),
    }


def _restore(
    repo_root: Path,
    resolved: Path,
    paths: dict[str, Path],
    run_id: str,
    version: str,
    surface: str,
    *,
    require_dead_owner: bool,
) -> ClaudeProfileResult:
    if not paths["state"].is_file():
        if not paths["lease"].exists():
            return _result_with_receipt(
                repo_root, run_id, version, surface, "restored", "already-restored", {},
                restoration_status="already-restored",
            )
        return _disable_and_receipt(
            repo_root, paths, run_id, version, surface, "missing-profile-state"
        )
    state = _read_json(paths["state"])
    if state.get("schema") != STATE_SCHEMA or state.get("settings_path") != str(resolved):
        return _disable_and_receipt(
            repo_root, paths, run_id, version, surface, "invalid-profile-state"
        )
    if require_dead_owner and _pid_alive(state.get("owner_pid")):
        return _result_with_receipt(
            repo_root, run_id, version, surface, "full-load", "lease-owner-alive", {},
            restoration_status="not-restored",
        )

    current_exists = resolved.is_file()
    current = resolved.read_bytes() if current_exists else b""
    applied_digest = state.get("applied_digest")
    baseline_digest = state.get("baseline_digest")
    safe_digest = applied_digest if isinstance(applied_digest, str) else baseline_digest
    if not isinstance(safe_digest, str) or _digest(current) != safe_digest:
        return _disable_and_receipt(
            repo_root, paths, run_id, version, surface, "user-edit-detected"
        )
    try:
        baseline = base64.b64decode(state["baseline_bytes"], validate=True)
        if _digest(baseline) != baseline_digest:
            raise ClaudeProfileError("baseline-digest-mismatch")
        if state.get("baseline_exists"):
            _write_bytes_atomic(resolved, baseline, private_parent=False)
        elif resolved.exists():
            resolved.unlink()
            _fsync_dir(resolved.parent)
        paths["state"].unlink(missing_ok=True)
        paths["lease"].unlink(missing_ok=True)
        paths["disabled"].unlink(missing_ok=True)
        _fsync_dir(paths["root"])
    except (OSError, ValueError, KeyError, ClaudeProfileError):
        return _disable_and_receipt(
            repo_root, paths, run_id, version, surface, "restore-failed"
        )
    return _result_with_receipt(
        repo_root, run_id, version, surface, "restored", "baseline-restored", {},
        restoration_status="restored",
    )


def _disable_and_receipt(
    repo_root: Path,
    paths: dict[str, Path],
    run_id: str,
    version: str,
    surface: str,
    reason: str,
) -> ClaudeProfileResult:
    _ensure_private_dir(paths["root"])
    _write_json_atomic(paths["disabled"], {"schema": STATE_SCHEMA, "reason_code": reason})
    return _result_with_receipt(
        repo_root,
        run_id,
        version,
        surface,
        "full-load",
        reason,
        {},
        restoration_status="recovery-required",
        recovery_action="inspect the preserved settings and profile state before manual recovery",
    )


def _rollback_failed_apply(settings_path: Path, paths: dict[str, Path]) -> None:
    if paths["state"].is_file():
        state = _read_json(paths["state"])
        current = settings_path.read_bytes() if settings_path.is_file() else b""
        applied_digest = state.get("applied_digest")
        baseline_digest = state.get("baseline_digest")
        if _digest(current) in {applied_digest, baseline_digest}:
            baseline = base64.b64decode(state.get("baseline_bytes", ""))
            if state.get("baseline_exists"):
                _write_bytes_atomic(settings_path, baseline, private_parent=False)
            elif settings_path.exists():
                settings_path.unlink()
            paths["state"].unlink(missing_ok=True)
            paths["lease"].unlink(missing_ok=True)
            return
        _write_json_atomic(paths["disabled"], {"schema": STATE_SCHEMA, "reason_code": "rollback-cas-mismatch"})
        return
    paths["lease"].unlink(missing_ok=True)


def _result_with_receipt(
    repo_root: Path,
    run_id: str,
    version: str,
    surface: str,
    status: str,
    reason: str,
    planned: dict[str, str],
    *,
    inventory_fingerprint: str | None = None,
    fresh_session_required: bool = False,
    restoration_status: str | None = None,
    recovery_action: str | None = None,
) -> ClaudeProfileResult:
    payload: dict[str, Any] = {
        "schema": receipts.SCHEMA,
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": "claude",
        "provider_version": version,
        "surface": surface,
        "status": status,
        "completed": True,
        "referenced": False,
        "reason_codes": [reason],
        "classifications": sorted(set(planned.values())) or ["none"],
        "requested_action": "user-invocable-only" if planned else "full-load",
        "actual_action": status,
    }
    if inventory_fingerprint:
        payload["inventory_fingerprint"] = inventory_fingerprint
    if restoration_status:
        payload["restoration_status"] = restoration_status
    receipts.write_receipt(repo_root, payload)
    return ClaudeProfileResult(
        status,
        reason,
        run_id,
        planned,
        fresh_session_required=fresh_session_required,
        recovery_action=recovery_action,
    )


def _profile_paths(repo_root: Path, settings_path: Path) -> dict[str, Path]:
    root = Path(repo_root) / PROFILE_RELATIVE / _settings_key(settings_path)
    return {
        "root": root,
        "lease": root / "lease.json",
        "state": root / "state.json",
        "disabled": root / "disabled.json",
    }


def _settings_key(path: Path) -> str:
    return hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:24]


def _digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _decode_settings(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise ClaudeProfileError("settings must be a JSON object")
    return value


def _ensure_private_dir(path: Path) -> None:
    if path.is_symlink():
        raise ClaudeProfileError("private storage path must not be a symlink")
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.is_symlink():
        raise ClaudeProfileError("private storage path must not be a symlink")
    os.chmod(path, 0o700)


def _ensure_profile_root(repo_root: Path, root: Path) -> None:
    app_root = Path(repo_root) / ".context-guard"
    current = app_root
    _ensure_private_dir(current)
    for part in root.relative_to(app_root).parts:
        current = current / part
        _ensure_private_dir(current)


def _write_json_atomic(path: Path, value: Mapping[str, Any]) -> None:
    _write_bytes_atomic(path, (json.dumps(value, sort_keys=True) + "\n").encode("utf-8"))


def _write_bytes_atomic(path: Path, value: bytes, *, private_parent: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if private_parent:
        os.chmod(path.parent, 0o700)
    temporary = path.parent / f".{path.name}.{secrets.token_hex(8)}.tmp"
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=True) as handle:
            fd = -1
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        os.chmod(path, 0o600)
        _fsync_dir(path.parent)
    finally:
        if fd >= 0:
            os.close(fd)
        if temporary.exists():
            temporary.unlink()


def _create_exclusive_json(path: Path, value: Mapping[str, Any]) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path.parent, 0o700)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        return False
    with os.fdopen(fd, "wb") as handle:
        handle.write((json.dumps(value, sort_keys=True) + "\n").encode("utf-8"))
        handle.flush()
        os.fsync(handle.fileno())
    _fsync_dir(path.parent)
    return True


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _lease_owner_alive(path: Path) -> bool:
    lease = _read_json(path)
    return _pid_alive(lease.get("pid"))


def _pid_alive(pid: object) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
