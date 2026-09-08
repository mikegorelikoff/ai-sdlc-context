# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared control result; evidence supports the reported result. | manifest.json |

| Control | Expected | Observed | Decision | Evidence |
| --- | --- | --- | --- | --- |
| Archive checksum | Published SHA-256 | Matching digest | PASS | manifest.json |

| Metric | Count | Evidence |
| --- | --- | --- |
| Controls evaluated | 1 | manifest.json |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate package manifest with its owning workflow | manifest.json |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | manifest.json |

| Control | Expected | Observed | Decision | Evidence |
| --- | --- | --- | --- | --- |
| Archive checksum | Published SHA-256 | Matching digest | PASS | manifest.json |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate package manifest with its owning workflow | manifest.json |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Package manifest is unavailable; dependent work has not run. | source-inventory.toon:missing |

| Package manifest | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| Package manifest | BLOCKED | Required source is absent | source-inventory.toon:missing | Provide package manifest |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Provide package manifest | Validated package manifest |
