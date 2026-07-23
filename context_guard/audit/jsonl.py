"""Append-only local JSONL audit log."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_LOG_RELATIVE = Path(".context-guard") / "audit.jsonl"


def _hash(value: str | None) -> str | None:
    if not value:
        return None
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_record(
    provider: str,
    event_name: str,
    operation: str,
    decision_status: str,
    rule_id: str | None,
    estimated_risk: str,
    repository: str,
    raw_command_or_path: str | None = None,
    include_raw: bool = False,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": provider,
        "event": event_name,
        "operation": operation,
        "rule": rule_id,
        "decision": decision_status,
        "estimated_risk": estimated_risk,
        "command_hash": _hash(raw_command_or_path),
        "repository": repository,
    }
    if include_raw and raw_command_or_path:
        record["raw"] = raw_command_or_path
    return record


def append(log_path: Path, record: dict[str, Any]) -> None:
    """Append one JSON record as a line. Best-effort: never raises on write failure."""
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")
    except OSError:
        pass


def default_log_path(repo_root: Path) -> Path:
    return repo_root / DEFAULT_LOG_RELATIVE


def read_records(log_path: Path) -> list[dict[str, Any]]:
    if not log_path.is_file():
        return []
    records = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def summarize(log_path: Path) -> dict[str, Any]:
    """Aggregate audit records into a prevented-context estimate report."""
    records = read_records(log_path)
    by_decision = Counter(r.get("decision") for r in records)
    by_rule = Counter(r.get("rule") for r in records if r.get("decision") == "block")
    return {
        "total_events": len(records),
        "by_decision": dict(by_decision),
        "blocked_by_rule": dict(by_rule),
        "note": "This is a local prevented-context estimate, not a provider-reported token count.",
    }
