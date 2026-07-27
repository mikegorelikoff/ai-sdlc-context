from __future__ import annotations

import json
import stat
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from context_guard import claude_measurement as measurement
from context_guard import quality, receipts


def _authorize(repo: Path, pair_id: str = "quality-pair") -> None:
    manifest = quality.QualityManifest.from_dict(
        {
            "schema": quality.MANIFEST_SCHEMA,
            "fixture_id": "fixture",
            "fixture_kind": "read-only-analysis",
            "provider": "claude",
            "provider_version": "2.1.218",
            "model": "claude-test",
            "repository_fingerprint": "repo",
            "task_fingerprint": "task",
            "baseline_profile_fingerprint": "baseline",
            "guarded_profile_fingerprint": "guarded",
            "required_instruction_ids": ["REQ-1"],
        }
    )

    def attempt(role: str):
        return quality.AttemptEvidence.from_dict(
            {
                "schema": quality.ATTEMPT_SCHEMA,
                "attempt_id": f"{pair_id}-{role}",
                "pair_id": pair_id,
                "role": role,
                "fixture_id": "fixture",
                "provider": "claude",
                "provider_version": "2.1.218",
                "model": "claude-test",
                "repository_fingerprint": "repo",
                "task_fingerprint": "task",
                "profile_fingerprint": role,
                "fresh_session": True,
                "completion_passed": True,
                "observed_instruction_ids": ["REQ-1"],
                "explicit_skill_invoked": True,
                "restoration_passed": True,
                "receipt_ref": f"{role}-receipt",
                "receipt_valid": True,
                "privacy_passed": True,
            }
        )

    quality.QualityLedger(repo).record_evaluation(
        manifest, attempt("baseline"), attempt("guarded"), run_id=f"q-{pair_id}"
    )


def _row(
    request_id: str,
    message_id: str,
    creation: int = 10,
    read: int = 20,
    **overrides,
):
    row = {
        "type": "assistant",
        "sessionId": "session-1",
        "requestId": request_id,
        "message": {
            "id": message_id,
            "model": "claude-test",
            "usage": {
                "cache_creation_input_tokens": creation,
                "cache_read_input_tokens": read,
            },
            "content": [{"type": "text", "text": "must never persist"}],
        },
    }
    row.update(overrides)
    return row


def _write_jsonl(path: Path, rows: list[object]) -> Path:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    return path


def _extract(repo: Path, source: Path, run_id: str = "run-baseline", **overrides):
    values = {
        "run_id": run_id,
        "quality_pair_id": "quality-pair",
        "fixture_kind": "read-only-analysis",
        "role": "baseline",
        "provider_version": "2.1.218",
        "model": "claude-test",
        "session_id": "session-1",
    }
    values.update(overrides)
    return measurement.extract_run(repo, source, **values)


def test_extract_deduplicates_identical_rows_and_persists_only_minimized_evidence(
    tmp_path: Path,
):
    _authorize(tmp_path)
    source = _write_jsonl(
        tmp_path / "session.jsonl",
        [_row("r1", "m1"), _row("r1", "m1"), _row("r2", "m2", 5, 7)],
    )
    result = _extract(tmp_path, source)
    ledger = measurement.MeasurementLedger(tmp_path)
    ledger.record_run(result)

    assert result.eligible_rows == 3
    assert result.duplicate_rows == 1
    assert result.cache_creation_tokens == 15
    assert result.cache_read_tokens == 27
    assert result.cache_tokens == 42
    assert stat.S_IMODE(ledger.root.stat().st_mode) == 0o700
    assert stat.S_IMODE(ledger.path.stat().st_mode) == 0o600
    serialized = ledger.path.read_text(encoding="utf-8")
    assert "must never persist" not in serialized
    assert str(source) not in serialized
    receipt = receipts.inspect_receipt(tmp_path, "run-baseline")
    assert receipt["measurement_ref"] == "run-baseline"


@pytest.mark.parametrize(
    ("rows", "reason"),
    [
        ([_row("r1", "m1"), _row("r1", "m1", 11, 20)], "inconsistent-duplicate"),
        ([_row("r1", "m1", creation=-1)], "invalid-cache-creation-counter"),
        ([_row("r1", "m1", read=True)], "invalid-cache-read-counter"),
        ([_row("r1", "m1", sessionId="other")], "empty-measurement-window"),
    ],
)
def test_extract_rejects_ambiguous_or_malformed_windows(
    tmp_path: Path, rows: list[object], reason: str
):
    _authorize(tmp_path)
    source = _write_jsonl(tmp_path / "bad.jsonl", rows)

    with pytest.raises(measurement.ClaudeMeasurementError, match=reason):
        _extract(tmp_path, source)


def test_quality_denial_happens_before_source_access(tmp_path: Path):
    with pytest.raises(measurement.ClaudeMeasurementError, match="quality-not-authorized"):
        _extract(tmp_path, tmp_path / "does-not-exist.jsonl")


def test_quality_context_must_match_declared_measurement(tmp_path: Path):
    _authorize(tmp_path)
    source = _write_jsonl(tmp_path / "session.jsonl", [_row("r1", "m1")])

    with pytest.raises(measurement.ClaudeMeasurementError, match="quality-context-mismatch"):
        _extract(tmp_path, source, fixture_kind="test-only-change")


