"""Read-only Claude cache-token extraction and exact paired statistics."""

from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import math
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

from context_guard import inventory, quality, receipts


RUN_SCHEMA = "context-guard-claude-run-measurement/v1"
PAIR_SCHEMA = "context-guard-claude-pair-measurement/v1"
QUALIFICATION_SCHEMA = "context-guard-claude-qualification/v1"
LEDGER_SCHEMA = "context-guard-claude-measurement-ledger/v1"
MEASUREMENT_RELATIVE = Path(".context-guard") / "measurements"
FIXTURE_KINDS = quality.FIXTURE_KINDS
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")


class ClaudeMeasurementError(ValueError):
    code = "CLAUDE_MEASUREMENT_INVALID"

    def __str__(self) -> str:
        return f"{self.code}: {super().__str__()}"


class ClaudeMeasurementBusyError(ClaudeMeasurementError):
    code = "CLAUDE_MEASUREMENT_BUSY"


@dataclass(frozen=True)
class ClaudeRunMeasurement:
    schema: str
    run_id: str
    quality_pair_id: str
    fixture_kind: str
    role: str
    provider_version: str
    model: str
    session_id: str
    status: str
    reason_code: str
    source_fingerprint: str
    eligible_rows: int
    duplicate_rows: int
    cache_creation_tokens: int
    cache_read_tokens: int
    cache_tokens: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ClaudeRunMeasurement":
        fields = tuple(cls.__dataclass_fields__)
        _exact_fields(value, fields, "Claude run")
        if value["schema"] != RUN_SCHEMA:
            raise ClaudeMeasurementError("Claude run schema is invalid")
        result = cls(**value)
        _validate_run(result)
        return result


@dataclass(frozen=True)
class ClaudePairMeasurement:
    schema: str
    pair_id: str
    quality_pair_id: str
    fixture_kind: str
    provider_version: str
    model: str
    execution_order: str
    baseline_run_id: str
    guarded_run_id: str
    baseline_cache_tokens: int
    guarded_cache_tokens: int
    reduction_numerator: int
    reduction_denominator: int

    @property
    def reduction(self) -> Fraction:
        return Fraction(self.reduction_numerator, self.reduction_denominator)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ClaudePairMeasurement":
        fields = tuple(cls.__dataclass_fields__)
        _exact_fields(value, fields, "Claude pair")
        if value["schema"] != PAIR_SCHEMA:
            raise ClaudeMeasurementError("Claude pair schema is invalid")
        result = cls(**value)
        _validate_pair(result)
        return result


@dataclass(frozen=True)
class ClaudeQualification:
    schema: str
    qualification_id: str
    provider_version: str
    model: str
    passed: bool
    reason_codes: tuple[str, ...]
    pair_ids: tuple[str, ...]
    provider_median_numerator: int
    provider_median_denominator: int
    q1_numerator: int
    q1_denominator: int
    fixture_medians: tuple[tuple[str, int, int], ...]

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["reason_codes"] = list(self.reason_codes)
        result["pair_ids"] = list(self.pair_ids)
        result["fixture_medians"] = [
            {"fixture_kind": kind, "numerator": numerator, "denominator": denominator}
            for kind, numerator, denominator in self.fixture_medians
        ]
        return result

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ClaudeQualification":
        fields = tuple(cls.__dataclass_fields__)
        _exact_fields(value, fields, "Claude qualification")
        medians = value["fixture_medians"]
        if (
            not isinstance(medians, list)
            or not isinstance(value["reason_codes"], list)
            or not isinstance(value["pair_ids"], list)
        ):
            raise ClaudeMeasurementError("qualification collections must be lists")
        normalized = []
        for item in medians:
            _exact_fields(
                item, ("fixture_kind", "numerator", "denominator"), "fixture median"
            )
            normalized.append(
                (item["fixture_kind"], item["numerator"], item["denominator"])
            )
        result = cls(
            value["schema"],
            value["qualification_id"],
            value["provider_version"],
            value["model"],
            value["passed"],
            tuple(value["reason_codes"]),
            tuple(value["pair_ids"]),
            value["provider_median_numerator"],
            value["provider_median_denominator"],
            value["q1_numerator"],
            value["q1_denominator"],
            tuple(normalized),
        )
        _validate_qualification(result)
        return result


