"""Read-only Codex cached-input measurement and exact paired statistics."""

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


RUN_SCHEMA = "context-guard-codex-run-measurement/v1"
PAIR_SCHEMA = "context-guard-codex-pair-measurement/v1"
QUALIFICATION_SCHEMA = "context-guard-codex-qualification/v1"
LEDGER_SCHEMA = "context-guard-codex-measurement-ledger/v1"
MEASUREMENT_RELATIVE = Path(".context-guard") / "measurements-codex"
FIXTURE_KINDS = quality.FIXTURE_KINDS
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")


class CodexMeasurementError(ValueError):
    code = "CODEX_MEASUREMENT_INVALID"

    def __str__(self) -> str:
        return f"{self.code}: {super().__str__()}"


@dataclass(frozen=True)
class CodexRunMeasurement:
    schema: str
    run_id: str
    quality_pair_id: str
    fixture_kind: str
    role: str
    provider_version: str
    model: str
    thread_id: str
    measurement_mode: str
    boundary_ref: str
    status: str
    reason_code: str
    source_fingerprint: str | None
    cached_input_tokens: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "CodexRunMeasurement":
        _exact_fields(value, tuple(cls.__dataclass_fields__), "Codex run")
        result = cls(**value)
        _validate_run(result)
        return result


@dataclass(frozen=True)
class CodexPairMeasurement:
    schema: str
    pair_id: str
    quality_pair_id: str
    fixture_kind: str
    provider_version: str
    model: str
    execution_order: str
    baseline_run_id: str
    guarded_run_id: str
    baseline_cached_input_tokens: int
    guarded_cached_input_tokens: int
    reduction_numerator: int
    reduction_denominator: int

    @property
    def reduction(self) -> Fraction:
        return Fraction(self.reduction_numerator, self.reduction_denominator)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "CodexPairMeasurement":
        _exact_fields(value, tuple(cls.__dataclass_fields__), "Codex pair")
        result = cls(**value)
        _validate_pair(result)
        return result


@dataclass(frozen=True)
class CodexQualification:
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
    def from_dict(cls, value: Mapping[str, Any]) -> "CodexQualification":
        _exact_fields(value, tuple(cls.__dataclass_fields__), "Codex qualification")
        medians = value["fixture_medians"]
        if (
            not isinstance(medians, list)
            or not isinstance(value["reason_codes"], list)
            or not isinstance(value["pair_ids"], list)
        ):
            raise CodexMeasurementError("qualification collections must be lists")
        normalized = []
        for item in medians:
            _exact_fields(item, ("fixture_kind", "numerator", "denominator"), "fixture median")
            normalized.append((item["fixture_kind"], item["numerator"], item["denominator"]))
        result = cls(
            value["schema"], value["qualification_id"], value["provider_version"],
            value["model"], value["passed"], tuple(value["reason_codes"]),
            tuple(value["pair_ids"]), value["provider_median_numerator"],
            value["provider_median_denominator"], value["q1_numerator"],
            value["q1_denominator"], tuple(normalized)
        )
        _validate_qualification(result)
        return result


