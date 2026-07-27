from __future__ import annotations

import json
from pathlib import Path

from context_guard import cli, receipts


def _receipt(run_id: str, timestamp: str = "2026-07-27T12:00:00+00:00"):
    return {
        "schema": receipts.SCHEMA,
        "run_id": run_id,
        "timestamp": timestamp,
        "provider": "claude",
        "provider_version": "2.1.218",
        "surface": "cli",
        "status": "valid",
        "completed": True,
        "referenced": False,
        "reason_codes": ["required"],
        "classifications": ["required"],
        "requested_action": "full-load",
        "actual_action": "full-load",
    }


def test_receipt_cli_inspect_and_delete_exact_run(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    receipts.write_receipt(tmp_path, _receipt("cli-run"))

    assert cli.main(["receipt", "inspect", "cli-run"]) == 0
    inspected = json.loads(capsys.readouterr().out)
    assert inspected["run_id"] == "cli-run"
    assert cli.main(["receipt", "delete", "cli-run"]) == 0
    deleted = json.loads(capsys.readouterr().out)
    assert deleted == {"deleted": True, "run_id": "cli-run"}
    assert cli.main(["receipt", "inspect", "cli-run"]) == 1
    assert "RECEIPT_NOT_FOUND" in capsys.readouterr().err


def test_receipt_cli_prune_uses_requested_retention(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    receipts.write_receipt(tmp_path, _receipt("old", "2000-01-01T00:00:00+00:00"))
    receipts.write_receipt(tmp_path, _receipt("recent", "2999-01-01T00:00:00+00:00"))

    assert cli.main(["receipt", "prune", "--days", "30"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["deleted"] == ["old"]
    assert result["retained"] == ["recent"]


def test_receipt_cli_rejects_traversal_identifier(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert cli.main(["receipt", "delete", "../other"]) == 1
    assert "RECEIPT_INVALID" in capsys.readouterr().err
