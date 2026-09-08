| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Partial result: second case is unverified; do not infer full coverage. | design.md:42 |

| Component | Responsibility | Decision | Dependency | Evidence |
| --- | --- | --- | --- | --- |
| Retry worker | Deduplicate deliveries | Reuse ledger | Payment store | design.md:42 |
| Retry worker [pending case] | Deduplicate deliveries | Reuse ledger | Payment store | design.md:42 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate architecture constraint with its owning workflow | design.md:42 |
