# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared test id result; evidence supports the reported result. | test-cases.md:12 |

| Test ID | Requirement ID | Scenario | Suite | Expected result | Evidence |
| --- | --- | --- | --- | --- | --- |
| TC-001 | AC-001 | Duplicate callback | Regression | One ledger entry | test-cases.md:12 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate qa strategy with its owning workflow | test-cases.md:12 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | test-cases.md:12 |

| Test ID | Requirement ID | Scenario | Suite | Expected result | Evidence |
| --- | --- | --- | --- | --- | --- |
| TC-001 | AC-001 | Duplicate callback | Regression | One ledger entry | test-cases.md:12 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate qa strategy with its owning workflow | test-cases.md:12 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | QA strategy is unavailable; dependent work has not run. | source-inventory.toon:missing |

| QA strategy | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| QA strategy | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide qa strategy |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Provide qa strategy | Validated qa strategy |
