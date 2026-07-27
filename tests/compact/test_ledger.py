from pathlib import Path

from context_guard.compact import ledger


def test_record_appends_one_row(tmp_path: Path):
    ledger.record(
        tmp_path,
        command="pytest",
        commit="abc123",
        artifact_kind="test",
        artifact_id="test-001",
        status="failed",
        summary={"tests": {"collected": 1, "passed": 0, "failed": 1}},
        timestamp="2026-07-24T00:00:00Z",
    )
    rows = ledger.all_rows(tmp_path)
    assert len(rows) == 1
    assert rows[0]["artifact_id"] == "test-001"
    assert rows[0]["command"] == "pytest"
    assert rows[0]["status"] == "failed"


def test_multiple_records_accumulate(tmp_path: Path):
    for i in range(3):
        ledger.record(
            tmp_path,
            command="pytest",
            commit=None,
            artifact_kind="test",
            artifact_id=f"test-{i:03d}",
            status="passed",
            summary={},
            timestamp="2026-07-24T00:00:00Z",
        )
    assert len(ledger.all_rows(tmp_path)) == 3


def test_no_ledger_file_returns_empty_list(tmp_path: Path):
    assert ledger.all_rows(tmp_path) == []


def test_summarize_reports_output_reduction_without_billing_claim(tmp_path: Path):
    ledger.record(
        tmp_path,
        command="pytest",
        commit=None,
        artifact_kind="test",
        artifact_id="test-001",
        status="passed",
        summary={"raw_output_bytes": 1000, "compact_output_bytes": 200},
        timestamp="2026-07-27T00:00:00Z",
    )

    summary = ledger.summarize(tmp_path)

    assert summary["invocations"] == 1
    assert summary["measured_invocations"] == 1
    assert summary["saved_output_bytes"] == 800
    assert summary["output_reduction_percent"] == 80.0
    assert summary["estimated_input_tokens_saved"] == 200
    assert "not a provider-reported" in summary["note"]
