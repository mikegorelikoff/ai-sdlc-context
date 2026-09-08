# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete; resolve the reported blocker before delivery. | brd.md:22 |

| Requirements package | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Requirements package | BLOCKED | Unresolved behavior prevents the next stage | brd.md:22 | Resolve the primary finding before handoff |

| Requirement dimension | Readiness | Contradiction / gap | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Business rules | BLOCKED | Retry window unresolved | brd.md:22 | Resolve DEC-002 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Resolve DEC-002 | brd.md:22 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete with a blocking finding and a source-freshness warning. | brd.md:22 |

| Requirements package | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Requirements package | BLOCKED | Unresolved behavior prevents the next stage | brd.md:22 | Resolve the primary finding before handoff |

| Requirement dimension | Readiness | Contradiction / gap | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Business rules | BLOCKED | Retry window unresolved | brd.md:22 | Resolve DEC-002 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Resolve DEC-002 | brd.md:22 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Requirements package is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Requirements package | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Requirements package | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide requirements package |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Provide requirements package | Validated requirements package |
