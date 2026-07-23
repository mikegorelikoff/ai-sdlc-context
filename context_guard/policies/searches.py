"""Search-command policy: require a path scope and/or a result limit."""

from __future__ import annotations

import re

from context_guard import decisions, events
from context_guard.policy_config import Policy

RULE_UNSCOPED_SEARCH = "search.unscoped"

_UNSCOPED_PATHS = {".", "./", "/"}
_RESULT_LIMIT_RE = re.compile(r"(-m\s*\d+|--max-count(=|\s+)\d+|--count\b)")


def _tokenize(command: str) -> list[str]:
    return command.strip().split()


def _scope_path(binary: str, args: list[str]) -> str | None:
    non_flag_args = [a for a in args if not a.startswith("-")]
    if binary == "find":
        return non_flag_args[0] if non_flag_args else None
    # grep/rg/ag/ack: pattern is typically the first non-flag arg, an optional
    # path follows as the last non-flag arg.
    if len(non_flag_args) >= 2:
        return non_flag_args[-1]
    return None


def evaluate(event: events.Event, policy: Policy) -> decisions.Decision | None:
    """Evaluate a search_command event. Returns None when this module does not apply."""
    if event.operation_kind != events.SEARCH_COMMAND:
        return None
    if not event.command:
        return None

    search_cfg = policy.search
    require_scope = search_cfg.get("require_path_scope", False)
    max_results = search_cfg.get("maximum_results")

    tokens = _tokenize(event.command)
    if not tokens:
        return None
    binary = tokens[0].rsplit("/", 1)[-1]
    args = tokens[1:]

    scope_path = _scope_path(binary, args)
    is_scoped = scope_path is not None and scope_path not in _UNSCOPED_PATHS
    has_result_limit = bool(_RESULT_LIMIT_RE.search(event.command)) or "| head" in event.command

    violates_scope = require_scope and not is_scoped
    violates_limit = max_results is not None and not has_result_limit and not is_scoped

    if not (violates_scope or violates_limit):
        return None

    mode = policy.mode_for("search")
    decision = decisions.block(
        f"'{event.command}' searches without a path scope or result limit, which can return excessive matches. "
        "Scope the search to a specific path or add a result limit.",
        RULE_UNSCOPED_SEARCH,
        suggestions=[f"{binary} <pattern> <path>", f"{binary} <pattern> <path> -m 50"],
    )
    return decisions.apply_mode(decision, mode)
