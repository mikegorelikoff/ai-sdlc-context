| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Prepared actor / behavior entities; listed evidence satisfies this skill check. | wireframe.md:18 |

| Journey / state | Actor | Behavior | Recovery | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- |
| Payment timeout &#124; перенос<br>строки | Operator | Show pending charge | Retry with same key | AC-002 | wireframe.md:18 |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Engineer | Validate journey actor with its owning workflow | wireframe.md:18 |

```toon
schema: fixture/v1
status: pending
source: "literal | value"
```