class MeasurementLedger:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.root = self.repo_root / MEASUREMENT_RELATIVE
        self.path = self.root / "ledger.jsonl"
        self.lock_path = self.root / ".writer.lock"

    def record_run(self, value: CodexRunMeasurement) -> None:
        _validate_run(value)
        self._record("run", value.run_id, value.to_dict(), value.provider_version,
                     value.quality_pair_id, True)

    def record_pair(self, value: CodexPairMeasurement) -> None:
        _validate_pair(value)
        self._record("pair", value.pair_id, value.to_dict(), value.provider_version,
                     value.quality_pair_id, True)

    def record_qualification(self, value: CodexQualification) -> None:
        _validate_qualification(value)
        self._record("qualification", value.qualification_id, value.to_dict(),
                     value.provider_version, None, value.passed)

    def _record(
        self,
        event: str,
        identifier: str,
        evidence: Mapping[str, Any],
        version: str,
        quality_ref: str | None,
        passed: bool,
    ) -> None:
        record = {
            "schema": LEDGER_SCHEMA,
            "event": event,
            "timestamp": _now(),
            "identifier": _identifier(identifier, "measurement identifier"),
            "evidence": dict(evidence),
        }
        payload: dict[str, Any] = {
            "schema": receipts.SCHEMA,
            "run_id": identifier,
            "timestamp": _now(),
            "provider": "codex",
            "provider_version": version,
            "surface": "codex-measurement",
            "status": "valid" if passed else "invalid",
            "completed": True,
            "referenced": True,
            "measurement_ref": identifier,
            "reason_codes": [f"codex-{event}-recorded"],
            "classifications": ["native-cached-input-tokens"],
            "requested_action": f"codex-{event}",
            "actual_action": f"codex-{event}-{'pass' if passed else 'fail'}",
        }
        if quality_ref:
            payload["quality_ref"] = quality_ref
        with _writer_lock(self.root, self.lock_path):
            if any(item["identifier"] == identifier for item in self.records()):
                raise CodexMeasurementError(f"measurement evidence already exists for {identifier}")
            receipts.write_receipt(self.repo_root, payload)
            _append(self.root, self.path, record)

    def records(self) -> tuple[dict[str, Any], ...]:
        if not self.path.is_file():
            return ()
        result = []
        try:
            for line in self.path.read_text(encoding="utf-8").splitlines():
                item = json.loads(line)
                if (
                    not isinstance(item, dict)
                    or item.get("schema") != LEDGER_SCHEMA
                    or set(item) != {"schema", "event", "timestamp", "identifier", "evidence"}
                ):
                    raise CodexMeasurementError("corrupt-measurement-ledger")
                _identifier(item["identifier"], "identifier")
                if not isinstance(item["timestamp"], str):
                    raise CodexMeasurementError("corrupt-measurement-ledger")
                evidence = item["evidence"]
                if item["event"] == "run":
                    CodexRunMeasurement.from_dict(evidence)
                elif item["event"] == "pair":
                    CodexPairMeasurement.from_dict(evidence)
                elif item["event"] == "qualification":
                    CodexQualification.from_dict(evidence)
                else:
                    raise CodexMeasurementError("corrupt-measurement-ledger")
                result.append(item)
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            raise CodexMeasurementError("corrupt-measurement-ledger") from exc
        return tuple(result)


def extract_exact_run(
    repo_root: Path,
    source: Path,
    *,
    run_id: str,
    quality_pair_id: str,
    fixture_kind: str,
    role: str,
    provider_version: str,
    model: str,
    thread_id: str,
) -> CodexRunMeasurement:
    """Extract exactly one Codex exec turn.completed event from one explicit file."""
    _validate_context(
        repo_root, run_id, quality_pair_id, fixture_kind, role,
        provider_version, model, thread_id
    )
    if not Path(source).is_file():
        raise CodexMeasurementError("source-not-file")
    digest = hashlib.sha256()
    started = []
    completed = []
    try:
        with Path(source).open("rb") as handle:
            for raw in handle:
                digest.update(raw)
                try:
                    row = json.loads(raw)
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise CodexMeasurementError("malformed-jsonl") from exc
                if not isinstance(row, dict):
                    raise CodexMeasurementError("invalid-event")
                if row.get("type") == "thread.started":
                    started.append(row)
                elif row.get("type") == "turn.completed":
                    completed.append(row)
    except OSError as exc:
        raise CodexMeasurementError("source-read-error") from exc
    if len(started) != 1 or started[0].get("thread_id") != thread_id:
        raise CodexMeasurementError("thread-correlation-mismatch")
    if len(completed) != 1:
        raise CodexMeasurementError("exactly-one-turn-completed-required")
    usage = completed[0].get("usage")
    if not isinstance(usage, dict):
        raise CodexMeasurementError("missing-usage")
    cached = _counter(usage.get("cached_input_tokens"), "cached-input")
    return CodexRunMeasurement(
        RUN_SCHEMA, run_id, quality_pair_id, fixture_kind, role, provider_version,
        model, thread_id, "exact-event", f"thread:{thread_id}", "measurable",
        "codex-turn-completed-valid", digest.hexdigest(), cached
    )


