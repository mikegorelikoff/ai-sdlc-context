| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | design.md:42 |

| Component | Responsibility | Decision | Dependency | Evidence |
| --- | --- | --- | --- | --- |
| Retry worker | Deduplicate deliveries | Reuse ledger | Payment store | design.md:42 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate architecture constraint with its owning workflow | design.md:42 |
