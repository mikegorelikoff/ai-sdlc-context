# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared story id result; evidence supports the reported result. | fixture.toon:1 |

| Story ID | Actor | Desired outcome | Acceptance | Dependency |
| --- | --- | --- | --- | --- |
| ST-001 | Operator | Retry without duplicate charge | AC-001 | Ledger unique key |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate accepted workflow with its owning workflow | fixture.toon:1 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| Story ID | Actor | Desired outcome | Acceptance | Dependency |
| --- | --- | --- | --- | --- |
| ST-001 | Operator | Retry without duplicate charge | AC-001 | Ledger unique key |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate accepted workflow with its owning workflow | fixture.toon:1 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Accepted workflow is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Accepted workflow | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Accepted workflow | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide accepted workflow |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Provide accepted workflow | Validated accepted workflow |
