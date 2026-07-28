# Prerequisites

Check these requirements before installing Context Guard.

- macOS or Linux.
- Bash and `curl`.
- A supported package manager when Python 3.10+ with `venv` is missing:
  Homebrew, APT, DNF, YUM, APK, Pacman, or Zypper.
- Claude Code, Codex, or both.
- Permission to write under `~/.local/`, `~/.claude/`, and `~/.codex/`.
- Root access or `sudo` when the selected Linux package manager requires it.
- A reviewed working tree where `.context-guard/` evidence can be stored.

Verify the tools:

```bash
bash --version
curl --version
python3 --version
git status --short
```

The installer checks for a compatible Python first. When it is missing, or
when `venv` cannot be created, the installer uses the detected supported
package manager to install the system dependency. It downloads the Context
Guard package through pip unless
`CONTEXT_GUARD_PACKAGE` points to a local source checkout. The recommended path
sets it to the reviewed clone.

Next, [install and initialize the hooks](install.md).
