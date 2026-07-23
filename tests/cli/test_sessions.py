import io
import json
import sys
from pathlib import Path

from context_guard import cli
from context_guard.policies import sessions


def _run_hook(monkeypatch, payload: dict) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    assert cli.main(["hook", "claude"]) == 0


def test_session_start_initializes_state(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _run_hook(monkeypatch, {"hook_event_name": "SessionStart", "session_id": "s1", "cwd": str(tmp_path), "timestamp": "t0"})
    state_path = sessions._state_path(tmp_path, "s1")
    assert state_path.is_file()


def test_pre_compact_records_checkpoint(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _run_hook(monkeypatch, {"hook_event_name": "SessionStart", "session_id": "s1", "cwd": str(tmp_path), "timestamp": "t0"})
    _run_hook(monkeypatch, {"hook_event_name": "PreCompact", "session_id": "s1", "cwd": str(tmp_path), "timestamp": "t1"})
    state = sessions._load_state(tmp_path, "s1")
    assert state["last_compaction_at"] == "t1"


def test_stop_removes_session_state(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _run_hook(monkeypatch, {"hook_event_name": "SessionStart", "session_id": "s1", "cwd": str(tmp_path), "timestamp": "t0"})
    _run_hook(monkeypatch, {"hook_event_name": "Stop", "session_id": "s1", "cwd": str(tmp_path)})
    assert not sessions._state_path(tmp_path, "s1").is_file()


def test_repeated_reads_tracked_across_hook_invocations(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    target = tmp_path / "a.txt"
    target.write_text("small", encoding="utf-8")
    payload = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Read",
        "tool_input": {"file_path": str(target)},
        "session_id": "s1",
        "cwd": str(tmp_path),
    }
    for _ in range(3):
        _run_hook(monkeypatch, payload)

    state = sessions._load_state(tmp_path, "s1")
    assert state["reads_by_path"][str(target)] == 3
