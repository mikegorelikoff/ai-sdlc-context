# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

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

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete with a blocking finding and a source-freshness warning. | policy.toon:14 |

| Policy layer | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Policy layer | BLOCKED | Unresolved behavior prevents the next stage | policy.toon:14 | Resolve the primary finding before handoff |

| Action | Matched rule | Decision | Required gate | Evidence |
| --- | --- | --- | --- | --- |
| change.apply | fresh-evidence | BLOCKED | Refresh stale report | policy.toon:14 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | change.apply | policy.toon:14 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Policy layer is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Policy layer | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Policy layer | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide policy layer |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Provide policy layer | Validated policy layer |
