| Status | Decision | Evidence |
| --- | --- | --- |
| PENDING | Prepared state / attempts entities; owner decision or execution remains pending. | state.toon:15 |

| Task ID | State | Attempts | Evidence | Next transition |
| --- | --- | --- | --- | --- |
| T001 &#124; перенос<br>строки | ready | 0 / 2 | state.toon:15 | Claim task |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Maintainer | Validate run identity with its owning workflow | state.toon:15 |

```toon
schema: fixture/v1
status: pending
source: "literal | value"
```
