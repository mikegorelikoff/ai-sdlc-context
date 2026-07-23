"""Codex hook adapter: parse hook JSON into Event, render Decision into hook JSON.

Codex currently executes command hook handlers only; the payload/response
shapes here are a documented assumption (see requirements.md Assumptions) and
are isolated to this module so a schema change does not touch the engine.
"""

from __future__ import annotations

from typing import Any

from context_guard import decisions, events

PROVIDER = "codex"

_LIFECYCLE_EVENTS = {"SessionStart", "PreCompact", "PostCompact", "Stop"}


def parse(payload: dict[str, Any]) -> events.Event:
    event_name = payload.get("event", "")
    tool = payload.get("tool", {}) or {}
    tool_name = tool.get("name")
    tool_input = tool.get("input", {}) or {}

    path = tool_input.get("path")
    command = tool_input.get("command")
    has_range = "start_line" in tool_input or "end_line" in tool_input

    if event_name in _LIFECYCLE_EVENTS:
        operation_kind = events.SESSION_LIFECYCLE
    else:
        operation_kind = events.classify_operation(event_name, tool_name, command)

    return events.Event(
        provider=PROVIDER,
        event_name=event_name,
        operation_kind=operation_kind,
        path=path,
        command=command,
        session_id=payload.get("session_id", ""),
        cwd=payload.get("cwd", ""),
        raw={**payload, "_has_range": has_range},
    )


def has_bounded_range(event: events.Event) -> bool:
    return bool(event.raw.get("_has_range"))


def render(decision: decisions.Decision) -> dict[str, Any]:
    if decision.status == decisions.BLOCK:
        message = decision.message or "Blocked by Context Guard policy."
        if decision.suggestions:
            message = message + " Suggested alternatives: " + "; ".join(decision.suggestions)
        return {"decision": "block", "message": message}
    if decision.status == decisions.WARN:
        return {"decision": "warn", "message": decision.message or "Context Guard warning."}
    return {"decision": "allow"}
