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
