"""Minimal SQLite ledger recording one row per compact-tool invocation."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

LEDGER_RELATIVE = Path(".context-guard") / "ledger.sqlite"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS invocations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    command TEXT NOT NULL,
    commit_hash TEXT,
    artifact_kind TEXT NOT NULL,
    artifact_id TEXT NOT NULL,
    status TEXT NOT NULL,
    summary_json TEXT NOT NULL
);
"""


def ledger_path(repo_root: Path) -> Path:
    return repo_root / LEDGER_RELATIVE


def _connect(repo_root: Path) -> sqlite3.Connection:
    path = ledger_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(_SCHEMA)
    return conn


def record(
    repo_root: Path,
    command: str,
    commit: str | None,
    artifact_kind: str,
    artifact_id: str,
    status: str,
    summary: dict[str, Any],
    timestamp: str,
) -> None:
    """Append one invocation row. Best-effort: never raises on failure."""
    try:
        conn = _connect(repo_root)
        try:
            conn.execute(
                "INSERT INTO invocations "
                "(timestamp, command, commit_hash, artifact_kind, artifact_id, status, summary_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (timestamp, command, commit, artifact_kind, artifact_id, status, json.dumps(summary)),
            )
            conn.commit()
        finally:
            conn.close()
    except sqlite3.Error:
        pass


def all_rows(repo_root: Path) -> list[dict[str, Any]]:
    """Return every ledger row. Used by tests and future dedup increments."""
    path = ledger_path(repo_root)
    if not path.is_file():
        return []
    conn = sqlite3.connect(path)
    try:
        conn.execute(_SCHEMA)
        cursor = conn.execute(
            "SELECT id, timestamp, command, commit_hash, artifact_kind, artifact_id, status, summary_json "
            "FROM invocations ORDER BY id"
        )
        columns = [d[0] for d in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        conn.close()