def test_compare_pair_retains_exact_negative_reduction_and_rechecks_quality(
    tmp_path: Path,
):
    _authorize(tmp_path)
    source = _write_jsonl(tmp_path / "session.jsonl", [_row("r1", "m1")])
    baseline = _extract(tmp_path, source)
    guarded = replace(
        baseline,
        run_id="run-guarded",
        role="guarded",
        cache_creation_tokens=20,
        cache_read_tokens=25,
        cache_tokens=45,
    )

    pair = measurement.compare_pair(
        tmp_path, baseline, guarded, pair_id="pair-1", execution_order="baseline-first"
    )

    assert pair.reduction == Fraction(-1, 2)
    measurement.MeasurementLedger(tmp_path).record_pair(pair)
    assert receipts.inspect_receipt(tmp_path, "pair-1")["quality_ref"] == "quality-pair"
    quality.QualityLedger(tmp_path).invalidate(
        "quality-pair", run_id="revoke", reason_code="qa-revoked"
    )
    with pytest.raises(measurement.ClaudeMeasurementError, match="qa-revoked"):
        measurement.compare_pair(
            tmp_path, baseline, guarded, pair_id="pair-2", execution_order="guarded-first"
        )


def _pair(index: int, kind: str, reduction: Fraction = Fraction(2, 5)):
    baseline = 100
    guarded = baseline - int(reduction * baseline)
    exact = Fraction(baseline - guarded, baseline)
    return measurement.ClaudePairMeasurement(
        measurement.PAIR_SCHEMA,
        f"pair-{index}",
        f"quality-{index}",
        kind,
        "2.1.218",
        "claude-test",
        "baseline-first" if index % 2 == 0 else "guarded-first",
        f"baseline-{index}",
        f"guarded-{index}",
        baseline,
        guarded,
        exact.numerator,
        exact.denominator,
    )


def _population(reductions: list[Fraction] | None = None):
    kinds = sorted(measurement.FIXTURE_KINDS)
    values = []
    for index in range(15):
        reduction = reductions[index] if reductions else Fraction(2, 5)
        values.append(_pair(index, kinds[index // 5], reduction))
    return values


def test_qualification_uses_exact_median_q1_and_fixture_gates(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(
        quality.QualityLedger,
        "authorize_measurement",
        lambda self, pair_id, **kwargs: quality.Authorization(pair_id, True, "pass"),
    )
    result = measurement.qualify(
        tmp_path, _population(), qualification_id="qualification-pass"
    )

    assert result.passed is True
    assert Fraction(
        result.provider_median_numerator, result.provider_median_denominator
    ) == Fraction(2, 5)
    assert Fraction(result.q1_numerator, result.q1_denominator) == Fraction(2, 5)
    assert all(Fraction(n, d) == Fraction(2, 5) for _, n, d in result.fixture_medians)

    reductions = [Fraction(-1, 10)] * 5 + [Fraction(2, 5)] * 10
    failed = measurement.qualify(
        tmp_path, _population(reductions), qualification_id="qualification-fail"
    )
    assert failed.passed is False
    assert "q1-negative" in failed.reason_codes
    assert "fixture-median-negative" in failed.reason_codes

    ledger = measurement.MeasurementLedger(tmp_path)
    ledger.record_qualification(result)
    assert ledger.records()[0]["evidence"] == result.to_dict()
    with pytest.raises(measurement.ClaudeMeasurementError, match="already exists"):
        ledger.record_qualification(result)


def test_qualification_rejects_incomplete_duplicate_and_non_alternating_populations(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setattr(
        quality.QualityLedger,
        "authorize_measurement",
        lambda self, pair_id, **kwargs: quality.Authorization(pair_id, True, "pass"),
    )
    values = _population()
    with pytest.raises(measurement.ClaudeMeasurementError, match="15-distinct"):
        measurement.qualify(tmp_path, values[:-1], qualification_id="incomplete")
    values[1] = replace(values[1], execution_order="baseline-first")
    with pytest.raises(measurement.ClaudeMeasurementError, match="not-alternating"):
        measurement.qualify(tmp_path, values, qualification_id="order")


def test_measurement_receipt_failure_leaves_no_ledger_evidence(
    tmp_path: Path, monkeypatch
):
    _authorize(tmp_path)
    source = _write_jsonl(tmp_path / "session.jsonl", [_row("r1", "m1")])
    result = _extract(tmp_path, source)
    ledger = measurement.MeasurementLedger(tmp_path)
    monkeypatch.setattr(
        receipts,
        "write_receipt",
        lambda *args, **kwargs: (_ for _ in ()).throw(receipts.ReceiptError("failed")),
    )

    with pytest.raises(receipts.ReceiptError):
        ledger.record_run(result)

    assert not ledger.path.exists()


def test_exact_input_schemas_reject_prohibited_fields(tmp_path: Path):
    _authorize(tmp_path)
    source = _write_jsonl(tmp_path / "session.jsonl", [_row("r1", "m1")])
    value = _extract(tmp_path, source).to_dict()
    value["prompt"] = "forbidden"

    with pytest.raises(measurement.ClaudeMeasurementError, match="unknown fields"):
        measurement.ClaudeRunMeasurement.from_dict(value)