class MeasurementLedger:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.root = self.repo_root / MEASUREMENT_RELATIVE
        self.path = self.root / "ledger.jsonl"
        self.lock_path = self.root / ".writer.lock"

    def record_run(self, measurement: ClaudeRunMeasurement) -> None:
        _validate_run(measurement)
        self._record(
            "run",
            measurement.run_id,
            measurement.to_dict(),
            provider_version=measurement.provider_version,
            quality_ref=measurement.quality_pair_id,
            passed=True,
        )

    def record_pair(self, measurement: ClaudePairMeasurement) -> None:
        _validate_pair(measurement)
        self._record(
            "pair",
            measurement.pair_id,
            measurement.to_dict(),
            provider_version=measurement.provider_version,
            quality_ref=measurement.quality_pair_id,
            passed=True,
        )

    def record_qualification(self, qualification: ClaudeQualification) -> None:
        _validate_qualification(qualification)
        self._record(
            "qualification",
            qualification.qualification_id,
            qualification.to_dict(),
            provider_version=qualification.provider_version,
            quality_ref=None,
            passed=qualification.passed,
        )

    def _record(
        self,
        event: str,
        identifier: str,
        evidence: Mapping[str, Any],
        *,
        provider_version: str,
        quality_ref: str | None,
        passed: bool,
    ) -> None:
        _identifier(identifier, "measurement identifier")
        record = {
            "schema": LEDGER_SCHEMA,
            "event": event,
            "timestamp": _now(),
            "identifier": identifier,
            "evidence": dict(evidence),
        }
        payload = {
            "schema": receipts.SCHEMA,
            "run_id": identifier,
            "timestamp": _now(),
            "provider": "claude",
            "provider_version": provider_version,
            "surface": "claude-measurement",
            "status": "valid" if passed else "invalid",
            "completed": True,
            "referenced": True,
            "measurement_ref": identifier,
            "reason_codes": [f"claude-{event}-recorded"],
            "classifications": ["native-cache-tokens"],
            "requested_action": f"claude-{event}",
            "actual_action": f"claude-{event}-{'pass' if passed else 'fail'}",
        }
        if quality_ref is not None:
            payload["quality_ref"] = quality_ref
        with _writer_lock(self.root, self.lock_path):
            if any(item["identifier"] == identifier for item in self.records()):
                raise ClaudeMeasurementError(
                    f"measurement evidence already exists for {identifier}"
                )
            # A missing receipt must never leave apparently usable ledger evidence.
            receipts.write_receipt(self.repo_root, payload)
            _append_record_unlocked(self.root, self.path, record)

    def records(self) -> tuple[dict[str, Any], ...]:
        if not self.path.is_file():
            return ()
        result = []
        try:
            for line in self.path.read_text(encoding="utf-8").splitlines():
                record = json.loads(line)
                _validate_record(record)
                result.append(record)
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            raise ClaudeMeasurementError("corrupt-measurement-ledger") from exc
        return tuple(result)


def extract_run(
    repo_root: Path,
    source: Path,
    *,
    run_id: str,
    quality_pair_id: str,
    fixture_kind: str,
    role: str,
    provider_version: str,
    model: str,
    session_id: str,
) -> ClaudeRunMeasurement:
    """Extract one explicit Claude JSONL session after quality authorization."""
    run_id = _identifier(run_id, "run_id")
    quality_pair_id = _identifier(quality_pair_id, "quality_pair_id")
    session_id = _identifier(session_id, "session_id")
    if fixture_kind not in FIXTURE_KINDS:
        raise ClaudeMeasurementError("fixture_kind is unsupported")
    if role not in {"baseline", "guarded"}:
        raise ClaudeMeasurementError("role must be baseline or guarded")
    if not isinstance(model, str) or not model or len(model) > 256:
        raise ClaudeMeasurementError("model is invalid")
    preflight = inventory.preflight("claude", provider_version, "cli")
    if preflight.status != "supported":
        raise ClaudeMeasurementError(preflight.reason_code)
    authorization = quality.QualityLedger(repo_root).authorize_measurement(
        quality_pair_id,
        provider="claude",
        provider_version=provider_version,
        model=model,
        fixture_kind=fixture_kind,
    )
    if not authorization.allowed:
        raise ClaudeMeasurementError(f"quality-not-authorized:{authorization.reason_code}")
    if not Path(source).is_file():
        raise ClaudeMeasurementError("source-not-file")

    digest = hashlib.sha256()
    unique: dict[tuple[str, str, str], tuple[int, int]] = {}
    eligible_rows = 0
    duplicate_rows = 0
    try:
        with Path(source).open("rb") as handle:
            for raw_line in handle:
                digest.update(raw_line)
                try:
                    row = json.loads(raw_line)
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise ClaudeMeasurementError("malformed-jsonl") from exc
                if not isinstance(row, dict) or row.get("type") != "assistant":
                    continue
                message = row.get("message")
                if not isinstance(message, dict) or message.get("usage") is None:
                    continue
                if row.get("sessionId") != session_id:
                    continue
                if message.get("model") != model:
                    raise ClaudeMeasurementError("model-drift")
                request_id = row.get("requestId")
                message_id = message.get("id")
                if not isinstance(request_id, str) or not request_id:
                    raise ClaudeMeasurementError("missing-request-id")
                if not isinstance(message_id, str) or not message_id:
                    raise ClaudeMeasurementError("missing-message-id")
                usage = message.get("usage")
                if not isinstance(usage, dict):
                    raise ClaudeMeasurementError("invalid-usage")
                creation = _counter(usage.get("cache_creation_input_tokens"), "cache-creation")
                read = _counter(usage.get("cache_read_input_tokens"), "cache-read")
                eligible_rows += 1
                key = (session_id, request_id, message_id)
                counters = (creation, read)
                previous = unique.get(key)
                if previous is not None:
                    if previous != counters:
                        raise ClaudeMeasurementError("inconsistent-duplicate")
                    duplicate_rows += 1
                    continue
                unique[key] = counters
    except OSError as exc:
        raise ClaudeMeasurementError("source-read-error") from exc
    if not unique:
        raise ClaudeMeasurementError("empty-measurement-window")
    creation_total = sum(item[0] for item in unique.values())
    read_total = sum(item[1] for item in unique.values())
    return ClaudeRunMeasurement(
        RUN_SCHEMA,
        run_id,
        quality_pair_id,
        fixture_kind,
        role,
        provider_version,
        model,
        session_id,
        "measurable",
        "claude-cache-window-valid",
        digest.hexdigest(),
        eligible_rows,
        duplicate_rows,
        creation_total,
        read_total,
        creation_total + read_total,
    )


