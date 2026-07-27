# Install and initialize

This guide installs Context Guard from reviewed local source and initializes
Claude Code and Codex hooks.

## Goal

Install the `context-guard` CLI and connect both supported provider
configurations while retaining the packaged observe policy.

## When to use it

Use this for a first evaluation or a repeatable update from a source checkout.

## Prerequisites

Complete the [prerequisites](prerequisites.md) and review `install.sh`.

## Procedure

```bash
git clone https://github.com/mikegorelikoff/ai-sdlc-context.git
cd ai-sdlc-context
CONTEXT_GUARD_PACKAGE="$PWD" ./install.sh
```

The script creates `~/.local/share/context-guard/venv`, links
`~/.local/bin/context-guard`, runs `context-guard install claude`, runs
`context-guard install codex`, and validates the policy. It preserves unrelated
configuration and is designed to be repeatable.

If `~/.local/bin` is not on `PATH`, add it for the current shell:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Verify

```bash
context-guard validate
context-guard doctor
```

`validate` must identify one policy source beginning with `packaged:`.
`doctor` reports Python, policy, and provider installation status.

## Troubleshooting

If the command is not found, use the full path printed by the installer. If a
provider config cannot be changed, stop and restore it from your normal
configuration backup process; do not delete unrelated settings.

## Next step

Run the [first self-test and report](first-run.md).

### Optional remote convenience

The remote pipeline is shorter but executes a changing script from the
repository default branch:

```bash
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-context/main/install.sh | bash
```

Use it only after reviewing that exact script and accepting the GitHub and pip
trust boundary.
