# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete; resolve the reported blocker before delivery. | requirements.md:32 |

| Changed reference | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Changed reference | BLOCKED | Unresolved behavior prevents the next stage | requirements.md:32 | Resolve the primary finding before handoff |

| Changed reference | Affected artifact | Staleness | Evidence | Reopen action |
| --- | --- | --- | --- | --- |
| AC-001 | test-cases.md | Stale retry expectation | requirements.md:32 | Update TC-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate changed reference with its owning workflow | requirements.md:32 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete with a blocking finding and a source-freshness warning. | requirements.md:32 |

| Changed reference | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Changed reference | BLOCKED | Unresolved behavior prevents the next stage | requirements.md:32 | Resolve the primary finding before handoff |

| Changed reference | Affected artifact | Staleness | Evidence | Reopen action |
| --- | --- | --- | --- | --- |
| AC-001 | test-cases.md | Stale retry expectation | requirements.md:32 | Update TC-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate changed reference with its owning workflow | requirements.md:32 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Changed reference is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Changed reference | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Changed reference | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide changed reference |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide changed reference | Validated changed reference |