def compare_pair(
    repo_root: Path,
    baseline: ClaudeRunMeasurement,
    guarded: ClaudeRunMeasurement,
    *,
    pair_id: str,
    execution_order: str,
) -> ClaudePairMeasurement:
    pair_id = _identifier(pair_id, "pair_id")
    if execution_order not in {"baseline-first", "guarded-first"}:
        raise ClaudeMeasurementError("execution_order is invalid")
    if baseline.role != "baseline" or guarded.role != "guarded":
        raise ClaudeMeasurementError("pair roles are invalid")
    comparable = (
        baseline.status == guarded.status == "measurable"
        and baseline.quality_pair_id == guarded.quality_pair_id
        and baseline.fixture_kind == guarded.fixture_kind
        and baseline.provider_version == guarded.provider_version
        and baseline.model == guarded.model
        and baseline.run_id != guarded.run_id
    )
    if not comparable:
        raise ClaudeMeasurementError("pair-correlation-mismatch")
    authorization = quality.QualityLedger(repo_root).authorize_measurement(
        baseline.quality_pair_id,
        provider="claude",
        provider_version=baseline.provider_version,
        model=baseline.model,
        fixture_kind=baseline.fixture_kind,
    )
    if not authorization.allowed:
        raise ClaudeMeasurementError(f"quality-not-authorized:{authorization.reason_code}")
    if baseline.cache_tokens == 0:
        raise ClaudeMeasurementError("zero-baseline")
    reduction = Fraction(
        baseline.cache_tokens - guarded.cache_tokens, baseline.cache_tokens
    )
    return ClaudePairMeasurement(
        PAIR_SCHEMA,
        pair_id,
        baseline.quality_pair_id,
        baseline.fixture_kind,
        baseline.provider_version,
        baseline.model,
        execution_order,
        baseline.run_id,
        guarded.run_id,
        baseline.cache_tokens,
        guarded.cache_tokens,
        reduction.numerator,
        reduction.denominator,
    )


