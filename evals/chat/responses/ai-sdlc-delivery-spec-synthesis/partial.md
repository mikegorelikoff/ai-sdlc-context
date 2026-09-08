| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Partial result: second case is unverified; do not infer full coverage. | ST-001 |

| Requirement ID | Behavior | Interface | Constraint | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 | Return prior charge for same key | POST /payments | One charge per key | ST-001 |
| AC-001 | Return prior charge for same key [pending case] | POST /payments | One charge per key | ST-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate accepted story with its owning workflow | ST-001 |
