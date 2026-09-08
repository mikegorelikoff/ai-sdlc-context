# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared journey / state result; evidence supports the reported result. | wireframe.md:18 |

| Journey / state | Actor | Behavior | Recovery | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- |
| Payment timeout | Operator | Show pending charge | Retry with same key | AC-002 | wireframe.md:18 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate journey actor with its owning workflow | wireframe.md:18 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | wireframe.md:18 |

| Journey / state | Actor | Behavior | Recovery | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- |
| Payment timeout | Operator | Show pending charge | Retry with same key | AC-002 | wireframe.md:18 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate journey actor with its owning workflow | wireframe.md:18 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Journey actor is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Journey actor | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Journey actor | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide journey actor |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide journey actor | Validated journey actor |
