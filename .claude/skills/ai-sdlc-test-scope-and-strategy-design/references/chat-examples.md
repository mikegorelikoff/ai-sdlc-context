# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared coverage target result; evidence supports the reported result. | fixture.toon:1 |

| Coverage target | Risk | Test approach | Data / environment | Exit criterion |
| --- | --- | --- | --- | --- |
| Payment replay | Duplicate debit | Service regression | Seeded ledger | TC-001 passes |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate testable scope with its owning workflow | fixture.toon:1 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| Coverage target | Risk | Test approach | Data / environment | Exit criterion |
| --- | --- | --- | --- | --- |
| Payment replay | Duplicate debit | Service regression | Seeded ledger | TC-001 passes |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate testable scope with its owning workflow | fixture.toon:1 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Testable scope is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Testable scope | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Testable scope | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide testable scope |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Provide testable scope | Validated testable scope |
