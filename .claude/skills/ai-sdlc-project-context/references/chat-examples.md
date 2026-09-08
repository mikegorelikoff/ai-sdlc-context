# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared context fact result; evidence supports the reported result. | fixture.toon:1 |

| Context fact | Value | Source | Freshness | Use |
| --- | --- | --- | --- | --- |
| Test command | pytest tests/payments | pyproject.toml:20 | Current | Verify AC-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate repository root with its owning workflow | fixture.toon:1 |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | fixture.toon:1 |

| Context fact | Value | Source | Freshness | Use |
| --- | --- | --- | --- | --- |
| Test command | pytest tests/payments | pyproject.toml:20 | Current | Verify AC-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate repository root with its owning workflow | fixture.toon:1 |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Repository root is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Repository root | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Repository root | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide repository root |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide repository root | Validated repository root |
