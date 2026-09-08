| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete; resolve the reported blocker before delivery. | policy.toon:14 |

| Policy layer | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Policy layer | BLOCKED | Unresolved behavior prevents the next stage | policy.toon:14 | Resolve the primary finding before handoff |

| Action | Matched rule | Decision | Required gate | Evidence |
| --- | --- | --- | --- | --- |
| change.apply | fresh-evidence | BLOCKED | Refresh stale report | policy.toon:14 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | change.apply | policy.toon:14 |
