"""Provider-neutral frozen-fixture quality gates and authorization ledger."""

from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

from context_guard import receipts


MANIFEST_SCHEMA = "context-guard-quality-manifest/v1"
ATTEMPT_SCHEMA = "context-guard-quality-attempt/v1"
LEDGER_SCHEMA = "context-guard-quality-ledger/v1"
QUALITY_RELATIVE = Path(".context-guard") / "quality"
FIXTURE_KINDS = {"read-only-analysis", "test-only-change", "explicit-ai-sdlc-skill"}
PROVIDERS = {"claude", "codex"}
GATE_IDS = tuple(f"QG-{number}" for number in range(301, 310))

_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_MANIFEST_FIELDS = {
    "schema",
    "fixture_id",
    "fixture_kind",
    "provider",
    "provider_version",
    "model",
    "repository_fingerprint",
    "task_fingerprint",
    "baseline_profile_fingerprint",
    "guarded_profile_fingerprint",
    "required_instruction_ids",
}
_ATTEMPT_FIELDS = {
    "schema",
    "attempt_id",
    "pair_id",
    "role",
    "fixture_id",
    "provider",
    "provider_version",
    "model",
    "repository_fingerprint",
    "task_fingerprint",
    "profile_fingerprint",
    "fresh_session",
    "completion_passed",
    "observed_instruction_ids",
    "explicit_skill_invoked",
    "restoration_passed",
    "receipt_ref",
    "receipt_valid",
    "privacy_passed",
}
_EVALUATION_FIELDS = {
    "schema",
    "event",
    "timestamp",
    "run_id",
    "pair_id",
    "fixture_id",
    "fixture_kind",
    "provider",
    "provider_version",
    "model",
    "valid",
    "measurement_allowed",
    "manifest_fingerprint",
    "attempt_fingerprints",
    "gates",
}
_INVALIDATION_FIELDS = {
    "schema",
    "event",
    "timestamp",
    "run_id",
    "pair_id",
    "reason_code",
}


class QualityError(ValueError):
    code = "QUALITY_INVALID"

    def __str__(self) -> str:
        return f"{self.code}: {super().__str__()}"


class QualityBusyError(QualityError):
    code = "QUALITY_BUSY"


@dataclass(frozen=True)
class QualityManifest:
    schema: str
    fixture_id: str
    fixture_kind: str
    provider: str
    provider_version: str
    model: str
    repository_fingerprint: str
    task_fingerprint: str
    baseline_profile_fingerprint: str
    guarded_profile_fingerprint: str
    required_instruction_ids: tuple[str, ...]

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "QualityManifest":
        _exact_fields(value, _MANIFEST_FIELDS, "manifest")
        if value["schema"] != MANIFEST_SCHEMA:
            raise QualityError(f"manifest schema must be {MANIFEST_SCHEMA}")
        fixture_id = _identifier(value["fixture_id"], "fixture_id")
        if value["fixture_kind"] not in FIXTURE_KINDS:
            raise QualityError("fixture_kind is unsupported")
        strings = _strings(
            value,
            (
                "provider",
                "provider_version",
                "model",
                "repository_fingerprint",
                "task_fingerprint",
                "baseline_profile_fingerprint",
                "guarded_profile_fingerprint",
            ),
        )
        if strings["provider"] not in PROVIDERS:
            raise QualityError("provider must be claude or codex")
        required = _string_list(value["required_instruction_ids"], "required_instruction_ids")
        return cls(
            MANIFEST_SCHEMA,
            fixture_id,
            value["fixture_kind"],
            strings["provider"],
            strings["provider_version"],
            strings["model"],
            strings["repository_fingerprint"],
            strings["task_fingerprint"],
            strings["baseline_profile_fingerprint"],
            strings["guarded_profile_fingerprint"],
            required,
        )

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["required_instruction_ids"] = list(self.required_instruction_ids)
        return result

    @property
    def fingerprint(self) -> str:
        return _canonical_digest(self.to_dict())


