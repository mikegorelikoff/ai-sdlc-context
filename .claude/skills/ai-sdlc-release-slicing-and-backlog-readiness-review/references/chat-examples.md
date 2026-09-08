# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared release slice result; evidence supports the reported result. | backlog.md:30 |

| Release slice | Included stories | Dependency | Exit criterion | Evidence |
| --- | --- | --- | --- | --- |
| Pilot | ST-001 | Ledger migration | TC-001 passes | backlog.md:30 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate release constraint with its owning workflow | backlog.md:30 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | backlog.md:30 |

| Release slice | Included stories | Dependency | Exit criterion | Evidence |
| --- | --- | --- | --- | --- |
| Pilot | ST-001 | Ledger migration | TC-001 passes | backlog.md:30 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate release constraint with its owning workflow | backlog.md:30 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Release constraint is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Release constraint | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Release constraint | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide release constraint |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Provide release constraint | Validated release constraint |
