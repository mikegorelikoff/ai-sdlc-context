# Compact command output

## Goal

Return bounded active output while preserving the complete command evidence
locally.

## When to use it

Use it for logs, searches, tests, builds, linters, package inspection, and
other commands whose full output is not needed immediately.

## Prerequisites

Install Context Guard and run `context-guard selftest`.

## Procedure

```bash
context-guard run -- git status
context-guard run -- git diff
context-guard run -- rg "pattern" src
context-guard test -- pytest
```

The explicit proxy accepts any supplied command. Recognized families receive
specialized filtering; other commands use generic bounded compaction.

## Verify

Check the command exit status and the emitted artifact ID. Run
`context-guard report` and confirm that `compact_runtime.invocations` changed.
For a failure, inspect the exact stored fragment before deciding to rerun.

## Troubleshooting

If a compound shell expression is not rewritten by a provider hook, invoke the
proxy explicitly with a single command. Do not use Context Guard to bypass
normal approval requirements for mutating commands.

## Next step

[Inspect the complete artifact](inspect-evidence.md).
