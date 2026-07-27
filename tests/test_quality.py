from __future__ import annotations

import json
import stat
from pathlib import Path

import pytest

from context_guard import quality, receipts


def _manifest(
    fixture_kind: str = "explicit-ai-sdlc-skill",
    fixture_id: str = "fixture-skill",
    **overrides,
):
    value = {
        "schema": quality.MANIFEST_SCHEMA,
        "fixture_id": fixture_id,
        "fixture_kind": fixture_kind,
        "provider": "claude",
        "provider_version": "2.1.218",
        "model": "test-model",
        "repository_fingerprint": "repo-digest",
        "task_fingerprint": "task-digest",
        "baseline_profile_fingerprint": "baseline-profile",
        "guarded_profile_fingerprint": "guarded-profile",
        "required_instruction_ids": ["REQ-1", "REQ-2"],
    }
    value.update(overrides)
    return value


def _attempt(role: str, pair_id: str = "pair-1", **overrides):
    value = {
        "schema": quality.ATTEMPT_SCHEMA,
        "attempt_id": f"{pair_id}-{role}",
        "pair_id": pair_id,
        "role": role,
        "fixture_id": "fixture-skill",
        "provider": "claude",
        "provider_version": "2.1.218",
        "model": "test-model",
        "repository_fingerprint": "repo-digest",
        "task_fingerprint": "task-digest",
        "profile_fingerprint": f"{role}-profile",
        "fresh_session": True,
        "completion_passed": True,
        "observed_instruction_ids": ["REQ-1", "REQ-2"],
        "explicit_skill_invoked": True,
        "restoration_passed": True,
        "receipt_ref": f"{pair_id}-{role}-receipt",
        "receipt_valid": True,
        "privacy_passed": True,
    }
    value.update(overrides)
    return value


def _parsed_pair(**guarded_overrides):
    manifest = quality.QualityManifest.from_dict(_manifest())
    baseline = quality.AttemptEvidence.from_dict(_attempt("baseline"))
    guarded = quality.AttemptEvidence.from_dict(_attempt("guarded", **guarded_overrides))
    return manifest, baseline, guarded


def test_suite_requires_exactly_one_of_each_frozen_fixture_kind():
    manifests = [
        quality.QualityManifest.from_dict(_manifest("read-only-analysis", "fixture-read")),
        quality.QualityManifest.from_dict(_manifest("test-only-change", "fixture-test")),
        quality.QualityManifest.from_dict(_manifest()),
    ]

    assert {item.fixture_kind for item in quality.validate_suite(reversed(manifests))} == (
        quality.FIXTURE_KINDS
    )
    with pytest.raises(quality.QualityError, match="exactly one"):
        quality.validate_suite(manifests[:2])
    with pytest.raises(quality.QualityError, match="exactly one"):
        quality.validate_suite([manifests[0], manifests[0], manifests[2]])


def test_passing_pair_is_private_receipted_and_measurement_authorized(tmp_path: Path):
    manifest, baseline, guarded = _parsed_pair()
    ledger = quality.QualityLedger(tmp_path)

    evaluation = ledger.record_evaluation(
        manifest, baseline, guarded, run_id="quality-pass"
    )

    assert evaluation.valid is True
    assert evaluation.measurement_allowed is True
    assert [gate.gate_id for gate in evaluation.gates] == list(quality.GATE_IDS)
    assert all(gate.passed for gate in evaluation.gates)
    assert ledger.authorize("pair-1").allowed is True
    assert stat.S_IMODE(ledger.root.stat().st_mode) == 0o700
    assert stat.S_IMODE(ledger.path.stat().st_mode) == 0o600
    receipt = receipts.inspect_receipt(tmp_path, "quality-pass")
    assert receipt["quality_ref"] == "pair-1"
    assert receipt["actual_action"] == "measurement-allowed"


@pytest.mark.parametrize(
    ("gate_id", "overrides"),
    [
        ("QG-302", {"pair_id": "other-pair"}),
        ("QG-303", {"model": "different-model"}),
        ("QG-304", {"fresh_session": False}),
        ("QG-305", {"completion_passed": False}),
        ("QG-306", {"observed_instruction_ids": ["REQ-1"]}),
        ("QG-307", {"explicit_skill_invoked": False}),
        ("QG-308", {"restoration_passed": False}),
        ("QG-309", {"receipt_valid": False}),
    ],
)
def test_each_runtime_gate_failure_is_retained_and_denied(
    tmp_path: Path, gate_id: str, overrides: dict[str, object]
):
    manifest, baseline, guarded = _parsed_pair(**overrides)
    ledger = quality.QualityLedger(tmp_path)

    evaluation = ledger.record_evaluation(
        manifest, baseline, guarded, run_id=f"failure-{gate_id.lower()}"
    )

    failed = {gate.gate_id for gate in evaluation.gates if not gate.passed}
    assert gate_id in failed
    assert evaluation.valid is False
    assert ledger.authorize("pair-1").reason_code == "quality-gates-failed"


