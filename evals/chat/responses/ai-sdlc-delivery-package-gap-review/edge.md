| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete; resolve the reported blocker before delivery. | brd.md:16 |

| Workflow rule | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Workflow rule | BLOCKED | Unresolved behavior prevents the next stage | brd.md:16 | Resolve the primary finding before handoff |

| Workflow | Missing rule | Delivery impact | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Retry settlement &#124; перенос<br>строки | Duplicate callback behavior | Stories remain ambiguous | brd.md:16 | Define replay outcome |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Define replay outcome | brd.md:16 |

```toon
schema: fixture/v1
status: pending
source: "literal | value"
```
