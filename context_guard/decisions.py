"""Internal decision model returned by policy modules and the engine."""

from __future__ import annotations

from dataclasses import dataclass, field

ALLOW = "allow"
WARN = "warn"
BLOCK = "block"


@dataclass
class Decision:
    """Normalized policy outcome, independent of any provider's response shape."""

    status: str = ALLOW
    message: str | None = None
    suggestions: list[str] = field(default_factory=list)
    rule_id: str | None = None
    estimated_risk: str = "low"
    # True when a block/warn was downgraded to allow because the matching rule
    # group is running in observe mode; kept for audit-record fidelity.
    would_have: str | None = None


def allow() -> Decision:
    return Decision(status=ALLOW)


def warn(message: str, rule_id: str, suggestions: list[str] | None = None, estimated_risk: str = "medium") -> Decision:
    return Decision(
        status=WARN,
        message=message,
        suggestions=suggestions or [],
        rule_id=rule_id,
        estimated_risk=estimated_risk,
    )


def block(message: str, rule_id: str, suggestions: list[str] | None = None, estimated_risk: str = "high") -> Decision:
    return Decision(
        status=BLOCK,
        message=message,
        suggestions=suggestions or [],
        rule_id=rule_id,
        estimated_risk=estimated_risk,
    )


def apply_mode(decision: Decision, mode: str) -> Decision:
    """Downgrade a block/warn decision according to the effective rule-group mode.

    `observe` always allows execution but preserves what the decision *would*
    have been for audit purposes. `warn` never blocks. `enforce` passes the
    decision through unchanged.
    """
    if decision.status == ALLOW or mode == "enforce":
        return decision
    if mode == "observe":
        return Decision(
            status=ALLOW,
            message=None,
            suggestions=[],
            rule_id=decision.rule_id,
            estimated_risk=decision.estimated_risk,
            would_have=decision.status,
        )
    if mode == "warn":
        if decision.status == BLOCK:
            return Decision(
                status=WARN,
                message=decision.message,
                suggestions=decision.suggestions,
                rule_id=decision.rule_id,
                estimated_risk=decision.estimated_risk,
                would_have=BLOCK,
            )
        return decision
    return decision