def test_qg301_schema_and_prohibited_content_fail_before_persistence(tmp_path: Path):
    ledger = quality.QualityLedger(tmp_path)
    malformed = _manifest(schema="wrong", prompt="raw task must not persist")

    with pytest.raises(quality.QualityError):
        quality.QualityManifest.from_dict(malformed)
    for field in ("prompt", "source", "output", "cache_read_tokens"):
        attempt = _attempt("baseline")
        attempt[field] = "forbidden"
        with pytest.raises(quality.QualityError, match="unknown fields"):
            quality.AttemptEvidence.from_dict(attempt)

    assert not ledger.path.exists()


@pytest.mark.parametrize("provider", ["unknown", "", "claude\nsecret"])
def test_provider_and_unbounded_content_are_rejected(provider: str):
    with pytest.raises(quality.QualityError):
        quality.QualityManifest.from_dict(_manifest(provider=provider))
    with pytest.raises(quality.QualityError):
        quality.AttemptEvidence.from_dict(_attempt("baseline", receipt_ref="x" * 257))


def test_invalid_pair_and_valid_retry_coexist_without_selection(tmp_path: Path):
    ledger = quality.QualityLedger(tmp_path)
    manifest, baseline, guarded = _parsed_pair(completion_passed=False)
    ledger.record_evaluation(manifest, baseline, guarded, run_id="bad-run")

    retry_baseline = quality.AttemptEvidence.from_dict(_attempt("baseline", "pair-2"))
    retry_guarded = quality.AttemptEvidence.from_dict(_attempt("guarded", "pair-2"))
    ledger.record_evaluation(
        manifest, retry_baseline, retry_guarded, run_id="good-run"
    )

    assert ledger.authorize("pair-1").allowed is False
    assert ledger.authorize("pair-2").allowed is True
    assert len(ledger.path.read_text(encoding="utf-8").splitlines()) == 2


def test_qa_invalidation_is_append_only_and_revokes_authorization(tmp_path: Path):
    manifest, baseline, guarded = _parsed_pair()
    ledger = quality.QualityLedger(tmp_path)
    ledger.record_evaluation(manifest, baseline, guarded, run_id="valid-run")
    original = ledger.path.read_bytes()

    result = ledger.invalidate(
        "pair-1", run_id="qa-invalidate", reason_code="qa-oracle-regression"
    )

    assert result.allowed is False
    assert ledger.path.read_bytes().startswith(original)
    assert ledger.authorize("pair-1").reason_code == "qa-oracle-regression"
    receipt = receipts.inspect_receipt(tmp_path, "qa-invalidate")
    assert receipt["actual_action"] == "measurement-denied"


def test_missing_corrupt_unknown_and_ambiguous_evidence_deny(tmp_path: Path):
    ledger = quality.QualityLedger(tmp_path)
    assert ledger.authorize("missing").reason_code == "missing-quality-evidence"

    ledger.root.mkdir(parents=True)
    ledger.path.write_text('{"schema":"wrong"}\n', encoding="utf-8")
    assert ledger.authorize("pair-1").reason_code == "corrupt-quality-ledger"

    ledger.path.unlink()
    manifest, baseline, guarded = _parsed_pair()
    ledger.record_evaluation(manifest, baseline, guarded, run_id="first-run")
    record = json.loads(ledger.path.read_text(encoding="utf-8"))
    record["prompt"] = "injected raw content"
    ledger.path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    assert ledger.authorize("pair-1").reason_code == "corrupt-quality-ledger"

    record.pop("prompt")
    ledger.path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    ledger.record_evaluation(manifest, baseline, guarded, run_id="second-run")
    assert ledger.authorize("pair-1").reason_code == "ambiguous-quality-evidence"


@pytest.mark.parametrize(
    "failure",
    [receipts.ReceiptError("simulated failure"), OSError("simulated I/O failure")],
)
def test_receipt_failure_appends_invalidation_and_never_authorizes(
    tmp_path: Path, monkeypatch, failure: Exception
):
    manifest, baseline, guarded = _parsed_pair()
    ledger = quality.QualityLedger(tmp_path)

    def fail_receipt(*args, **kwargs):
        raise failure

    monkeypatch.setattr(receipts, "write_receipt", fail_receipt)
    with pytest.raises(type(failure)):
        ledger.record_evaluation(manifest, baseline, guarded, run_id="receipt-fail")

    assert ledger.authorize("pair-1").reason_code == "quality-receipt-failed"


def test_writer_contention_leaves_no_partial_ledger_record(tmp_path: Path):
    ledger = quality.QualityLedger(tmp_path)
    manifest, baseline, guarded = _parsed_pair()

    with quality.writer_lock(ledger.root):
        with pytest.raises(quality.QualityBusyError):
            ledger.record_evaluation(manifest, baseline, guarded, run_id="busy-run")

    assert not ledger.path.exists()
    assert not (
        tmp_path / ".context-guard" / "receipts" / "records" / "busy-run.json"
    ).exists()


def test_ledger_contains_only_sanitized_fingerprints_and_gate_evidence(tmp_path: Path):
    manifest, baseline, guarded = _parsed_pair()
    ledger = quality.QualityLedger(tmp_path)
    ledger.record_evaluation(manifest, baseline, guarded, run_id="privacy-run")

    record = json.loads(ledger.path.read_text(encoding="utf-8"))
    assert set(record) == {
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
    serialized = json.dumps(record)
    assert all(word not in serialized for word in ("prompt", "source", "output", "token"))
