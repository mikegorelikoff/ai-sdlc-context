import io
import json
import sys
from pathlib import Path

from context_guard import cli


def test_run_command_returns_compact_output_and_artifact(
    tmp_path: Path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    for index in range(20):
        (tmp_path / f"file-{index:02d}.txt").write_text("x", encoding="utf-8")

    assert cli.main(["run", "--", "ls", "-1"]) == 0

    output = capsys.readouterr().out
    assert "file-00.txt" in output
    assert "[full output: artifact:command-001]" in output


def test_claude_hook_transparently_rewrites_supported_command(
    tmp_path: Path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    payload = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "git status"},
        "session_id": "session-1",
        "cwd": str(tmp_path),
    }
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))

    assert cli.main(["hook", "claude"]) == 0

    output = json.loads(capsys.readouterr().out)
    updated = output["hookSpecificOutput"]["updatedInput"]["command"]
    assert updated == "context-guard run -- git status"


def test_claude_hook_does_not_rewrite_compound_command(
    tmp_path: Path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    payload = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "git status && git diff"},
        "session_id": "session-1",
        "cwd": str(tmp_path),
    }
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))

    assert cli.main(["hook", "claude"]) == 0

    assert json.loads(capsys.readouterr().out) == {}
