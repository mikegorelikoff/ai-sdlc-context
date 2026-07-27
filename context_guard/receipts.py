"""Privacy-safe, local decision receipt storage."""

from __future__ import annotations

import contextlib
import fcntl
import json
import os
import re
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator, Mapping


SCHEMA = "context-guard-receipt/v1"
DEFAULT_RETENTION_DAYS = 30
RECEIPTS_RELATIVE = Path(".context-guard") / "receipts"

_RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_REQUIRED_FIELDS = {
    "schema",
    "run_id",
    "timestamp",
    "provider",
    "provider_version",
    "surface",
    "status",
    "completed",
    "referenced",
}
_OPTIONAL_STRING_FIELDS = {
    "pair_id",
    "model",
    "task_id",
    "repository_fingerprint",
    "policy_fingerprint",
    "inventory_fingerprint",
    "requested_action",
    "actual_action",
    "fallback_reason",
    "quality_ref",
    "measurement_ref",
    "restoration_status",
}
_OPTIONAL_STRING_LIST_FIELDS = {
    "identity_digests",
    "reason_codes",
    "classifications",
}
_ALLOWED_FIELDS = _REQUIRED_FIELDS | _OPTIONAL_STRING_FIELDS | _OPTIONAL_STRING_LIST_FIELDS
_PROVIDERS = {"claude", "codex"}
_STATUSES = {"attempted", "valid", "invalid", "full-load", "reduced", "restored"}


class ReceiptError(ValueError):
    """Base error for receipt operations."""

    code = "RECEIPT_ERROR"

    def __str__(self) -> str:
        return f"{self.code}: {super().__str__()}"


class ReceiptValidationError(ReceiptError):
    code = "RECEIPT_INVALID"


class ReceiptExistsError(ReceiptError):
    code = "RECEIPT_EXISTS"


class ReceiptBusyError(ReceiptError):
    code = "RECEIPT_BUSY"


class ReceiptNotFoundError(ReceiptError):
    code = "RECEIPT_NOT_FOUND"


class ReceiptCorruptError(ReceiptError):
    code = "RECEIPT_CORRUPT"

    def __init__(self, run_id: str, quarantine_path: Path):
        self.run_id = run_id
        self.quarantine_path = quarantine_path
        super().__init__(f"{run_id} quarantined at {quarantine_path}")


@dataclass(frozen=True)
class PruneResult:
    deleted: tuple[str, ...]
    retained: tuple[str, ...]
    quarantined: tuple[str, ...]

    def to_dict(self) -> dict[str, list[str]]:
        return {
            "deleted": list(self.deleted),
            "retained": list(self.retained),
            "quarantined": list(self.quarantined),
        }


def _base(repo_root: Path) -> Path:
    return Path(repo_root) / RECEIPTS_RELATIVE


def _records(repo_root: Path) -> Path:
    return _base(repo_root) / "records"


def _quarantine(repo_root: Path) -> Path:
    return _base(repo_root) / "quarantine"


def _ensure_private_dir(path: Path) -> None:
    if path.is_symlink():
        raise ReceiptValidationError("private storage path must not be a symlink")
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.is_symlink():
        raise ReceiptValidationError("private storage path must not be a symlink")
    os.chmod(path, 0o700)


def _ensure_layout(repo_root: Path) -> None:
    base = _base(repo_root)
    _ensure_private_dir(base.parent)
    _ensure_private_dir(base)
    _ensure_private_dir(_records(repo_root))
    _ensure_private_dir(_quarantine(repo_root))


def _validate_run_id(run_id: object) -> str:
    if not isinstance(run_id, str) or not _RUN_ID.fullmatch(run_id):
        raise ReceiptValidationError("run_id must match [A-Za-z0-9][A-Za-z0-9._-]{0,127}")
    return run_id