def qualify(
    repo_root: Path,
    pairs: Iterable[ClaudePairMeasurement],
    *,
    qualification_id: str,
) -> ClaudeQualification:
    qualification_id = _identifier(qualification_id, "qualification_id")
    values = tuple(pairs)
    if len(values) != 15 or len({pair.pair_id for pair in values}) != 15:
        raise ClaudeMeasurementError("qualification-requires-15-distinct-pairs")
    versions = {pair.provider_version for pair in values}
    models = {pair.model for pair in values}
    if len(versions) != 1 or len(models) != 1:
        raise ClaudeMeasurementError("qualification-provider-or-model-drift")
    provider_version = next(iter(versions))
    preflight = inventory.preflight("claude", provider_version, "cli")
    if preflight.status != "supported":
        raise ClaudeMeasurementError(preflight.reason_code)
    for index, pair in enumerate(values):
        expected_order = "baseline-first" if index % 2 == 0 else "guarded-first"
        if pair.execution_order != expected_order:
            raise ClaudeMeasurementError("execution-order-not-alternating")
        authorization = quality.QualityLedger(repo_root).authorize_measurement(
            pair.quality_pair_id,
            provider="claude",
            provider_version=pair.provider_version,
            model=pair.model,
            fixture_kind=pair.fixture_kind,
        )
        if not authorization.allowed:
            raise ClaudeMeasurementError(
                f"quality-not-authorized:{authorization.reason_code}"
            )
    grouped = {
        kind: tuple(pair for pair in values if pair.fixture_kind == kind)
        for kind in sorted(FIXTURE_KINDS)
    }
    if any(len(items) != 5 for items in grouped.values()):
        raise ClaudeMeasurementError("qualification-requires-five-pairs-per-fixture")
    reductions = tuple(pair.reduction for pair in values)
    provider_median = _median(reductions)
    q1 = sorted(reductions)[math.ceil(0.25 * len(reductions)) - 1]
    fixture_values = tuple(
        (kind, _median(tuple(pair.reduction for pair in items)))
        for kind, items in grouped.items()
    )
    reasons = []
    if provider_median < Fraction(3, 10):
        reasons.append("provider-median-below-30-percent")
    if q1 < 0:
        reasons.append("q1-negative")
    if any(value < 0 for _, value in fixture_values):
        reasons.append("fixture-median-negative")
    return ClaudeQualification(
        QUALIFICATION_SCHEMA,
        qualification_id,
        provider_version,
        next(iter(models)),
        not reasons,
        tuple(reasons) or ("claude-qualification-pass",),
        tuple(pair.pair_id for pair in values),
        provider_median.numerator,
        provider_median.denominator,
        q1.numerator,
        q1.denominator,
        tuple((kind, value.numerator, value.denominator) for kind, value in fixture_values),
    )


def _median(values: tuple[Fraction, ...]) -> Fraction:
    if not values:
        raise ClaudeMeasurementError("median requires observations")
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def _counter(value: Any, label: str) -> int:
    if type(value) is not int or value < 0:
        raise ClaudeMeasurementError(f"invalid-{label}-counter")
    return value


