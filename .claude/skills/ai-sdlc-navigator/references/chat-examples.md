# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PENDING | Prepared rank result; owner decision or execution remains pending. | requirements.md:8 |

| Rank | Next skill | Reason | Expected artifact | Evidence |
| --- | --- | --- | --- | --- |
| 1 | ai-sdlc-sdd | Approved scope needs design | design.md | requirements.md:8 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate requested feature with its owning workflow | requirements.md:8 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | requirements.md:8 |

| Rank | Next skill | Reason | Expected artifact | Evidence |
| --- | --- | --- | --- | --- |
| 1 | ai-sdlc-sdd | Approved scope needs design | design.md | requirements.md:8 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate requested feature with its owning workflow | requirements.md:8 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Requested feature is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Requested feature | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Requested feature | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide requested feature |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide requested feature | Validated requested feature |
