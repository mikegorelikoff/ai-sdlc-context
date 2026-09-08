# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete; resolve the reported blocker before delivery. | delivery-spec.md:40 |

| Delivery package | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Delivery package | BLOCKED | Unresolved behavior prevents the next stage | delivery-spec.md:40 | Resolve the primary finding before handoff |

| Delivery gate | Decision | Gap | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Ownership | BLOCKED | Support owner absent | delivery-spec.md:40 | Name escalation owner |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Name escalation owner | delivery-spec.md:40 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Review complete with a blocking finding and a source-freshness warning. | delivery-spec.md:40 |

| Delivery package | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Delivery package | BLOCKED | Unresolved behavior prevents the next stage | delivery-spec.md:40 | Resolve the primary finding before handoff |

| Delivery gate | Decision | Gap | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Ownership | BLOCKED | Support owner absent | delivery-spec.md:40 | Name escalation owner |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Name escalation owner | delivery-spec.md:40 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Delivery package is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Delivery package | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Delivery package | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide delivery package |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide delivery package | Validated delivery package |