def _identifier(value: object, field: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise ClaudeMeasurementError(f"{field} is invalid")
    return value


def _exact_fields(value: Mapping[str, Any], fields: Iterable[str], label: str) -> None:
    if not isinstance(value, Mapping):
        raise ClaudeMeasurementError(f"{label} must be an object")
    expected = set(fields)
    unknown = sorted(set(value) - expected)
    missing = sorted(expected - set(value))
    if unknown or missing:
        detail = unknown if unknown else missing
        kind = "unknown" if unknown else "missing"
        raise ClaudeMeasurementError(f"{label} {kind} fields: {', '.join(detail)}")


def _validate_run(value: ClaudeRunMeasurement) -> None:
    for field in ("run_id", "quality_pair_id", "session_id"):
        _identifier(getattr(value, field), field)
    if value.schema != RUN_SCHEMA or value.fixture_kind not in FIXTURE_KINDS:
        raise ClaudeMeasurementError("Claude run identity is invalid")
    if inventory.preflight("claude", value.provider_version, "cli").status != "supported":
        raise ClaudeMeasurementError("Claude run version is invalid")
    if not isinstance(value.model, str) or not value.model:
        raise ClaudeMeasurementError("Claude run model is invalid")
    if value.role not in {"baseline", "guarded"} or value.status != "measurable":
        raise ClaudeMeasurementError("Claude run state is invalid")
    if (
        not isinstance(value.source_fingerprint, str)
        or not re.fullmatch(r"[0-9a-f]{64}", value.source_fingerprint)
    ):
        raise ClaudeMeasurementError("source_fingerprint is invalid")
    counters = (
        value.eligible_rows,
        value.duplicate_rows,
        value.cache_creation_tokens,
        value.cache_read_tokens,
        value.cache_tokens,
    )
    if any(type(item) is not int or item < 0 for item in counters):
        raise ClaudeMeasurementError("Claude run counters are invalid")
    if value.eligible_rows <= value.duplicate_rows:
        raise ClaudeMeasurementError("Claude run row counts are invalid")
    if value.cache_tokens != value.cache_creation_tokens + value.cache_read_tokens:
        raise ClaudeMeasurementError("Claude run total is invalid")


def _validate_pair(value: ClaudePairMeasurement) -> None:
    for field in ("pair_id", "quality_pair_id", "baseline_run_id", "guarded_run_id"):
        _identifier(getattr(value, field), field)
    if value.schema != PAIR_SCHEMA or value.fixture_kind not in FIXTURE_KINDS:
        raise ClaudeMeasurementError("Claude pair identity is invalid")
    if inventory.preflight("claude", value.provider_version, "cli").status != "supported":
        raise ClaudeMeasurementError("Claude pair version is invalid")
    if not isinstance(value.model, str) or not value.model:
        raise ClaudeMeasurementError("Claude pair model is invalid")
    if value.execution_order not in {"baseline-first", "guarded-first"}:
        raise ClaudeMeasurementError("Claude pair execution order is invalid")
    if (
        type(value.baseline_cache_tokens) is not int
        or value.baseline_cache_tokens <= 0
        or type(value.guarded_cache_tokens) is not int
        or value.guarded_cache_tokens < 0
        or type(value.reduction_numerator) is not int
        or type(value.reduction_denominator) is not int
        or value.reduction_denominator <= 0
    ):
        raise ClaudeMeasurementError("Claude pair counters are invalid")
    expected = Fraction(
        value.baseline_cache_tokens - value.guarded_cache_tokens,
        value.baseline_cache_tokens,
    )
    if expected != value.reduction:
        raise ClaudeMeasurementError("Claude pair reduction is invalid")


def _validate_qualification(value: ClaudeQualification) -> None:
    _identifier(value.qualification_id, "qualification_id")
    if value.schema != QUALIFICATION_SCHEMA or type(value.passed) is not bool:
        raise ClaudeMeasurementError("Claude qualification schema is invalid")
    if inventory.preflight("claude", value.provider_version, "cli").status != "supported":
        raise ClaudeMeasurementError("Claude qualification version is invalid")
    if not isinstance(value.model, str) or not value.model:
        raise ClaudeMeasurementError("Claude qualification model is invalid")
    if len(value.pair_ids) != 15 or len(set(value.pair_ids)) != 15:
        raise ClaudeMeasurementError("Claude qualification pair population is invalid")
    if any(not isinstance(item, str) or not item for item in value.reason_codes):
        raise ClaudeMeasurementError("Claude qualification reasons are invalid")
    for pair_id in value.pair_ids:
        _identifier(pair_id, "pair_id")
    fractions = (
        (value.provider_median_numerator, value.provider_median_denominator),
        (value.q1_numerator, value.q1_denominator),
        *((item[1], item[2]) for item in value.fixture_medians),
    )
    if any(
        type(numerator) is not int
        or type(denominator) is not int
        or denominator <= 0
        for numerator, denominator in fractions
    ):
        raise ClaudeMeasurementError("Claude qualification statistics are invalid")
    if {item[0] for item in value.fixture_medians} != FIXTURE_KINDS:
        raise ClaudeMeasurementError("Claude qualification fixture population is invalid")


def _validate_record(value: object) -> None:
    if not isinstance(value, Mapping):
        raise ClaudeMeasurementError("measurement ledger record must be an object")
    _exact_fields(
        value,
        ("schema", "event", "timestamp", "identifier", "evidence"),
        "measurement ledger record",
    )
    if value["schema"] != LEDGER_SCHEMA or value["event"] not in {
        "run",
        "pair",
        "qualification",
    }:
        raise ClaudeMeasurementError("measurement ledger record is invalid")
    _identifier(value["identifier"], "identifier")
    if not isinstance(value["timestamp"], str) or not isinstance(value["evidence"], Mapping):
        raise ClaudeMeasurementError("measurement ledger evidence is invalid")
    if value["event"] == "run":
        ClaudeRunMeasurement.from_dict(value["evidence"])
    elif value["event"] == "pair":
        ClaudePairMeasurement.from_dict(value["evidence"])
    else:
        ClaudeQualification.from_dict(value["evidence"])


def _append_record_unlocked(
    root: Path, path: Path, record: Mapping[str, Any]
) -> None:
    encoded = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    with os.fdopen(fd, "ab", closefd=True) as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(path, 0o600)
    _fsync_dir(root)


@contextlib.contextmanager
def _writer_lock(root: Path, lock_path: Path) -> Iterator[None]:
    if root.parent.is_symlink() or root.is_symlink():
        raise ClaudeMeasurementError("private storage path must not be a symlink")
    root.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    if root.parent.is_symlink() or root.is_symlink():
        raise ClaudeMeasurementError("private storage path must not be a symlink")
    os.chmod(root.parent, 0o700)
    os.chmod(root, 0o700)
    fd = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
    os.fchmod(fd, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ClaudeMeasurementBusyError("measurement ledger writer is busy") from exc
        yield
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
