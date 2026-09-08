# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared observation result; evidence supports the reported result. | incident.md:8 |

| Observation | Evidence | Improvement proposal | Decision status | Owner |
| --- | --- | --- | --- | --- |
| Retries lack scenario coverage | incident.md:8 | Add replay fixture | Proposed | QA |

| Proposal | Decision reference | Next action | Owner |
| --- | --- | --- | --- |
| Add concurrency check to the retry suite | DEC-001 | Add TC-002 concurrency coverage | QA |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate observation evidence with its owning workflow | incident.md:8 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | incident.md:8 |

| Observation | Evidence | Improvement proposal | Decision status | Owner |
| --- | --- | --- | --- | --- |
| Retries lack scenario coverage | incident.md:8 | Add replay fixture | Proposed | QA |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate observation evidence with its owning workflow | incident.md:8 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Observation evidence is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Observation evidence | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Observation evidence | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide observation evidence |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide observation evidence | Validated observation evidence |
