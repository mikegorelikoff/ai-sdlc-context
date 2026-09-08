# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared goal result; evidence supports the reported result. | fixture.toon:1 |

| Goal | Actor | Capability | Epic | Success measure |
| --- | --- | --- | --- | --- |
| Reduce duplicate charges | Operator | Idempotent retry | EP-001 | No duplicate ledger entry |

| Capability | Dependency | Owner | Evidence |
| --- | --- | --- | --- |
| Idempotent retry | Payment store | Product owner | fixture.toon:1 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate business goal with its owning workflow | fixture.toon:1 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| Goal | Actor | Capability | Epic | Success measure |
| --- | --- | --- | --- | --- |
| Reduce duplicate charges | Operator | Idempotent retry | EP-001 | No duplicate ledger entry |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate business goal with its owning workflow | fixture.toon:1 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Business goal is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Business goal | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Business goal | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide business goal |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Provide business goal | Validated business goal |