def _parse_timestamp(value: object) -> datetime:
    if not isinstance(value, str):
        raise ReceiptValidationError("timestamp must be an ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReceiptValidationError("timestamp must be a valid ISO-8601 value") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ReceiptValidationError("timestamp must include a timezone")
    return parsed


def validate_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Return a normalized receipt or raise before any persistence occurs."""
    if not isinstance(payload, Mapping):
        raise ReceiptValidationError("receipt must be an object")
    keys = set(payload)
    unknown = sorted(keys - _ALLOWED_FIELDS)
    missing = sorted(_REQUIRED_FIELDS - keys)
    if unknown:
        raise ReceiptValidationError(f"unknown fields: {', '.join(unknown)}")
    if missing:
        raise ReceiptValidationError(f"missing fields: {', '.join(missing)}")
    if payload["schema"] != SCHEMA:
        raise ReceiptValidationError(f"schema must be {SCHEMA}")

    normalized = dict(payload)
    normalized["run_id"] = _validate_run_id(payload["run_id"])
    _parse_timestamp(payload["timestamp"])

    if payload["provider"] not in _PROVIDERS:
        raise ReceiptValidationError("provider must be claude or codex")
    for field in ("provider_version", "surface"):
        if not isinstance(payload[field], str) or not payload[field]:
            raise ReceiptValidationError(f"{field} must be a non-empty string")
    if payload["status"] not in _STATUSES:
        raise ReceiptValidationError(f"status must be one of {', '.join(sorted(_STATUSES))}")
    for field in ("completed", "referenced"):
        if type(payload[field]) is not bool:
            raise ReceiptValidationError(f"{field} must be a boolean")

    for field in _OPTIONAL_STRING_FIELDS:
        if field in payload and (not isinstance(payload[field], str) or not payload[field]):
            raise ReceiptValidationError(f"{field} must be a non-empty string")
    for field in _OPTIONAL_STRING_LIST_FIELDS:
        if field not in payload:
            continue
        value = payload[field]
        if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
            raise ReceiptValidationError(f"{field} must be a list of non-empty strings")
        normalized[field] = list(value)
    return normalized


def _decode_receipt(raw: bytes) -> dict[str, Any]:
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReceiptValidationError("record is not valid UTF-8 JSON") from exc
    return validate_receipt(payload)


@contextlib.contextmanager
def writer_lock(repo_root: Path) -> Iterator[None]:
    """Acquire the receipt store's non-blocking single-writer lock."""
    _ensure_layout(repo_root)
    lock_path = _base(repo_root) / ".writer.lock"
    fd = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
    os.fchmod(fd, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ReceiptBusyError("another receipt mutation is in progress") from exc
        yield
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


def _fsync_directory(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_receipt(repo_root: Path, payload: Mapping[str, Any]) -> Path:
    """Validate and atomically persist one non-overwriting receipt."""
    normalized = validate_receipt(payload)
    run_id = normalized["run_id"]
    encoded = (json.dumps(normalized, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    # Validate the exact serialized representation before taking the writer lock.
    _decode_receipt(encoded)

    with writer_lock(repo_root):
        records = _records(repo_root)
        target = records / f"{run_id}.json"
        if target.exists():
            raise ReceiptExistsError(f"receipt already exists for run_id {run_id}")
        temporary = records / f".{run_id}.{secrets.token_hex(8)}.tmp"
        fd = -1
        try:
            fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "wb", closefd=True) as handle:
                fd = -1
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            _decode_receipt(temporary.read_bytes())
            os.replace(temporary, target)
            os.chmod(target, 0o600)
            _fsync_directory(records)
        finally:
            if fd >= 0:
                os.close(fd)
            if temporary.exists():
                temporary.unlink()
        return target


def _record_path(repo_root: Path, run_id: str) -> Path:
    return _records(repo_root) / f"{_validate_run_id(run_id)}.json"


def _quarantine_locked(repo_root: Path, path: Path, run_id: str) -> Path:
    quarantine = _quarantine(repo_root)
    destination = quarantine / f"{run_id}.json"
    if destination.exists():
        destination = quarantine / f"{run_id}.{secrets.token_hex(8)}.json"
    os.replace(path, destination)
    os.chmod(destination, 0o600)
    _fsync_directory(quarantine)
    _fsync_directory(path.parent)
    return destination


def inspect_receipt(repo_root: Path, run_id: str) -> dict[str, Any]:
    """Read one validated receipt; quarantine corrupt bytes."""
    path = _record_path(repo_root, run_id)
    if not path.is_file():
        raise ReceiptNotFoundError(f"no receipt for run_id {run_id}")
    try:
        return _decode_receipt(path.read_bytes())
    except (OSError, ReceiptValidationError):
        with writer_lock(repo_root):
            if not path.is_file():
                raise ReceiptNotFoundError(f"no receipt for run_id {run_id}")
            try:
                return _decode_receipt(path.read_bytes())
            except (OSError, ReceiptValidationError):
                quarantined = _quarantine_locked(repo_root, path, run_id)
        raise ReceiptCorruptError(run_id, quarantined)


def delete_receipt(repo_root: Path, run_id: str) -> bool:
    """Delete only the exact validated run id."""
    path = _record_path(repo_root, run_id)
    with writer_lock(repo_root):
        if not path.is_file():
            return False
        path.unlink()
        _fsync_directory(path.parent)
        return True


def prune_receipts(
    repo_root: Path,
    *,
    now: datetime | None = None,
    retention_days: int = DEFAULT_RETENTION_DAYS,
) -> PruneResult:
    """Prune completed, unreferenced receipts older than the retention cutoff."""
    if type(retention_days) is not int or retention_days < 1:
        raise ReceiptValidationError("retention_days must be a positive integer")
    reference_time = now or datetime.now(timezone.utc)
    if reference_time.tzinfo is None or reference_time.utcoffset() is None:
        raise ReceiptValidationError("now must include a timezone")
    cutoff = reference_time - timedelta(days=retention_days)
    deleted: list[str] = []
    retained: list[str] = []
    quarantined: list[str] = []

    with writer_lock(repo_root):
        records = _records(repo_root)
        for path in sorted(records.glob("*.json"), key=lambda item: item.name):
            run_id = path.stem
            try:
                receipt = _decode_receipt(path.read_bytes())
                if receipt["run_id"] != run_id:
                    raise ReceiptValidationError("filename and run_id do not match")
            except (OSError, ReceiptValidationError):
                destination = _quarantine_locked(repo_root, path, run_id)
                quarantined.append(destination.name)
                continue
            timestamp = _parse_timestamp(receipt["timestamp"])
            if receipt["completed"] and not receipt["referenced"] and timestamp < cutoff:
                path.unlink()
                deleted.append(run_id)
            else:
                retained.append(run_id)
        _fsync_directory(records)
    return PruneResult(tuple(deleted), tuple(retained), tuple(quarantined))
