# Quality runner

Context Guard permits token measurement only after a frozen baseline/guarded
pair passes deterministic quality gates. The runner evaluates sanitized
evidence; it does not launch Claude Code or Codex, execute fixture commands, or
accept token counts.

## Frozen suite

A qualification suite contains exactly one manifest for each fixture kind:

- `read-only-analysis`
- `test-only-change`
- `explicit-ai-sdlc-skill`

Each versioned manifest fixes the provider and version, model, repository and
task fingerprints, baseline and guarded profile fingerprints, and required
instruction IDs. Validate the suite before collecting attempts:

```bash
context-guard quality validate-suite \
  fixtures/read.json fixtures/test.json fixtures/skill.json
```

Manifest and attempt JSON use exact schemas. Unknown fields—including prompt,
source, output, and token fields—are rejected before persistence.

## Evaluate a pair

Collect baseline and guarded evidence in separate fresh sessions, then run:

```bash
context-guard quality evaluate \
  --manifest fixtures/skill.json \
  --baseline evidence/skill-baseline.json \
  --guarded evidence/skill-guarded.json \
  --run-id skill-pair-evaluation
```

The evaluator applies these hard gates:

| Gate | Required evidence |
| --- | --- |
| QG-301 | Valid exact manifest schema |
| QG-302 | One correlated baseline and guarded attempt |
| QG-303 | Provider, version, model, repository, task, and profile fingerprints match |
| QG-304 | Both attempts used fresh sessions |
| QG-305 | Both completion oracles passed |
| QG-306 | Both attempts preserved every required instruction |
| QG-307 | The explicit-skill fixture invoked the required skill |
| QG-308 | Both attempts passed restoration checks |
| QG-309 | Both attempts reference valid privacy-safe receipts |

Every result—passing or failing—is appended to the private
`.context-guard/quality/ledger.jsonl`. A passing pair is authorized only when it
has exactly one valid evaluation and no invalidation:

```bash
context-guard quality authorize PAIR_ID
```

Missing, corrupt, ambiguous, failed, or unrecognized evidence denies
measurement. It never substitutes zero token values.

## QA invalidation

QA can revoke a formerly valid pair without rewriting prior evidence:

```bash
context-guard quality invalidate PAIR_ID \
  --run-id qa-revocation-1 \
  --reason qa-oracle-regression
```

Evaluation and invalidation write sanitized decision receipts. The ledger and
receipts contain identifiers, fingerprints, gate outcomes, and action results;
they do not contain raw task text, source, provider output, or token data.
