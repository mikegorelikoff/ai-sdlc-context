# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PENDING | Prepared stage result; owner decision or execution remains pending. | fixture.toon:1 |

| Stage | Owning skill | Eligibility | Dependency | Expected artifact |
| --- | --- | --- | --- | --- |
| Verification | ai-sdlc-validation | Deferred | Implementation evidence | validation.md |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate workflow intent with its owning workflow | fixture.toon:1 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| Stage | Owning skill | Eligibility | Dependency | Expected artifact |
| --- | --- | --- | --- | --- |
| Verification | ai-sdlc-validation | Deferred | Implementation evidence | validation.md |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate workflow intent with its owning workflow | fixture.toon:1 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Workflow intent is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Workflow intent | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Workflow intent | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide workflow intent |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide workflow intent | Validated workflow intent |
