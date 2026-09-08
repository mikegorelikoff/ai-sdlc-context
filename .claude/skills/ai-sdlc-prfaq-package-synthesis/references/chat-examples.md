# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PENDING | Prepared customer result; owner decision or execution remains pending. | fixture.toon:1 |

| Customer | Problem | Proposed outcome | Business evidence | Open decision |
| --- | --- | --- | --- | --- |
| Operator | Manual duplicate refunds | One charge per request key | interview.md:12 | Retry window |

| FAQ topic | Answer | Evidence | Unresolved choice |
| --- | --- | --- | --- |
| Payment retries | A retry reuses the original payment identity | fixture.toon:1 | None within approved retry scope |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate validated discovery with its owning workflow | fixture.toon:1 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| Customer | Problem | Proposed outcome | Business evidence | Open decision |
| --- | --- | --- | --- | --- |
| Operator | Manual duplicate refunds | One charge per request key | interview.md:12 | Retry window |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Validate validated discovery with its owning workflow | fixture.toon:1 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Validated discovery is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Validated discovery | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Validated discovery | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide validated discovery |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Product owner | Provide validated discovery | Validated validated discovery |
