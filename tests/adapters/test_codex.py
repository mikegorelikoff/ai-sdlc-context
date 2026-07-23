import json
from pathlib import Path

from context_guard import decisions, events
from context_guard.adapters import codex

FIXTURES = Path(__file__).parent.parent / "fixtures" / "codex"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_parse_pre_tool_use_read():
    event = codex.parse(_load("pre_tool_use_read.json"))
    assert event.operation_kind == events.FILE_READ
    assert event.path == "dist/bundle.min.js"


def test_parse_pre_tool_use_shell():
    event = codex.parse(_load("pre_tool_use_shell.json"))
    assert event.operation_kind == events.SHELL_COMMAND
    assert event.command == "kubectl logs my-pod"


def test_parse_post_tool_use():
    event = codex.parse(_load("post_tool_use.json"))
    assert event.event_name == "PostToolUse"


def test_parse_session_start_is_lifecycle():
    event = codex.parse(_load("session_start.json"))
    assert event.operation_kind == events.SESSION_LIFECYCLE


def test_parse_pre_compact_is_lifecycle():
    event = codex.parse(_load("pre_compact.json"))
    assert event.operation_kind == events.SESSION_LIFECYCLE


def test_parse_post_compact_is_lifecycle():
    event = codex.parse(_load("post_compact.json"))
    assert event.operation_kind == events.SESSION_LIFECYCLE


def test_parse_stop_is_lifecycle():
    event = codex.parse(_load("stop.json"))
    assert event.operation_kind == events.SESSION_LIFECYCLE


def test_render_block_decision():
    rendered = codex.render(decisions.block("nope", "rule-x", suggestions=["try y"]))
    assert rendered["decision"] == "block"
    assert "try y" in rendered["message"]


def test_render_allow_decision():
    assert codex.render(decisions.allow()) == {"decision": "allow"}


def test_render_warn_decision():
    rendered = codex.render(decisions.warn("careful", "rule-y"))
    assert rendered["decision"] == "warn"
