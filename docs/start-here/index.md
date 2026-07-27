# Start here

Use this section to run the one-line installer, initialize provider hooks,
validate the packaged policy, run the bundled self-test, and inspect the first
local report. A reviewable local-clone path remains available when your trust
policy does not permit remote shell pipelines.

## Recommended path

1. Check the [prerequisites](prerequisites.md).
2. [Run the one-line installer](install.md) in the default observe mode.
3. Follow the [first run](first-run.md).
4. Read [safe rollout](../guides/safe-rollout.md) before considering warn or
   enforce.
5. Keep [troubleshooting](troubleshooting.md) available for configuration and
   path failures.

Observe mode is the safe default because it records applicable decisions
without blocking operations. You do not need to understand profiles,
measurement ledgers, or parser internals for the first run.

For exact commands and files, use [Reference](../reference/index.md).
