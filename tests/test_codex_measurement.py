from __future__ import annotations

import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from context_guard import codex_measurement as measurement
from context_guard import quality, receipts


def _authorize(repo: Path, pair_id: str = "quality-pair") -> None:
    manifest = quality.QualityManifest.from_dict(
        {
            "schema": quality.MANIFEST_SCHEMA,
            "fixture_id": "fixture",
            "fixture_kind": "read-only-analysis",
            "provider": "codex",
            "provider_version": "0.144.1",
            "model": "gpt-test",
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
                "provider": "codex",
                "provider_version": "0.144.1",
                "model": "gpt-test",
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


def _context(repo: Path, **overrides):
    values = {
        "run_id": "run-baseline",
        "quality_pair_id": "quality-pair",
        "fixture_kind": "read-only-analysis",
        "role": "baseline",
        "provider_version": "0.144.1",
        "model": "gpt-test",
        "thread_id": "thread-1",
    }
    values.update(overrides)
    return values


def _jsonl(path: Path, rows: list[object]) -> Path:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    return path


def test_exact_event_extracts_only_cached_input_and_persists_minimized_evidence(
    tmp_path: Path,
):
    _authorize(tmp_path)
    source = _jsonl(
        tmp_path / "exec.jsonl",
        [
            {"type": "thread.started", "thread_id": "thread-1"},
            {"type": "item.completed", "item": {"text": "never persist"}},
            {
                "type": "turn.completed",
                "usage": {
                    "input_tokens": 200,
                    "cached_input_tokens": 120,
                    "output_tokens": 10,
                },
            },
        ],
    )
    result = measurement.extract_exact_run(tmp_path, source, **_context(tmp_path))
    ledger = measurement.MeasurementLedger(tmp_path)
    ledger.record_run(result)

    assert result.cached_input_tokens == 120
    assert result.measurement_mode == "exact-event"
    serialized = ledger.path.read_text(encoding="utf-8")
    assert "never persist" not in serialized
    assert str(source) not in serialized
    assert receipts.inspect_receipt(tmp_path, "run-baseline")["provider"] == "codex"


@pytest.mark.parametrize(
    ("rows", "reason"),
    [
        (
            [
                {"type": "thread.started", "thread_id": "other"},
                {"type": "turn.completed", "usage": {"cached_input_tokens": 1}},
            ],
            "thread-correlation-mismatch",
        ),
        (
            [
                {"type": "thread.started", "thread_id": "thread-1"},
                {"type": "turn.completed", "usage": {"cached_input_tokens": 1}},
                {"type": "turn.completed", "usage": {"cached_input_tokens": 2}},
            ],
            "exactly-one-turn-completed-required",
        ),
        (
            [
                {"type": "thread.started", "thread_id": "thread-1"},
                {"type": "turn.completed", "usage": {"cached_input_tokens": True}},
            ],
            "invalid-cached-input-counter",
        ),
    ],
)
def test_exact_event_rejects_ambiguous_or_invalid_evidence(
    tmp_path: Path, rows: list[object], reason: str
):
    _authorize(tmp_path)
    source = _jsonl(tmp_path / "bad.jsonl", rows)
    with pytest.raises(measurement.CodexMeasurementError, match=reason):
        measurement.extract_exact_run(tmp_path, source, **_context(tmp_path))


def test_quality_denial_happens_before_source_access(tmp_path: Path):
    with pytest.raises(measurement.CodexMeasurementError, match="quality-not-authorized"):
        measurement.extract_exact_run(
            tmp_path, tmp_path / "missing.jsonl", **_context(tmp_path)
        )


def test_cumulative_boundaries_use_monotonic_delta(tmp_path: Path):
    _authorize(tmp_path)
    result = measurement.measure_cumulative_run(
        tmp_path,
        **_context(tmp_path),
        start_boundary_id="before",
        end_boundary_id="after",
        start_cached_input_tokens=100,
        end_cached_input_tokens=175,
    )
    assert result.cached_input_tokens == 75
    assert result.source_fingerprint is None
    assert result.measurement_mode == "cumulative-boundary"

    with pytest.raises(measurement.CodexMeasurementError, match="non-monotonic"):
        measurement.measure_cumulative_run(
            tmp_path,
            **_context(tmp_path, run_id="reset"),
            start_boundary_id="before",
            end_boundary_id="after",
            start_cached_input_tokens=175,
            end_cached_input_tokens=100,
        )


def test_pair_retains_exact_negative_reduction(tmp_path: Path):
    _authorize(tmp_path)
    baseline = measurement.measure_cumulative_run(
        tmp_path, **_context(tmp_path), start_boundary_id="b0",
        end_boundary_id="b1", start_cached_input_tokens=0,
        end_cached_input_tokens=100
    )
    guarded = replace(
        baseline, run_id="run-guarded", role="guarded", cached_input_tokens=125
    )
    pair = measurement.compare_pair(
        tmp_path, baseline, guarded, pair_id="pair-1",
        execution_order="baseline-first"
    )
    assert pair.reduction == Fraction(-1, 4)


def _pair(index: int, kind: str, reduction: Fraction = Fraction(2, 5)):
    baseline = 100
    guarded = baseline - int(reduction * baseline)
    exact = Fraction(baseline - guarded, baseline)
    return measurement.CodexPairMeasurement(
        measurement.PAIR_SCHEMA, f"pair-{index}", f"quality-{index}", kind,
        "0.144.1", "gpt-test",
        "baseline-first" if index % 2 == 0 else "guarded-first",
        f"baseline-{index}", f"guarded-{index}", baseline, guarded,
        exact.numerator, exact.denominator
    )


def test_qualification_requires_complete_five_by_three_population(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(
        quality.QualityLedger,
        "authorize_measurement",
        lambda self, pair_id, **kwargs: quality.Authorization(pair_id, True, "pass"),
    )
    kinds = sorted(measurement.FIXTURE_KINDS)
    values = [_pair(i, kinds[i // 5]) for i in range(15)]
    result = measurement.qualify(
        tmp_path, values, qualification_id="qualification"
    )
    assert result.passed is True
    assert Fraction(
        result.provider_median_numerator, result.provider_median_denominator
    ) == Fraction(2, 5)

    with pytest.raises(measurement.CodexMeasurementError, match="15-distinct"):
        measurement.qualify(
            tmp_path, values[:-1], qualification_id="incomplete"
        )


def test_exact_schemas_reject_prohibited_fields(tmp_path: Path):
    _authorize(tmp_path)
    value = measurement.measure_cumulative_run(
        tmp_path, **_context(tmp_path), start_boundary_id="a",
        end_boundary_id="b", start_cached_input_tokens=0,
        end_cached_input_tokens=1
    ).to_dict()
    value["prompt"] = "forbidden"
    with pytest.raises(measurement.CodexMeasurementError, match="unknown"):
        measurement.CodexRunMeasurement.from_dict(value)


def test_ledger_rejects_invalid_nested_evidence(tmp_path: Path):
    ledger = measurement.MeasurementLedger(tmp_path)
    ledger.root.mkdir(parents=True)
    ledger.path.write_text(
        json.dumps(
            {
                "schema": measurement.LEDGER_SCHEMA,
                "event": "run",
                "timestamp": "2026-07-27T00:00:00+00:00",
                "identifier": "bad-run",
                "evidence": {"prompt": "must-not-pass"},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(measurement.CodexMeasurementError):
        ledger.records()
