# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PENDING | Prepared discovery topic result; owner decision or execution remains pending. | fixture.toon:1 |

| Discovery topic | Known evidence | Unresolved question | Decision impact | Owner |
| --- | --- | --- | --- | --- |
| Customer pain | Duplicate refunds reported | How many per month? | MVP priority | Product |

| Assumption | Validation method | Owner | Evidence |
| --- | --- | --- | --- |
| Payment providers honor idempotency keys | Exercise a retry in the provider sandbox | Product | fixture.toon:1 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate customer problem with its owning workflow | fixture.toon:1 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| Discovery topic | Known evidence | Unresolved question | Decision impact | Owner |
| --- | --- | --- | --- | --- |
| Customer pain | Duplicate refunds reported | How many per month? | MVP priority | Product |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate customer problem with its owning workflow | fixture.toon:1 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Customer problem is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Customer problem | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Customer problem | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide customer problem |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Provide customer problem | Validated customer problem |