def measure_cumulative_run(
    repo_root: Path,
    *,
    run_id: str,
    quality_pair_id: str,
    fixture_kind: str,
    role: str,
    provider_version: str,
    model: str,
    thread_id: str,
    start_boundary_id: str,
    end_boundary_id: str,
    start_cached_input_tokens: int,
    end_cached_input_tokens: int,
) -> CodexRunMeasurement:
    """Measure one declared monotonic cumulative cached-input interval."""
    _validate_context(
        repo_root, run_id, quality_pair_id, fixture_kind, role,
        provider_version, model, thread_id
    )
    start = _counter(start_cached_input_tokens, "start-cached-input")
    end = _counter(end_cached_input_tokens, "end-cached-input")
    start_id = _identifier(start_boundary_id, "start_boundary_id")
    end_id = _identifier(end_boundary_id, "end_boundary_id")
    if start_id == end_id:
        raise CodexMeasurementError("boundary-identifiers-must-differ")
    if end < start:
        raise CodexMeasurementError("non-monotonic-cumulative-counter")
    return CodexRunMeasurement(
        RUN_SCHEMA, run_id, quality_pair_id, fixture_kind, role, provider_version,
        model, thread_id, "cumulative-boundary", f"{start_id}:{end_id}",
        "measurable", "codex-cumulative-window-valid", None, end - start
    )


def compare_pair(
    repo_root: Path,
    baseline: CodexRunMeasurement,
    guarded: CodexRunMeasurement,
    *,
    pair_id: str,
    execution_order: str,
) -> CodexPairMeasurement:
    _validate_run(baseline)
    _validate_run(guarded)
    pair_id = _identifier(pair_id, "pair_id")
    if execution_order not in {"baseline-first", "guarded-first"}:
        raise CodexMeasurementError("execution_order is invalid")
    if (
        baseline.role != "baseline"
        or guarded.role != "guarded"
        or baseline.quality_pair_id != guarded.quality_pair_id
        or baseline.fixture_kind != guarded.fixture_kind
        or baseline.provider_version != guarded.provider_version
        or baseline.model != guarded.model
        or baseline.run_id == guarded.run_id
    ):
        raise CodexMeasurementError("pair-correlation-mismatch")
    _authorize(
        repo_root, baseline.quality_pair_id, baseline.fixture_kind,
        baseline.provider_version, baseline.model
    )
    if baseline.cached_input_tokens == 0:
        raise CodexMeasurementError("zero-baseline")
    reduction = Fraction(
        baseline.cached_input_tokens - guarded.cached_input_tokens,
        baseline.cached_input_tokens,
    )
    return CodexPairMeasurement(
        PAIR_SCHEMA, pair_id, baseline.quality_pair_id, baseline.fixture_kind,
        baseline.provider_version, baseline.model, execution_order, baseline.run_id,
        guarded.run_id, baseline.cached_input_tokens, guarded.cached_input_tokens,
        reduction.numerator, reduction.denominator
    )


def qualify(
    repo_root: Path,
    pairs: Iterable[CodexPairMeasurement],
    *,
    qualification_id: str,
) -> CodexQualification:
    qualification_id = _identifier(qualification_id, "qualification_id")
    values = tuple(pairs)
    if len(values) != 15 or len({item.pair_id for item in values}) != 15:
        raise CodexMeasurementError("qualification-requires-15-distinct-pairs")
    versions = {item.provider_version for item in values}
    models = {item.model for item in values}
    if len(versions) != 1 or len(models) != 1:
        raise CodexMeasurementError("qualification-provider-or-model-drift")
    version = next(iter(versions))
    if inventory.preflight("codex", version, "cli").status != "supported":
        raise CodexMeasurementError("unsupported-version")
    for index, item in enumerate(values):
        _validate_pair(item)
        expected = "baseline-first" if index % 2 == 0 else "guarded-first"
        if item.execution_order != expected:
            raise CodexMeasurementError("execution-order-not-alternating")
        _authorize(
            repo_root, item.quality_pair_id, item.fixture_kind,
            item.provider_version, item.model
        )
    grouped = {
        kind: tuple(item for item in values if item.fixture_kind == kind)
        for kind in sorted(FIXTURE_KINDS)
    }
    if any(len(items) != 5 for items in grouped.values()):
        raise CodexMeasurementError("qualification-requires-five-pairs-per-fixture")
    reductions = tuple(item.reduction for item in values)
    provider_median = _median(reductions)
    q1 = sorted(reductions)[math.ceil(0.25 * len(reductions)) - 1]
    fixture_medians = tuple(
        (kind, _median(tuple(item.reduction for item in items)))
        for kind, items in grouped.items()
    )
    reasons = []
    if provider_median < Fraction(3, 10):
        reasons.append("provider-median-below-30-percent")
    if q1 < 0:
        reasons.append("q1-negative")
    if any(value < 0 for _, value in fixture_medians):
        reasons.append("fixture-median-negative")
    return CodexQualification(
        QUALIFICATION_SCHEMA, qualification_id, version, next(iter(models)),
        not reasons, tuple(reasons) or ("codex-qualification-pass",),
        tuple(item.pair_id for item in values), provider_median.numerator,
        provider_median.denominator, q1.numerator, q1.denominator,
        tuple((kind, value.numerator, value.denominator)
              for kind, value in fixture_medians)
    )


