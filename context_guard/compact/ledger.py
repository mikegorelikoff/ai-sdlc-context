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


def summarize(repo_root: Path) -> dict[str, Any]:
    """Aggregate local compact-output savings without claiming provider billing."""
    raw_bytes = 0
    compact_bytes = 0
    measured_invocations = 0
    by_status: dict[str, int] = {}
    for row in all_rows(repo_root):
        status = str(row["status"])
        by_status[status] = by_status.get(status, 0) + 1
        try:
            summary = json.loads(row["summary_json"])
        except (json.JSONDecodeError, TypeError):
            continue
        raw = summary.get("raw_output_bytes")
        compact = summary.get("compact_output_bytes")
        if (
            isinstance(raw, int)
            and not isinstance(raw, bool)
            and raw >= 0
            and isinstance(compact, int)
            and not isinstance(compact, bool)
            and compact >= 0
        ):
            raw_bytes += raw
            compact_bytes += compact
            measured_invocations += 1

    saved_bytes = max(raw_bytes - compact_bytes, 0)
    reduction = round((saved_bytes / raw_bytes) * 100, 2) if raw_bytes else None
    return {
        "invocations": len(all_rows(repo_root)),
        "measured_invocations": measured_invocations,
        "by_status": by_status,
        "raw_output_bytes": raw_bytes,
        "compact_output_bytes": compact_bytes,
        "saved_output_bytes": saved_bytes,
        "output_reduction_percent": reduction,
        "estimated_input_tokens_saved": saved_bytes // 4,
        "note": (
            "Estimated tokens use bytes/4. Output reduction is not a provider-reported "
            "token count or billing reduction."
        ),
    }
