# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared requirement id result; evidence supports the reported result. | interview.md:12 |

| Requirement ID | Actor | Business rule | Acceptance | Evidence |
| --- | --- | --- | --- | --- |
| REQ-001 | Operator | Retry preserves payment identity | One charge per key | interview.md:12 |

| Assumption | Validation question | Owner | Evidence |
| --- | --- | --- | --- |
| Payment providers honor idempotency keys | Does the provider retain retry keys for 24 hours? | Product owner | interview.md:12 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate business actor with its owning workflow | interview.md:12 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | interview.md:12 |

| Requirement ID | Actor | Business rule | Acceptance | Evidence |
| --- | --- | --- | --- | --- |
| REQ-001 | Operator | Retry preserves payment identity | One charge per key | interview.md:12 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate business actor with its owning workflow | interview.md:12 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Business actor is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Business actor | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Business actor | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide business actor |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Provide business actor | Validated business actor |
