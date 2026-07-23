"""Claude Code hook adapter: parse hook JSON into Event, render Decision into hook JSON.

Schema assumptions are documented in specs/001-context-guard/requirements.md
under Assumptions; isolated here so a Claude Code schema change only touches
this module.
"""

from __future__ import annotations

from typing import Any

from context_guard import decisions, events

PROVIDER = "claude-code"

_LIFECYCLE_EVENTS = {"SessionStart", "PreCompact", "Stop"}


def parse(payload: dict[str, Any]) -> events.Event:
    event_name = payload.get("hook_event_name", "")
    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input", {}) or {}

    path = tool_input.get("file_path")
    command = tool_input.get("command")
    has_range = "offset" in tool_input or "limit" in tool_input

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
        reason = decision.message or "Blocked by Context Guard policy."
        if decision.suggestions:
            reason = reason + " Suggested alternatives: " + "; ".join(decision.suggestions)
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
    if decision.status == decisions.WARN:
        reason = decision.message or "Context Guard warning."
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": reason,
            }
        }
    return {}
