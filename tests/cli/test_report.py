import json
from pathlib import Path

from context_guard import cli
from context_guard.audit import jsonl


def test_report_summarizes_audit_log(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    log_path = jsonl.default_log_path(tmp_path)
    jsonl.append(log_path, jsonl.build_record("claude-code", "PreToolUse", "file_read", "block", "files.deny_glob", "high", "repo"))

    assert cli.main(["report"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["total_events"] == 1
    assert "estimate" in output["note"]
    assert output["compact_runtime"]["invocations"] == 0


def test_report_with_no_audit_log(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["report"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["total_events"] == 0


def test_gain_is_an_alias_for_report(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert cli.main(["gain"]) == 0

    output = json.loads(capsys.readouterr().out)
    assert output["compact_runtime"]["raw_output_bytes"] == 0
    assert "billing reduction" in output["compact_runtime"]["note"]
