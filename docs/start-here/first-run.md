# Run and verify Context Guard

This guide validates the packaged policy, exercises bundled fixtures, and
inspects the first report without requiring enforcement.

## Goal

Prove that the installation is usable and establish a local observe-mode
baseline.

## When to use it

Use it immediately after installation and after a Context Guard update.

## Prerequisites

Complete [Install and initialize](install.md).

## Procedure

From a working repository:

```bash
context-guard validate
context-guard selftest
context-guard report
```

Then exercise the explicit compact proxy with a read-only command:

```bash
context-guard run -- git status
context-guard report
```

## Verify

- `validate` lists one `packaged:` policy source.
- `selftest` ends with all fixtures passed and contains no `FAIL`.
- `run` returns bounded `git status` output and preserves its exit status.
- `report` returns JSON with event and compact-runtime summaries. Zero values
  are valid when no applicable event has been observed.

## Troubleshooting

Use `context-guard doctor` for installation and policy diagnostics. Check that
you ran the command from the repository whose `.context-guard/` records you
want to inspect.

## Next step

Follow the [safe rollout guide](../guides/safe-rollout.md), or learn how
[Stage 1 and Stage 2](../how-it-works/stages.md) differ.
