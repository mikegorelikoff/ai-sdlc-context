# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared topic result; evidence supports the reported result. | DEC-001 |

| Topic | Position | Agreement / conflict | Reviewer mode | Evidence |
| --- | --- | --- | --- | --- |
| Retry storage | Use existing ledger | Agreement | Simulated perspectives | DEC-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate reviewer evidence with its owning workflow | DEC-001 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | DEC-001 |

| Topic | Position | Agreement / conflict | Reviewer mode | Evidence |
| --- | --- | --- | --- | --- |
| Retry storage | Use existing ledger | Agreement | Simulated perspectives | DEC-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate reviewer evidence with its owning workflow | DEC-001 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Reviewer evidence is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Reviewer evidence | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Reviewer evidence | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide reviewer evidence |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide reviewer evidence | Validated reviewer evidence |
