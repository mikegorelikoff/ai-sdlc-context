# Prerequisites

Check these requirements before installing Context Guard.

- macOS or Linux.
- Bash and `curl`.
- Python 3.10 or newer with `venv`.
- Claude Code, Codex, or both.
- Permission to write under `~/.local/`, `~/.claude/`, and `~/.codex/`.
- A reviewed working tree where `.context-guard/` evidence can be stored.

Verify the tools:

```bash
bash --version
curl --version
python3 --version
git status --short
```

The installer downloads packages through pip unless
`CONTEXT_GUARD_PACKAGE` points to a local source checkout. The recommended path
sets it to the reviewed clone. Context Guard does not use `sudo`.

Next, [install and initialize the hooks](install.md).