def _validate_context(
    repo_root: Path,
    run_id: str,
    quality_pair_id: str,
    fixture_kind: str,
    role: str,
    version: str,
    model: str,
    thread_id: str,
) -> None:
    _identifier(run_id, "run_id")
    _identifier(quality_pair_id, "quality_pair_id")
    _identifier(thread_id, "thread_id")
    if fixture_kind not in FIXTURE_KINDS:
        raise CodexMeasurementError("fixture_kind is unsupported")
    if role not in {"baseline", "guarded"}:
        raise CodexMeasurementError("role must be baseline or guarded")
    if not isinstance(model, str) or not model or len(model) > 256:
        raise CodexMeasurementError("model is invalid")
    preflight = inventory.preflight("codex", version, "cli")
    if preflight.status != "supported":
        raise CodexMeasurementError(preflight.reason_code)
    _authorize(repo_root, quality_pair_id, fixture_kind, version, model)


def _authorize(repo: Path, pair: str, fixture: str, version: str, model: str) -> None:
    authorization = quality.QualityLedger(repo).authorize_measurement(
        pair, provider="codex", provider_version=version,
        model=model, fixture_kind=fixture
    )
    if not authorization.allowed:
        raise CodexMeasurementError(
            f"quality-not-authorized:{authorization.reason_code}"
        )


def _validate_run(value: CodexRunMeasurement) -> None:
    if value.schema != RUN_SCHEMA:
        raise CodexMeasurementError("Codex run schema is invalid")
    for item, field in (
        (value.run_id, "run_id"),
        (value.quality_pair_id, "quality_pair_id"),
        (value.thread_id, "thread_id"),
    ):
        _identifier(item, field)
    if value.fixture_kind not in FIXTURE_KINDS or value.role not in {"baseline", "guarded"}:
        raise CodexMeasurementError("Codex run correlation is invalid")
    if inventory.preflight("codex", value.provider_version, "cli").status != "supported":
        raise CodexMeasurementError("Codex run version is invalid")
    if not isinstance(value.model, str) or not value.model or len(value.model) > 256:
        raise CodexMeasurementError("Codex run model is invalid")
    if value.measurement_mode not in {"exact-event", "cumulative-boundary"}:
        raise CodexMeasurementError("measurement_mode is invalid")
    if not isinstance(value.boundary_ref, str) or not value.boundary_ref:
        raise CodexMeasurementError("boundary_ref is invalid")
    if (
        value.measurement_mode == "exact-event"
        and (
            not isinstance(value.source_fingerprint, str)
            or not re.fullmatch(r"[0-9a-f]{64}", value.source_fingerprint)
        )
    ):
        raise CodexMeasurementError("source_fingerprint is invalid")
    if value.measurement_mode == "cumulative-boundary" and value.source_fingerprint is not None:
        raise CodexMeasurementError("cumulative source_fingerprint must be null")
    _counter(value.cached_input_tokens, "cached-input")
    if (
        value.status != "measurable"
        or not isinstance(value.reason_code, str)
        or not value.reason_code
    ):
        raise CodexMeasurementError("Codex run is not measurable")


