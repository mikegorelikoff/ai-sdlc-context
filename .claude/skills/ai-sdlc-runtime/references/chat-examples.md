# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PENDING | Prepared task id result; owner decision or execution remains pending. | state.toon:15 |

| Task ID | State | Attempts | Evidence | Next transition |
| --- | --- | --- | --- | --- |
| T001 | ready | 0 / 2 | state.toon:15 | Claim task |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate run identity with its owning workflow | state.toon:15 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | state.toon:15 |

| Task ID | State | Attempts | Evidence | Next transition |
| --- | --- | --- | --- | --- |
| T001 | ready | 0 / 2 | state.toon:15 | Claim task |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate run identity with its owning workflow | state.toon:15 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Run identity is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Run identity | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Run identity | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide run identity |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Provide run identity | Validated run identity |
