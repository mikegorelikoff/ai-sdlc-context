from pathlib import Path

from context_guard import events
from context_guard.policies import files
from context_guard.policy_config import Policy


def _policy(**overrides):
    base = Policy(
        mode="enforce",
        files={
            "max_full_read_bytes": 200000,
            "require_range_above_bytes": 50000,
            "deny": ["**/*.min.js", "**/*.lock", "**/package-lock.json"],
        },
    )
    for key, value in overrides.items():
        setattr(base, key, value)
    return base


def _read_event(path: str) -> events.Event:
    return events.Event(provider="claude-code", event_name="PreToolUse", operation_kind=events.FILE_READ, path=path)


def test_deny_glob_blocks_full_read():
    decision = files.evaluate(_read_event("dist/bundle.min.js"), _policy())
    assert decision.status == "block"
    assert decision.rule_id == files.RULE_DENY_GLOB


def test_deny_glob_blocks_lockfile():
    decision = files.evaluate(_read_event("package-lock.json"), _policy())
    assert decision.status == "block"


def test_oversized_full_read_blocks(tmp_path: Path):
    big_file = tmp_path / "big.txt"
    big_file.write_bytes(b"x" * 60000)
    decision = files.evaluate(_read_event(str(big_file)), _policy())
    assert decision.status == "block"
    assert decision.rule_id == files.RULE_OVERSIZED_READ


def test_bounded_range_allows_large_file(tmp_path: Path):
    big_file = tmp_path / "big.txt"
    big_file.write_bytes(b"x" * 60000)
    decision = files.evaluate(_read_event(str(big_file)), _policy(), has_range=True)
    assert decision is None


def test_small_file_allowed(tmp_path: Path):
    small_file = tmp_path / "small.txt"
    small_file.write_bytes(b"x" * 100)
    decision = files.evaluate(_read_event(str(small_file)), _policy())
    assert decision is None


def test_non_file_read_event_ignored():
    event = events.Event(provider="claude-code", event_name="PreToolUse", operation_kind=events.SHELL_COMMAND, command="ls")
    assert files.evaluate(event, _policy()) is None


def test_missing_file_fails_open(tmp_path: Path):
    missing = tmp_path / "does-not-exist.txt"
    decision = files.evaluate(_read_event(str(missing)), _policy())
    assert decision is None


def test_observe_mode_allows_but_marks_would_have():
    decision = files.evaluate(_read_event("dist/bundle.min.js"), _policy(mode="observe"))
    assert decision.status == "allow"
    assert decision.would_have == "block"
