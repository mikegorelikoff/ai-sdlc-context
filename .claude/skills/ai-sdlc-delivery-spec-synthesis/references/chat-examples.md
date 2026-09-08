# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared requirement id result; evidence supports the reported result. | ST-001 |

| Requirement ID | Behavior | Interface | Constraint | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 | Return prior charge for same key | POST /payments | One charge per key | ST-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate accepted story with its owning workflow | ST-001 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | ST-001 |

| Requirement ID | Behavior | Interface | Constraint | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 | Return prior charge for same key | POST /payments | One charge per key | ST-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate accepted story with its owning workflow | ST-001 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Accepted story is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Accepted story | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Accepted story | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide accepted story |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide accepted story | Validated accepted story |
