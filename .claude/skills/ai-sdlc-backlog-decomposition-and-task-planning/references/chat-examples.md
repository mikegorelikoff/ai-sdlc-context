# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared task id result; evidence supports the reported result. | fixture.toon:1 |

| Task ID | Story | Scope | Depends on | Verification |
| --- | --- | --- | --- | --- |
| T001 | ST-001 | Add idempotency lookup | DEC-001 | TC-001 |

| Story ID | Actor | Outcome | Acceptance |
| --- | --- | --- | --- |
| US-001 | Customer | Retry without a second charge | TC-001 produces one charge |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate approved epic with its owning workflow | fixture.toon:1 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| Task ID | Story | Scope | Depends on | Verification |
| --- | --- | --- | --- | --- |
| T001 | ST-001 | Add idempotency lookup | DEC-001 | TC-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate approved epic with its owning workflow | fixture.toon:1 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Approved epic is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Approved epic | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Approved epic | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide approved epic |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Provide approved epic | Validated approved epic |
