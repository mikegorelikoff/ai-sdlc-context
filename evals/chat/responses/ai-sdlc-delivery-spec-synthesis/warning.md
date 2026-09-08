| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Result has limited source freshness; confirm it before downstream use. | ST-001 |

| Requirement ID | Behavior | Interface | Constraint | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 | Return prior charge for same key | POST /payments | One charge per key | ST-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate accepted story with its owning workflow | ST-001 |
