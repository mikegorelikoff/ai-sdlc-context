# Inspect retained evidence

## Goal

Recover complete output or one exact failure fragment after seeing a compact
result.

## When to use it

Use it when a compact command reports an artifact ID or fragment ID.

## Prerequisites

Run a command through `context-guard run` or `context-guard test` from the
repository where evidence should be stored.

## Procedure

```bash
context-guard artifact show <artifact-id>
context-guard artifact show <artifact-id> --fragment <fragment-id>
context-guard report
```

Artifacts are stored beneath `.context-guard/artifacts/`; the compact ledger is
`.context-guard/ledger.sqlite`.

## Verify

The full artifact view prints retained stdout, stderr, and available native
test output. A fragment view prints the exact indexed fragment. A missing ID
returns a nonzero result and `Not found`.

## Troubleshooting

Run the command from the same repository root used to create the artifact.
Protect retained output as sensitive local evidence and do not attach it to an
issue without review.

## Next step

Review [files and environment](../reference/files-environment.md) for the full
local storage map.
