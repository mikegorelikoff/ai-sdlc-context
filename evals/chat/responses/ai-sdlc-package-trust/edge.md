| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared expected / observed entities; listed evidence satisfies this skill check. | manifest.json |

| Control | Expected | Observed | Decision | Evidence |
| --- | --- | --- | --- | --- |
| Archive checksum &#124; перенос<br>строки | Published SHA-256 | Matching digest | PASS | manifest.json |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate package manifest with its owning workflow | manifest.json |

```toon
schema: fixture/v1
status: pending
source: "literal | value"
```
