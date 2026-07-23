import json
from pathlib import Path

from context_guard.audit import jsonl


def test_build_record_excludes_raw_by_default():
    record = jsonl.build_record(
        provider="claude-code",
        event_name="PreToolUse",
        operation="file_read",
        decision_status="block",
        rule_id="files.deny_glob",
        estimated_risk="high",
        repository="my-repo",
        raw_command_or_path="secret/path.env",
    )
    assert "raw" not in record
    assert record["command_hash"].startswith("sha256:")
    assert record["repository"] == "my-repo"
    assert record["decision"] == "block"


def test_append_writes_one_line_per_record(tmp_path: Path):
    log_path = tmp_path / "audit.jsonl"
    record = jsonl.build_record("claude-code", "PreToolUse", "file_read", "allow", None, "low", "repo")
    jsonl.append(log_path, record)
    jsonl.append(log_path, record)
    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["decision"] == "allow"


def test_summarize_counts_by_decision_and_rule(tmp_path: Path):
    log_path = tmp_path / "audit.jsonl"
    jsonl.append(log_path, jsonl.build_record("claude-code", "PreToolUse", "file_read", "block", "files.deny_glob", "high", "repo"))
    jsonl.append(log_path, jsonl.build_record("claude-code", "PreToolUse", "shell_command", "allow", None, "low", "repo"))
    summary = jsonl.summarize(log_path)
    assert summary["total_events"] == 2
    assert summary["by_decision"]["block"] == 1
    assert summary["blocked_by_rule"]["files.deny_glob"] == 1


def test_summarize_empty_log_returns_zero_counts(tmp_path: Path):
    summary = jsonl.summarize(tmp_path / "missing.jsonl")
    assert summary["total_events"] == 0
