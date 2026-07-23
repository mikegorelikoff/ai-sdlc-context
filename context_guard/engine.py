"""Policy evaluation engine: routes events to policy modules with fail-open/fail-closed handling."""

from __future__ import annotations

from context_guard import decisions, events
from context_guard.policies import commands as commands_policy
from context_guard.policies import files as files_policy
from context_guard.policies import searches as searches_policy
from context_guard.policy_config import Policy

RULE_INTERNAL_ERROR = "internal-error"

_POLICY_MODULES = (files_policy, commands_policy, searches_policy)


def evaluate(event: events.Event, policy: Policy, **kwargs) -> decisions.Decision:
    """Evaluate an event against every applicable policy module.

    Any unhandled exception in a policy module is caught here and converted to
    fail-open (allow) unless the module's rule id is in the fail-closed list,
    in which case the operation is blocked with a generic message.
    """
    for module in _POLICY_MODULES:
        try:
            result = module.evaluate(event, policy, **kwargs) if module is files_policy else module.evaluate(event, policy)
        except Exception:  # noqa: BLE001 - deliberate fail-safe boundary
            return _error_decision(policy)
        if result is not None:
            return result
    return decisions.allow()


def _error_decision(policy: Policy) -> decisions.Decision:
    if RULE_INTERNAL_ERROR in policy.fail_closed_rules:
        return decisions.block(
            "Policy could not be verified for this operation; blocking as a precaution.",
            RULE_INTERNAL_ERROR,
        )
    return decisions.Decision(status=decisions.ALLOW, rule_id=RULE_INTERNAL_ERROR)
