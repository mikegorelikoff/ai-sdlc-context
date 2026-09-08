# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared operation result; evidence supports the reported result. | adapter.toon:9 |

| Operation | Host mapping | Capability | Fallback | Evidence |
| --- | --- | --- | --- | --- |
| inspect diff | git diff | Read repository | Direct read | adapter.toon:9 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate host capability with its owning workflow | adapter.toon:9 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | adapter.toon:9 |

| Operation | Host mapping | Capability | Fallback | Evidence |
| --- | --- | --- | --- | --- |
| inspect diff | git diff | Read repository | Direct read | adapter.toon:9 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate host capability with its owning workflow | adapter.toon:9 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Host capability is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Host capability | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Host capability | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide host capability |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide host capability | Validated host capability |
