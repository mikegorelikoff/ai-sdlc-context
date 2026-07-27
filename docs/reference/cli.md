# CLI reference

This page lists the top-level commands exposed by Context Guard `0.1.1`.
Run `context-guard <command> --help` for nested actions and arguments.

| Command | Contract |
| --- | --- |
| `hook {claude,codex}` | Process one provider hook event. |
| `install {claude,codex}` | Add idempotent hook configuration for one provider. |
| `validate` | Validate the packaged policy. |
| `selftest` | Evaluate bundled fixtures with enforced expected decisions. |
| `doctor` | Report Python, policy, and provider installation state. |
| `report` / `gain` | Summarize local audit and compact-runtime evidence. |
| `inventory` | Inventory supported provider skill metadata and digests. |
| `receipt` | Inspect, delete, or prune local receipts. |
| `claude-profile` | Plan, apply, restore, or recover a Claude skill profile. |
| `codex-profile` | Plan, apply, restore, or recover a Codex skill profile. |
| `quality` | Manage frozen-fixture quality evidence. |
| `claude-measurement` | Manage Claude measurement evidence. |
| `codex-measurement` | Manage Codex measurement evidence. |
| `test -- <command>` | Run a test command and retain full evidence. |
| `run -- <command>` | Run an explicit command through compact output. |
| `artifact show` | Retrieve a complete artifact or one fragment. |

There is no `context-guard sessions` command in version `0.1.1`.

Exit behavior is command-specific. Validation, self-test, missing artifacts,
invalid inputs, and wrapped command failures return nonzero results. `run`
preserves the wrapped command exit code.
