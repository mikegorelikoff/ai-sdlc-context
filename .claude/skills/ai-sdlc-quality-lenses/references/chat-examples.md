# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete; resolve the reported blocker before delivery. | requirements.md:25 |

| Review artifact | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Review artifact | BLOCKED | Unresolved behavior prevents the next stage | requirements.md:25 | Resolve the primary finding before handoff |

| Lens | Severity | Finding | Requirement ID | Evidence | Next action |
| --- | --- | --- | --- | --- | --- |
| edge-case-hunt | HIGH | Retry limit unspecified | AC-002 | requirements.md:25 | Define retry cap |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Define retry cap | requirements.md:25 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete with a blocking finding and a source-freshness warning. | requirements.md:25 |

| Review artifact | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Review artifact | BLOCKED | Unresolved behavior prevents the next stage | requirements.md:25 | Resolve the primary finding before handoff |

| Lens | Severity | Finding | Requirement ID | Evidence | Next action |
| --- | --- | --- | --- | --- | --- |
| edge-case-hunt | HIGH | Retry limit unspecified | AC-002 | requirements.md:25 | Define retry cap |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Define retry cap | requirements.md:25 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review artifact is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Review artifact | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Review artifact | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide review artifact |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide review artifact | Validated review artifact |
