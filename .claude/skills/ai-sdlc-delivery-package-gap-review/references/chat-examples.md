# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete; resolve the reported blocker before delivery. | brd.md:16 |

| Workflow rule | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Workflow rule | BLOCKED | Unresolved behavior prevents the next stage | brd.md:16 | Resolve the primary finding before handoff |

| Workflow | Missing rule | Delivery impact | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Retry settlement | Duplicate callback behavior | Stories remain ambiguous | brd.md:16 | Define replay outcome |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Define replay outcome | brd.md:16 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete with a blocking finding and a source-freshness warning. | brd.md:16 |

| Workflow rule | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Workflow rule | BLOCKED | Unresolved behavior prevents the next stage | brd.md:16 | Resolve the primary finding before handoff |

| Workflow | Missing rule | Delivery impact | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Retry settlement | Duplicate callback behavior | Stories remain ambiguous | brd.md:16 | Define replay outcome |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Define replay outcome | brd.md:16 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Workflow rule is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Workflow rule | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Workflow rule | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide workflow rule |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide workflow rule | Validated workflow rule |
