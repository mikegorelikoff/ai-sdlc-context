# Trust boundaries

This page identifies what Context Guard keeps local, what it changes, and what
remains outside its control.

## What stays local

Context Guard writes repository-local records under `.context-guard/`,
including audit JSONL, compact artifacts, a SQLite invocation ledger, receipts,
profiles, quality evidence, and measurement ledgers. Audit records hash raw
commands or paths by default. Compact artifacts retain complete captured
stdout and stderr, which may contain sensitive content.

## User configuration changes

The installer creates a private environment under
`~/.local/share/context-guard`, a command under `~/.local/bin`, and hook entries
under `~/.claude/settings.json` and `~/.codex/config.toml`. When Python 3.10+
or `venv` is missing, it can also invoke a detected system package manager;
that step may request `sudo` and changes system-managed packages.

## What Context Guard does not control

- Network behavior of the executed command.
- Data handling by Claude Code, Codex, model providers, GitHub, or pip.
- Operations a provider does not expose through a supported hook.
- Compound, mutating, or deployment commands left unchanged by transparent
  rewriting.
- Secrets already present in source, logs, environment, or tool output.
- Provider token accounting, billing, model quality, or business outcomes.

Context Guard itself does not upload its local evidence records. That statement
does not imply that the surrounding tools are offline.

Next, review [security and privacy](../project/security-privacy.md).
