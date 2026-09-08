# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete; resolve the reported blocker before delivery. | requirements.md:25 |

| Requirement source | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Requirement source | BLOCKED | Unresolved behavior prevents the next stage | requirements.md:25 | Resolve the primary finding before handoff |

| Requirement ID | Testability gap | Risk | Evidence | Required action |
| --- | --- | --- | --- | --- |
| AC-002 | Timeout lacks upper bound | Cannot assert deadline | requirements.md:25 | Define timeout limit |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Define timeout limit | requirements.md:25 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete with a blocking finding and a source-freshness warning. | requirements.md:25 |

| Requirement source | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Requirement source | BLOCKED | Unresolved behavior prevents the next stage | requirements.md:25 | Resolve the primary finding before handoff |

| Requirement ID | Testability gap | Risk | Evidence | Required action |
| --- | --- | --- | --- | --- |
| AC-002 | Timeout lacks upper bound | Cannot assert deadline | requirements.md:25 | Define timeout limit |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Define timeout limit | requirements.md:25 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Requirement source is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Requirement source | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Requirement source | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide requirement source |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| QA | Provide requirement source | Validated requirement source |
