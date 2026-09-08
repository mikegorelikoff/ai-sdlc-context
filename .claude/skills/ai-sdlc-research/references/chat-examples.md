# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared question result; evidence supports the reported result. | schema.sql:18 |

| Question | Finding | Confidence | Limitation | Evidence |
| --- | --- | --- | --- | --- |
| Can ledger deduplicate retries? | Unique key already stored | High | Retention window unknown | schema.sql:18 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate research question with its owning workflow | schema.sql:18 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | schema.sql:18 |

| Question | Finding | Confidence | Limitation | Evidence |
| --- | --- | --- | --- | --- |
| Can ledger deduplicate retries? | Unique key already stored | High | Retention window unknown | schema.sql:18 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate research question with its owning workflow | schema.sql:18 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Research question is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Research question | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Research question | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide research question |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide research question | Validated research question |
