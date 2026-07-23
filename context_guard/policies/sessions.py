"""Session lifecycle bookkeeping: repeated-read counters and compaction checkpoints."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from context_guard import events

STATE_DIR_NAME = ".context-guard"
SESSIONS_SUBDIR = "sessions"


def _state_path(repo_root: Path, session_id: str) -> Path:
    return repo_root / STATE_DIR_NAME / SESSIONS_SUBDIR / f"{session_id}.json"


def _load_state(repo_root: Path, session_id: str) -> dict[str, Any]:
    path = _state_path(repo_root, session_id)
    if not path.is_file():
        return {
            "session_id": session_id,
            "reads_by_path": {},
            "prevented_bytes_estimate": 0,
            "prevented_lines_estimate": 0,
            "last_compaction_at": None,
        }
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "session_id": session_id,
            "reads_by_path": {},
            "prevented_bytes_estimate": 0,
            "prevented_lines_estimate": 0,
            "last_compaction_at": None,
        }


def _save_state(repo_root: Path, state: dict[str, Any]) -> None:
    path = _state_path(repo_root, state["session_id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(json.dumps(state), encoding="utf-8")
    except OSError:
        pass


def handle_session_start(repo_root: Path, session_id: str, started_at: str) -> None:
    state = _load_state(repo_root, session_id)
    state["started_at"] = started_at
    _save_state(repo_root, state)


def record_read(repo_root: Path, session_id: str, path: str) -> int:
    """Record a file read for repeated-read detection; returns the new count for path."""
    state = _load_state(repo_root, session_id)
    reads = state.setdefault("reads_by_path", {})
    reads[path] = reads.get(path, 0) + 1
    _save_state(repo_root, state)
    return reads[path]


def record_prevented(repo_root: Path, session_id: str, bytes_estimate: int = 0, lines_estimate: int = 0) -> None:
    state = _load_state(repo_root, session_id)
    state["prevented_bytes_estimate"] = state.get("prevented_bytes_estimate", 0) + bytes_estimate
    state["prevented_lines_estimate"] = state.get("prevented_lines_estimate", 0) + lines_estimate
    _save_state(repo_root, state)


def handle_compaction(repo_root: Path, session_id: str, at: str) -> dict[str, Any]:
    """Record a compaction checkpoint and return the session's cumulative estimate."""
    state = _load_state(repo_root, session_id)
    state["last_compaction_at"] = at
    _save_state(repo_root, state)
    return {
        "prevented_bytes_estimate": state.get("prevented_bytes_estimate", 0),
        "prevented_lines_estimate": state.get("prevented_lines_estimate", 0),
    }


def handle_stop(repo_root: Path, session_id: str) -> None:
    """Remove the per-session state file when the session ends."""
    path = _state_path(repo_root, session_id)
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass


def is_lifecycle_event(event: events.Event) -> bool:
    return event.operation_kind == events.SESSION_LIFECYCLE
