# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared target result; evidence supports the reported result. | delta.toon:8 |

| Target | Operation | Before / after | Authority | Evidence |
| --- | --- | --- | --- | --- |
| requirements.md | Replace AC-001 | Retry once / reuse key | Preview only | delta.toon:8 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate change target with its owning workflow | delta.toon:8 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | delta.toon:8 |

| Target | Operation | Before / after | Authority | Evidence |
| --- | --- | --- | --- | --- |
| requirements.md | Replace AC-001 | Retry once / reuse key | Preview only | delta.toon:8 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate change target with its owning workflow | delta.toon:8 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Change target is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Change target | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Change target | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide change target |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide change target | Validated change target |
