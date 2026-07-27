# Files and environment

This page lists the installation and repository-local paths used by Context
Guard.

| Path | Purpose |
| --- | --- |
| `~/.local/share/context-guard/venv` | Installed private Python environment |
| `~/.local/bin/context-guard` | CLI link |
| `~/.claude/settings.json` | Claude Code hook configuration |
| `~/.codex/config.toml` | Codex hook configuration |
| `.context-guard/audit.jsonl` | Local policy audit records |
| `.context-guard/artifacts/` | Full compact-output evidence |
| `.context-guard/ledger.sqlite` | Compact invocation ledger |
| `.context-guard/receipts/` | Correlation receipts |
| `.context-guard/profiles/` | Profile state and recovery data |
| `.context-guard/quality/` | Quality evidence |
| `.context-guard/measurements/` | Claude measurement ledger |
| `.context-guard/measurements-codex/` | Codex measurement ledger |

Installer environment overrides are `CONTEXT_GUARD_INSTALL_ROOT`,
`CONTEXT_GUARD_BIN_DIR`, `CONTEXT_GUARD_CONFIG_ROOT`, and
`CONTEXT_GUARD_PACKAGE`.

`CONTEXT_GUARD_MODE` and local policy files do not override the packaged policy
in version `0.1.1`.