@dataclass(frozen=True)
class AttemptEvidence:
    schema: str
    attempt_id: str
    pair_id: str
    role: str
    fixture_id: str
    provider: str
    provider_version: str
    model: str
    repository_fingerprint: str
    task_fingerprint: str
    profile_fingerprint: str
    fresh_session: bool
    completion_passed: bool
    observed_instruction_ids: tuple[str, ...]
    explicit_skill_invoked: bool
    restoration_passed: bool
    receipt_ref: str
    receipt_valid: bool
    privacy_passed: bool

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "AttemptEvidence":
        _exact_fields(value, _ATTEMPT_FIELDS, "attempt")
        if value["schema"] != ATTEMPT_SCHEMA:
            raise QualityError(f"attempt schema must be {ATTEMPT_SCHEMA}")
        attempt_id = _identifier(value["attempt_id"], "attempt_id")
        pair_id = _identifier(value["pair_id"], "pair_id")
        fixture_id = _identifier(value["fixture_id"], "fixture_id")
        if value["role"] not in {"baseline", "guarded"}:
            raise QualityError("role must be baseline or guarded")
        strings = _strings(
            value,
            (
                "provider",
                "provider_version",
                "model",
                "repository_fingerprint",
                "task_fingerprint",
                "profile_fingerprint",
                "receipt_ref",
            ),
        )
        if strings["provider"] not in PROVIDERS:
            raise QualityError("provider must be claude or codex")
        booleans = {}
        for field in (
            "fresh_session",
            "completion_passed",
            "explicit_skill_invoked",
            "restoration_passed",
            "receipt_valid",
            "privacy_passed",
        ):
            if type(value[field]) is not bool:
                raise QualityError(f"{field} must be a boolean")
            booleans[field] = value[field]
        observed = _string_list(value["observed_instruction_ids"], "observed_instruction_ids")
        return cls(
            ATTEMPT_SCHEMA,
            attempt_id,
            pair_id,
            value["role"],
            fixture_id,
            strings["provider"],
            strings["provider_version"],
            strings["model"],
            strings["repository_fingerprint"],
            strings["task_fingerprint"],
            strings["profile_fingerprint"],
            booleans["fresh_session"],
            booleans["completion_passed"],
            observed,
            booleans["explicit_skill_invoked"],
            booleans["restoration_passed"],
            strings["receipt_ref"],
            booleans["receipt_valid"],
            booleans["privacy_passed"],
        )

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["observed_instruction_ids"] = list(self.observed_instruction_ids)
        return result

    @property
    def fingerprint(self) -> str:
        return _canonical_digest(self.to_dict())


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    passed: bool
    reason_code: str


@dataclass(frozen=True)
class PairEvaluation:
    pair_id: str
    fixture_id: str
    valid: bool
    measurement_allowed: bool
    gates: tuple[GateResult, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "pair_id": self.pair_id,
            "fixture_id": self.fixture_id,
            "valid": self.valid,
            "measurement_allowed": self.measurement_allowed,
            "gates": [asdict(gate) for gate in self.gates],
        }


@dataclass(frozen=True)
class Authorization:
    pair_id: str
    allowed: bool
    reason_code: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def validate_suite(manifests: Iterable[QualityManifest]) -> tuple[QualityManifest, ...]:
    values = tuple(manifests)
    kinds = [manifest.fixture_kind for manifest in values]
    ids = [manifest.fixture_id for manifest in values]
    if len(values) != 3 or set(kinds) != FIXTURE_KINDS:
        raise QualityError("suite must contain exactly one manifest for each fixture kind")
    if len(set(ids)) != len(ids):
        raise QualityError("suite fixture_id values must be unique")
    return tuple(sorted(values, key=lambda item: item.fixture_kind))


