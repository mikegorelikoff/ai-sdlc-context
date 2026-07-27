# Evaluate measurement evidence

## Goal

Use Context Guard's advanced provider measurement paths without overstating
what the evidence proves.

## When to use it

Use it after normal observe-mode and compact-runtime evaluation, when you need
controlled Claude Code or Codex baseline/guarded comparisons.

## Prerequisites

Read the [parser and measurement contracts](../reference/parsers-measurement.md)
and preserve provider version, surface, policy, inventory, receipt, and quality
correlation.

## Procedure

Inspect the exact command groups for the installed version:

```bash
context-guard claude-measurement --help
context-guard codex-measurement --help
```

Use repository fixtures first. For provider runs, pair baseline and guarded
evidence under the same declared task and preserve the generated receipts.
Counterbalance execution order across repeated pairs when making a consistency
claim.

## Verify

- **Fixture evidence** proves expected behavior for known inputs.
- **Single-pair evidence** describes one correlated baseline/guarded pair.
- **Repeated evidence** supports a stronger consistency assessment when pair
  identity, order, provider version, and quality gates remain valid.

None of these is provider-reported billing evidence or proof of model-quality
improvement.

## Troubleshooting

Treat missing receipts, corrupt ledgers, fingerprint mismatches, and failed
quality gates as invalid evidence. Do not reconstruct missing fields by guess.

## Next step

Record the limitation and return to [safe rollout](safe-rollout.md) before
changing packaged policy.
