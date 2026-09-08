# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared requirement id result; evidence supports the reported result. | traceability.md:9 |

| Requirement ID | Test ID | Suite | Coverage status | Blocker | Evidence |
| --- | --- | --- | --- | --- | --- |
| AC-001 | TC-001 | Regression | PASS | None | traceability.md:9 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate test suite with its owning workflow | traceability.md:9 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | traceability.md:9 |

| Requirement ID | Test ID | Suite | Coverage status | Blocker | Evidence |
| --- | --- | --- | --- | --- | --- |
| AC-001 | TC-001 | Regression | PASS | None | traceability.md:9 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Validate test suite with its owning workflow | traceability.md:9 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Test suite is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Test suite | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Test suite | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide test suite |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Provide test suite | Validated test suite |