def evaluate_pair(
    manifest: QualityManifest,
    first: AttemptEvidence,
    second: AttemptEvidence,
) -> PairEvaluation:
    by_role = {first.role: first, second.role: second}
    baseline = by_role.get("baseline")
    guarded = by_role.get("guarded")
    pair_id = first.pair_id

    qg301 = True
    qg302 = (
        baseline is not None
        and guarded is not None
        and first.role != second.role
        and first.attempt_id != second.attempt_id
        and first.pair_id == second.pair_id
        and first.fixture_id == second.fixture_id == manifest.fixture_id
    )
    if baseline is None or guarded is None:
        baseline, guarded = first, second
    qg303 = all(
        all(
            (
            attempt.provider == manifest.provider,
            attempt.provider_version == manifest.provider_version,
            attempt.model == manifest.model,
            attempt.repository_fingerprint == manifest.repository_fingerprint,
            attempt.task_fingerprint == manifest.task_fingerprint,
            attempt.profile_fingerprint
            == (
                manifest.baseline_profile_fingerprint
                if attempt.role == "baseline"
                else manifest.guarded_profile_fingerprint
            ),
            )
        )
        for attempt in (baseline, guarded)
    )
    qg304 = baseline.fresh_session and guarded.fresh_session
    qg305 = baseline.completion_passed and guarded.completion_passed
    required = set(manifest.required_instruction_ids)
    qg306 = required.issubset(baseline.observed_instruction_ids) and required.issubset(
        guarded.observed_instruction_ids
    )
    qg307 = manifest.fixture_kind != "explicit-ai-sdlc-skill" or (
        baseline.explicit_skill_invoked and guarded.explicit_skill_invoked
    )
    qg308 = baseline.restoration_passed and guarded.restoration_passed
    qg309 = all(
        attempt.receipt_ref and attempt.receipt_valid and attempt.privacy_passed
        for attempt in (baseline, guarded)
    )
    checks = (qg301, qg302, qg303, qg304, qg305, qg306, qg307, qg308, qg309)
    reasons = (
        "manifest-valid",
        "pair-correlated",
        "fingerprints-match",
        "fresh-sessions",
        "completion-oracles-pass",
        "instructions-preserved",
        "explicit-skill-oracle-pass",
        "restoration-pass",
        "receipt-privacy-pass",
    )
    failure_reasons = (
        "manifest-invalid",
        "pair-correlation-mismatch",
        "fingerprint-mismatch",
        "fresh-session-missing",
        "completion-oracle-failed",
        "instruction-oracle-failed",
        "explicit-skill-oracle-failed",
        "restoration-failed",
        "receipt-or-privacy-failed",
    )
    gates = tuple(
        GateResult(gate_id, passed, reasons[index] if passed else failure_reasons[index])
        for index, (gate_id, passed) in enumerate(zip(GATE_IDS, checks))
    )
    valid = all(checks)
    return PairEvaluation(pair_id, manifest.fixture_id, valid, valid, gates)


