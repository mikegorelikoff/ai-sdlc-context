| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared component result; evidence supports the reported result. | design.md:42 |

| Component | Responsibility | Decision | Dependency | Evidence |
| --- | --- | --- | --- | --- |
| Retry worker | Deduplicate deliveries | Reuse ledger | Payment store | design.md:42 |

| Decision ID | Alternative | Consequence | Evidence |
| --- | --- | --- | --- |
| DEC-001 | Create a separate retry queue | Adds an independently operated component | design.md:42 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate architecture constraint with its owning workflow | design.md:42 |
