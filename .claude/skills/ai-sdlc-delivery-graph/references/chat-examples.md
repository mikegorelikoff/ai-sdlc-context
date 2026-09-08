# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared requirement id result; evidence supports the reported result. | graph.toon:20 |

| Requirement ID | Task ID | Test ID | Coverage | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 | T001 | TC-001 | Traced | graph.toon:20 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate trace source with its owning workflow | graph.toon:20 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | graph.toon:20 |

| Requirement ID | Task ID | Test ID | Coverage | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 | T001 | TC-001 | Traced | graph.toon:20 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate trace source with its owning workflow | graph.toon:20 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Trace source is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Trace source | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Trace source | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide trace source |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide trace source | Validated trace source |
