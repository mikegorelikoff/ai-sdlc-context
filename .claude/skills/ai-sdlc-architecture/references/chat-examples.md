# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared component result; evidence supports the reported result. | design.md:42 |

| Component | Responsibility | Decision | Dependency | Evidence |
| --- | --- | --- | --- | --- |
| Retry worker | Deduplicate deliveries | Reuse ledger | Payment store | design.md:42 |

| Decision ID | Alternative | Consequence | Evidence |
| --- | --- | --- | --- |
| DEC-001 | Create a separate retry queue | Adds an independently operated component | design.md:42 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate architecture constraint with its owning workflow | design.md:42 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | design.md:42 |

| Component | Responsibility | Decision | Dependency | Evidence |
| --- | --- | --- | --- | --- |
| Retry worker | Deduplicate deliveries | Reuse ledger | Payment store | design.md:42 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate architecture constraint with its owning workflow | design.md:42 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Architecture constraint is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Architecture constraint | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Architecture constraint | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide architecture constraint |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide architecture constraint | Validated architecture constraint |