def _validate_pair(value: CodexPairMeasurement) -> None:
    if value.schema != PAIR_SCHEMA:
        raise CodexMeasurementError("Codex pair schema is invalid")
    for item, field in (
        (value.pair_id, "pair_id"),
        (value.quality_pair_id, "quality_pair_id"),
        (value.baseline_run_id, "baseline_run_id"),
        (value.guarded_run_id, "guarded_run_id"),
    ):
        _identifier(item, field)
    if value.fixture_kind not in FIXTURE_KINDS:
        raise CodexMeasurementError("pair fixture is invalid")
    if inventory.preflight("codex", value.provider_version, "cli").status != "supported":
        raise CodexMeasurementError("Codex pair version is invalid")
    if not isinstance(value.model, str) or not value.model or len(value.model) > 256:
        raise CodexMeasurementError("Codex pair model is invalid")
    if value.execution_order not in {"baseline-first", "guarded-first"}:
        raise CodexMeasurementError("pair execution order is invalid")
    _counter(value.baseline_cached_input_tokens, "baseline-cached-input")
    _counter(value.guarded_cached_input_tokens, "guarded-cached-input")
    if (
        type(value.reduction_numerator) is not int
        or type(value.reduction_denominator) is not int
        or value.reduction_denominator <= 0
    ):
        raise CodexMeasurementError("pair reduction is invalid")
    expected = Fraction(
        value.baseline_cached_input_tokens - value.guarded_cached_input_tokens,
        value.baseline_cached_input_tokens,
    ) if value.baseline_cached_input_tokens else None
    if expected is None or expected != value.reduction:
        raise CodexMeasurementError("pair reduction mismatch")


def _validate_qualification(value: CodexQualification) -> None:
    if value.schema != QUALIFICATION_SCHEMA:
        raise CodexMeasurementError("qualification schema is invalid")
    _identifier(value.qualification_id, "qualification_id")
    if inventory.preflight("codex", value.provider_version, "cli").status != "supported":
        raise CodexMeasurementError("qualification version is invalid")
    if not isinstance(value.model, str) or not value.model or len(value.model) > 256:
        raise CodexMeasurementError("qualification model is invalid")
    if (
        type(value.passed) is not bool
        or len(value.pair_ids) != 15
        or len(set(value.pair_ids)) != 15
    ):
        raise CodexMeasurementError("qualification evidence is invalid")
    if any(not isinstance(reason, str) or not reason for reason in value.reason_codes):
        raise CodexMeasurementError("qualification reasons are invalid")
    for pair_id in value.pair_ids:
        _identifier(pair_id, "pair_id")
    if {item[0] for item in value.fixture_medians} != FIXTURE_KINDS:
        raise CodexMeasurementError("qualification fixtures are invalid")
    for numerator, denominator in (
        (value.provider_median_numerator, value.provider_median_denominator),
        (value.q1_numerator, value.q1_denominator),
        *((item[1], item[2]) for item in value.fixture_medians)
    ):
        if (
            type(numerator) is not int
            or type(denominator) is not int
            or denominator <= 0
        ):
            raise CodexMeasurementError("qualification denominator is invalid")


def _median(values: tuple[Fraction, ...]) -> Fraction:
    ordered = sorted(values)
    if not ordered:
        raise CodexMeasurementError("median requires observations")
    middle = len(ordered) // 2
    return ordered[middle] if len(ordered) % 2 else (
        ordered[middle - 1] + ordered[middle]
    ) / 2


def _counter(value: object, label: str) -> int:
    if type(value) is not int or value < 0:
        raise CodexMeasurementError(f"invalid-{label}-counter")
    return value


def _identifier(value: object, field: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise CodexMeasurementError(f"{field} is invalid")
    return value


def _exact_fields(value: Mapping[str, Any], fields: Iterable[str], label: str) -> None:
    if not isinstance(value, Mapping) or set(value) != set(fields):
        raise CodexMeasurementError(f"{label} has unknown or missing fields")


@contextlib.contextmanager
def _writer_lock(root: Path, path: Path) -> Iterator[None]:
    if root.parent.is_symlink() or root.is_symlink():
        raise CodexMeasurementError("private storage path must not be a symlink")
    root.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    if root.parent.is_symlink() or root.is_symlink():
        raise CodexMeasurementError("private storage path must not be a symlink")
    os.chmod(root.parent, 0o700)
    os.chmod(root, 0o700)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    os.fchmod(fd, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise CodexMeasurementError("measurement-ledger-busy") from exc
        yield
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


def _append(root: Path, path: Path, value: Mapping[str, Any]) -> None:
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    with os.fdopen(fd, "ab") as handle:
        handle.write((json.dumps(value, sort_keys=True) + "\n").encode("utf-8"))
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(path, 0o600)
    directory = os.open(root, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
