| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared behavior / interface entities; listed evidence satisfies this skill check. | ST-001 |

| Requirement ID | Behavior | Interface | Constraint | Evidence |
| --- | --- | --- | --- | --- |
| AC-001 &#124; перенос<br>строки | Return prior charge for same key | POST /payments | One charge per key | ST-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate accepted story with its owning workflow | ST-001 |

```toon
schema: fixture/v1
status: pending
source: "literal | value"
```
