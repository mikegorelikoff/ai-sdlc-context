# Troubleshooting

Use this page for first-run installation, validation, self-test, and report
failures.

## Command not found

Run `~/.local/bin/context-guard --help`. Add `~/.local/bin` to `PATH` only if
that location matches the installer output.

## Policy does not validate

Run `context-guard validate`. Version `0.1.1` loads the single packaged policy;
user, repository, and environment overrides are not supported. Reinstall from
the reviewed source instead of creating an undocumented local policy.

## Self-test reports a failure

Record the exact failing fixture and installed version. Do not advance rollout
mode. Run the repository product tests from a source checkout before reporting
the defect.

## Report is empty

An empty report is valid before applicable hook or compact-runtime activity.
Run `context-guard run -- git status`, then rerun `context-guard report` from
the same repository.

## Provider hooks are missing

Run `context-guard doctor`. Re-run only the required initializer:

```bash
context-guard install claude
context-guard install codex
```

Each command is idempotent but modifies its provider configuration. Preserve
unrelated settings.

If the issue persists, collect nonsensitive diagnostics and follow the
[contribution path](../project/contributing.md).
