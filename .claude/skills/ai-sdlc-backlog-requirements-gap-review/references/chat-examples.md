# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete; resolve the reported blocker before delivery. | brief.md:18 |

| Planning scope | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Planning scope | BLOCKED | Unresolved behavior prevents the next stage | brief.md:18 | Resolve the primary finding before handoff |

| Planning dimension | Gap | Impact | Evidence | Required action |
| --- | --- | --- | --- | --- |
| MVP boundary | Region rollout unspecified | Cannot slice pilot | brief.md:18 | Confirm pilot region |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Confirm pilot region | brief.md:18 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete with a blocking finding and a source-freshness warning. | brief.md:18 |

| Planning scope | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Planning scope | BLOCKED | Unresolved behavior prevents the next stage | brief.md:18 | Resolve the primary finding before handoff |

| Planning dimension | Gap | Impact | Evidence | Required action |
| --- | --- | --- | --- | --- |
| MVP boundary | Region rollout unspecified | Cannot slice pilot | brief.md:18 | Confirm pilot region |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Confirm pilot region | brief.md:18 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Planning scope is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Planning scope | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Planning scope | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide planning scope |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Provide planning scope | Validated planning scope |