class QualityLedger:
    def __init__(self, repo_root: Path):
        self.root = Path(repo_root) / QUALITY_RELATIVE
        self.path = self.root / "ledger.jsonl"
        self.lock_path = self.root / ".writer.lock"

    def record_evaluation(
        self,
        manifest: QualityManifest,
        first: AttemptEvidence,
        second: AttemptEvidence,
        *,
        run_id: str,
    ) -> PairEvaluation:
        evaluation = evaluate_pair(manifest, first, second)
        record = {
            "schema": LEDGER_SCHEMA,
            "event": "evaluation",
            "timestamp": _now(),
            "run_id": _identifier(run_id, "run_id"),
            "pair_id": evaluation.pair_id,
            "fixture_id": evaluation.fixture_id,
            "fixture_kind": manifest.fixture_kind,
            "provider": manifest.provider,
            "provider_version": manifest.provider_version,
            "model": manifest.model,
            "valid": evaluation.valid,
            "measurement_allowed": evaluation.measurement_allowed,
            "manifest_fingerprint": manifest.fingerprint,
            "attempt_fingerprints": [first.fingerprint, second.fingerprint],
            "gates": [asdict(gate) for gate in evaluation.gates],
        }
        _append_record(self.root, self.path, self.lock_path, record)
        try:
            _write_quality_receipt(
                self.root.parent.parent,
                run_id,
                manifest,
                evaluation,
                "quality-evaluated",
            )
        except (receipts.ReceiptError, OSError):
            invalidation = {
                "schema": LEDGER_SCHEMA,
                "event": "invalidation",
                "timestamp": _now(),
                "run_id": f"{run_id}.receipt-failure"[:128],
                "pair_id": evaluation.pair_id,
                "reason_code": "quality-receipt-failed",
            }
            _append_record(self.root, self.path, self.lock_path, invalidation)
            raise
        return evaluation

    def invalidate(self, pair_id: str, *, run_id: str, reason_code: str) -> Authorization:
        pair_id = _identifier(pair_id, "pair_id")
        run_id = _identifier(run_id, "run_id")
        reason_code = _identifier(reason_code, "reason_code")
        records = _read_records(self.path)
        evaluations = [
            item
            for item in records
            if item.get("event") == "evaluation" and item.get("pair_id") == pair_id
        ]
        if not evaluations:
            raise QualityError("cannot invalidate a pair without evaluation evidence")
        provider = evaluations[-1].get("provider")
        provider_version = evaluations[-1].get("provider_version")
        if provider not in {"claude", "codex"} or not isinstance(provider_version, str):
            raise QualityError("evaluation provider evidence is invalid")
        record = {
            "schema": LEDGER_SCHEMA,
            "event": "invalidation",
            "timestamp": _now(),
            "run_id": run_id,
            "pair_id": pair_id,
            "reason_code": reason_code,
        }
        _append_record(self.root, self.path, self.lock_path, record)
        payload = _base_receipt(
            run_id, "invalid", pair_id, reason_code, provider, provider_version
        )
        payload["quality_ref"] = pair_id
        receipts.write_receipt(self.root.parent.parent, payload)
        return Authorization(pair_id, False, reason_code)

    def authorize(self, pair_id: str) -> Authorization:
        pair_id = _identifier(pair_id, "pair_id")
        try:
            records = _read_records(self.path)
        except QualityError:
            return Authorization(pair_id, False, "corrupt-quality-ledger")
        related = [record for record in records if record.get("pair_id") == pair_id]
        evaluations = [record for record in related if record.get("event") == "evaluation"]
        invalidations = [record for record in related if record.get("event") == "invalidation"]
        if invalidations:
            return Authorization(pair_id, False, invalidations[-1].get("reason_code", "invalidated"))
        if not evaluations:
            return Authorization(pair_id, False, "missing-quality-evidence")
        if len(evaluations) != 1:
            return Authorization(pair_id, False, "ambiguous-quality-evidence")
        evaluation = evaluations[0]
        if evaluation.get("valid") is True and evaluation.get("measurement_allowed") is True:
            return Authorization(pair_id, True, "quality-gates-pass")
        return Authorization(pair_id, False, "quality-gates-failed")

    def authorize_measurement(
        self,
        pair_id: str,
        *,
        provider: str,
        provider_version: str,
        model: str,
        fixture_kind: str,
    ) -> Authorization:
        authorization = self.authorize(pair_id)
        if not authorization.allowed:
            return authorization
        try:
            matching = [
                record
                for record in _read_records(self.path)
                if record.get("event") == "evaluation" and record.get("pair_id") == pair_id
            ]
        except QualityError:
            return Authorization(pair_id, False, "corrupt-quality-ledger")
        if len(matching) != 1:
            return Authorization(pair_id, False, "ambiguous-quality-evidence")
        record = matching[0]
        if (
            record.get("provider") != provider
            or record.get("provider_version") != provider_version
            or record.get("model") != model
            or record.get("fixture_kind") != fixture_kind
        ):
            return Authorization(pair_id, False, "quality-context-mismatch")
        return authorization


def _write_quality_receipt(
    repo_root: Path,
    run_id: str,
    manifest: QualityManifest,
    evaluation: PairEvaluation,
    reason: str,
) -> None:
    status = "valid" if evaluation.valid else "invalid"
    payload = _base_receipt(
        run_id,
        status,
        evaluation.pair_id,
        reason,
        manifest.provider,
        manifest.provider_version,
    )
    payload["quality_ref"] = evaluation.pair_id
    payload["repository_fingerprint"] = manifest.repository_fingerprint
    payload["reason_codes"] = [gate.reason_code for gate in evaluation.gates if not gate.passed] or [
        reason
    ]
    receipts.write_receipt(repo_root, payload)


def _base_receipt(
    run_id: str,
    status: str,
    pair_id: str,
    reason: str,
    provider: str,
    provider_version: str,
) -> dict[str, Any]:
    return {
        "schema": receipts.SCHEMA,
        "run_id": run_id,
        "timestamp": _now(),
        "provider": provider,
        "provider_version": provider_version,
        "surface": "quality-runner",
        "status": status,
        "completed": True,
        "referenced": True,
        "pair_id": pair_id,
        "reason_codes": [reason],
        "classifications": ["quality-gate"],
        "requested_action": "quality-evaluate",
        "actual_action": "measurement-allowed" if status == "valid" else "measurement-denied",
    }


def _append_record(root: Path, path: Path, lock_path: Path, record: Mapping[str, Any]) -> None:
    with writer_lock(root, lock_path):
        encoded = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        with os.fdopen(fd, "ab", closefd=True) as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(path, 0o600)
        _fsync_dir(root)


