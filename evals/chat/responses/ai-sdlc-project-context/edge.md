| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared value / source entities; listed evidence satisfies this skill check. | fixture.toon:1 |

| Context fact | Value | Source | Freshness | Use |
| --- | --- | --- | --- | --- |
| Test command &#124; перенос<br>строки | pytest tests/payments | pyproject.toml:20 | Current | Verify AC-001 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate repository root with its owning workflow | fixture.toon:1 |

```toon
schema: fixture/v1
status: pending
source: "literal | value"
```
