from context_guard import events
from context_guard.policies import searches
from context_guard.policy_config import Policy


def _policy():
    return Policy(mode="enforce", search={"require_path_scope": True, "maximum_results": 100})


def _search_event(command: str) -> events.Event:
    return events.Event(provider="claude-code", event_name="PreToolUse", operation_kind=events.SEARCH_COMMAND, command=command)


def test_unscoped_find_blocked():
    decision = searches.evaluate(_search_event("find . -type f"), _policy())
    assert decision.status == "block"


def test_unscoped_grep_r_blocked():
    decision = searches.evaluate(_search_event('grep -R "term" .'), _policy())
    assert decision.status == "block"


def test_scoped_rg_allowed():
    decision = searches.evaluate(_search_event('rg "PaymentService" src/payment'), _policy())
    assert decision is None


def test_scoped_find_allowed():
    decision = searches.evaluate(_search_event("find src -name '*.py'"), _policy())
    assert decision is None


def test_non_search_event_ignored():
    event = events.Event(provider="claude-code", event_name="PreToolUse", operation_kind=events.SHELL_COMMAND, command="ls")
    assert searches.evaluate(event, _policy()) is None
