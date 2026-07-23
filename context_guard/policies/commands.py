"""Shell-command policy: detect unbounded log/history commands."""

from __future__ import annotations

import re

from context_guard import decisions, events
from context_guard.policy_config import Policy

RULE_UNBOUNDED_COMMAND = "commands.unbounded"

# Flags that count as a recognized boundary for a given command family.
_BOUND_FLAGS: dict[str, list[re.Pattern[str]]] = {
    "docker logs": [re.compile(r"--tail\b"), re.compile(r"--since\b"), re.compile(r"--until\b")],
    "docker compose logs": [re.compile(r"--tail\b"), re.compile(r"--since\b"), re.compile(r"--until\b")],
    "kubectl logs": [re.compile(r"--tail\b"), re.compile(r"--since\b"), re.compile(r"--since-time\b")],
    "git log": [
        re.compile(r"-n\d*\b"),
        re.compile(r"-\d+\b"),
        re.compile(r"--max-count\b"),
        re.compile(r"--since\b"),
        re.compile(r"--oneline\b"),
    ],
}

_ALTERNATIVES: dict[str, list[str]] = {
    "docker logs": ["docker logs --tail 200 <container>", "docker logs --since 10m <container>"],
    "docker compose logs": ["docker compose logs --tail 200 <service>", "docker compose logs --since 10m <service>"],
    "kubectl logs": ["kubectl logs --tail 200 <pod>", "kubectl logs --since 10m <pod>"],
    "git log": ["git log -n 20", "git log --oneline -20"],
}


def _matched_family(command: str, families: list[str]) -> str | None:
    normalized = command.strip()
    for family in families:
        if normalized == family or normalized.startswith(family + " "):
            return family
    return None


def evaluate(event: events.Event, policy: Policy) -> decisions.Decision | None:
    """Evaluate a shell_command event. Returns None when this module does not apply."""
    if event.operation_kind != events.SHELL_COMMAND:
        return None
    if not event.command:
        return None

    require_bounds = policy.commands.get("require_bounds", [])
    family = _matched_family(event.command, require_bounds)
    if family is None:
        return None

    bound_patterns = _BOUND_FLAGS.get(family, [])
    if any(pattern.search(event.command) for pattern in bound_patterns):
        return None

    mode = policy.mode_for("commands")
    alternatives = _ALTERNATIVES.get(family, [])
    decision = decisions.block(
        f"Unbounded '{family}' can add excessive output to the agent context. "
        + (f"Use one of: {', '.join(alternatives)}" if alternatives else "Add a line/time/count boundary."),
        RULE_UNBOUNDED_COMMAND,
        suggestions=alternatives,
    )
    return decisions.apply_mode(decision, mode)