@contextlib.contextmanager
def writer_lock(root: Path, lock_path: Path | None = None) -> Iterator[None]:
    """Acquire the non-blocking single-writer lock for a quality ledger root."""
    _ensure_private(root.parent)
    _ensure_private(root)
    lock_path = lock_path or root / ".writer.lock"
    lock_fd = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
    os.fchmod(lock_fd, 0o600)
    try:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise QualityBusyError("quality ledger writer is busy") from exc
        yield
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        finally:
            os.close(lock_fd)


def _read_records(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    records = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        for line in lines:
            record = json.loads(line)
            if not isinstance(record, dict) or record.get("schema") != LEDGER_SCHEMA:
                raise QualityError("invalid quality ledger record")
            _validate_ledger_record(record)
            records.append(record)
    except (OSError, json.JSONDecodeError) as exc:
        raise QualityError("corrupt quality ledger") from exc
    return records


def _validate_ledger_record(record: Mapping[str, Any]) -> None:
    event = record.get("event")
    _identifier(record.get("pair_id"), "pair_id")
    _identifier(record.get("run_id"), "run_id")
    if event == "invalidation":
        _exact_fields(record, _INVALIDATION_FIELDS, "quality ledger invalidation")
        _identifier(record.get("reason_code"), "reason_code")
        return
    if event != "evaluation":
        raise QualityError("quality ledger event is unsupported")
    _exact_fields(record, _EVALUATION_FIELDS, "quality ledger evaluation")
    _identifier(record.get("fixture_id"), "fixture_id")
    if record.get("provider") not in PROVIDERS:
        raise QualityError("quality ledger provider is invalid")
    if record.get("fixture_kind") not in FIXTURE_KINDS:
        raise QualityError("quality ledger fixture_kind is invalid")
    if not isinstance(record.get("provider_version"), str) or not record["provider_version"]:
        raise QualityError("quality ledger provider_version is invalid")
    if not isinstance(record.get("model"), str) or not record["model"]:
        raise QualityError("quality ledger model is invalid")
    if type(record.get("valid")) is not bool or type(record.get("measurement_allowed")) is not bool:
        raise QualityError("quality ledger authorization flags are invalid")
    gates = record.get("gates")
    if not isinstance(gates, list) or len(gates) != len(GATE_IDS):
        raise QualityError("quality ledger gates are invalid")
    for expected, gate in zip(GATE_IDS, gates):
        if (
            not isinstance(gate, dict)
            or gate.get("gate_id") != expected
            or type(gate.get("passed")) is not bool
            or not isinstance(gate.get("reason_code"), str)
            or not gate["reason_code"]
        ):
            raise QualityError("quality ledger gate evidence is invalid")


def _exact_fields(value: Mapping[str, Any], allowed: set[str], label: str) -> None:
    if not isinstance(value, Mapping):
        raise QualityError(f"{label} must be an object")
    unknown = sorted(set(value) - allowed)
    missing = sorted(allowed - set(value))
    if unknown:
        raise QualityError(f"{label} unknown fields: {', '.join(unknown)}")
    if missing:
        raise QualityError(f"{label} missing fields: {', '.join(missing)}")


def _identifier(value: object, field: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise QualityError(f"{field} is invalid")
    return value


def _strings(value: Mapping[str, Any], fields: Iterable[str]) -> dict[str, str]:
    result = {}
    for field in fields:
        item = value[field]
        if not _safe_text(item):
            raise QualityError(f"{field} must be a non-empty string")
        result[field] = item
    return result


def _string_list(value: object, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) > 128 or any(
        not _safe_text(item) for item in value
    ):
        raise QualityError(f"{field} must be a list of non-empty strings")
    if len(set(value)) != len(value):
        raise QualityError(f"{field} must not contain duplicates")
    return tuple(value)


def _safe_text(value: object) -> bool:
    return (
        isinstance(value, str)
        and 0 < len(value) <= 256
        and all(character >= " " and character != "\x7f" for character in value)
    )


def _canonical_digest(value: Mapping[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _ensure_private(path: Path) -> None:
    if path.is_symlink():
        raise QualityError("private storage path must not be a symlink")
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.is_symlink():
        raise QualityError("private storage path must not be a symlink")
    os.chmod(path, 0o700)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
