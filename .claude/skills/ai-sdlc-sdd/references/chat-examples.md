# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared artifact result; evidence supports the reported result. | plan.toon:12 |

| Artifact | Change | Requirement ID | Validation | Evidence |
| --- | --- | --- | --- | --- |
| design.md | Specify retry identity | AC-001 | PASS | plan.toon:12 |

| Component | Responsibility | Decision | Dependency | Evidence |
| --- | --- | --- | --- | --- |
| Retry worker | Deduplicate repeated payment requests | Reuse the payment ledger | Payment store | plan.toon:12 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate approved behavior with its owning workflow | plan.toon:12 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | plan.toon:12 |

| Artifact | Change | Requirement ID | Validation | Evidence |
| --- | --- | --- | --- | --- |
| design.md | Specify retry identity | AC-001 | PASS | plan.toon:12 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate approved behavior with its owning workflow | plan.toon:12 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Approved behavior is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Approved behavior | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Approved behavior | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide approved behavior |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide approved behavior | Validated approved behavior |
