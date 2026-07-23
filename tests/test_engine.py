import pytest

from context_guard import decisions, engine, events
from context_guard.policy_config import Policy


def _policy(**overrides):
    base = Policy(
        mode="enforce",
        files={"deny": ["**/*.min.js"]},
        commands={"require_bounds": ["docker compose logs"]},
        search={"require_path_scope": True},
    )
    for key, value in overrides.items():
        setattr(base, key, value)
    return base


def test_enforce_mode_blocks():
    event = events.Event(provider="claude-code", event_name="PreToolUse", operation_kind=events.FILE_READ, path="a.min.js")
    decision = engine.evaluate(event, _policy(mode="enforce"))
    assert decision.status == decisions.BLOCK


def test_observe_mode_allows_with_would_have():
    event = events.Event(provider="claude-code", event_name="PreToolUse", operation_kind=events.FILE_READ, path="a.min.js")
    decision = engine.evaluate(event, _policy(mode="observe"))
    assert decision.status == decisions.ALLOW
    assert decision.would_have == decisions.BLOCK


def test_warn_mode_downgrades_block_to_warn():
    event = events.Event(provider="claude-code", event_name="PreToolUse", operation_kind=events.FILE_READ, path="a.min.js")
    decision = engine.evaluate(event, _policy(mode="warn"))
    assert decision.status == decisions.WARN


def test_no_matching_rule_allows():
    event = events.Event(provider="claude-code", event_name="PreToolUse", operation_kind=events.SHELL_COMMAND, command="npm test")
    decision = engine.evaluate(event, _policy(mode="enforce"))
    assert decision.status == decisions.ALLOW


def test_unhandled_exception_fails_open_by_default(monkeypatch):
    def _boom(event, policy):
        raise RuntimeError("boom")

    monkeypatch.setattr(engine, "_POLICY_MODULES", (type("M", (), {"evaluate": staticmethod(_boom)}),))
    event = events.Event(provider="claude-code", event_name="PreToolUse", operation_kind=events.SHELL_COMMAND, command="anything")
    decision = engine.evaluate(event, _policy())
    assert decision.status == decisions.ALLOW
    assert decision.rule_id == engine.RULE_INTERNAL_ERROR


def test_unhandled_exception_fails_closed_when_configured(monkeypatch):
    def _boom(event, policy):
        raise RuntimeError("boom")

    monkeypatch.setattr(engine, "_POLICY_MODULES", (type("M", (), {"evaluate": staticmethod(_boom)}),))
    event = events.Event(provider="claude-code", event_name="PreToolUse", operation_kind=events.SHELL_COMMAND, command="anything")
    policy = _policy(fail_closed_rules=[engine.RULE_INTERNAL_ERROR])
    decision = engine.evaluate(event, policy)
    assert decision.status == decisions.BLOCK
