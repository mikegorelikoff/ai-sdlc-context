import json
from pathlib import Path

from context_guard import decisions, events
from context_guard.adapters import claude_code

FIXTURES = Path(__file__).parent.parent / "fixtures" / "claude_code"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_parse_pre_tool_use_read():
    event = claude_code.parse(_load("pre_tool_use_read.json"))
    assert event.operation_kind == events.FILE_READ
    assert event.path == "dist/bundle.min.js"
    assert event.session_id == "session-abc"


def test_parse_pre_tool_use_bash():
    event = claude_code.parse(_load("pre_tool_use_bash.json"))
    assert event.operation_kind == events.SHELL_COMMAND
    assert event.command == "docker compose logs api"


def test_parse_post_tool_use():
    event = claude_code.parse(_load("post_tool_use.json"))
    assert event.event_name == "PostToolUse"


def test_parse_post_tool_use_failure():
    event = claude_code.parse(_load("post_tool_use_failure.json"))
    assert event.event_name == "PostToolUseFailure"


def test_parse_session_start_is_lifecycle():
    event = claude_code.parse(_load("session_start.json"))
    assert event.operation_kind == events.SESSION_LIFECYCLE
    assert event.event_name == "SessionStart"


def test_parse_pre_compact_is_lifecycle():
    event = claude_code.parse(_load("pre_compact.json"))
    assert event.operation_kind == events.SESSION_LIFECYCLE


def test_parse_stop_is_lifecycle():
    event = claude_code.parse(_load("stop.json"))
    assert event.operation_kind == events.SESSION_LIFECYCLE


def test_render_block_decision():
    rendered = claude_code.render(decisions.block("nope", "rule-x", suggestions=["try y"]))
    assert rendered["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "try y" in rendered["hookSpecificOutput"]["permissionDecisionReason"]


def test_render_allow_decision():
    assert claude_code.render(decisions.allow()) == {}


def test_render_warn_decision():
    rendered = claude_code.render(decisions.warn("careful", "rule-y"))
    assert rendered["hookSpecificOutput"]["permissionDecision"] == "allow"
