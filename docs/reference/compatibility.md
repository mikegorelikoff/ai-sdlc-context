# Compatibility

Context Guard `0.1.1` requires Python 3.10 or newer. The installer targets
macOS or Linux with Bash, curl, Python `venv`, and user-level write access.

The CLI supports Claude Code and Codex provider adapters. Inventory and profile
actions apply provider-version and surface preflight checks defined in source.
Do not infer compatibility for an unlisted provider, version, or hook surface.

Recognized compact command families include selected Git/GitHub, files/search,
tests, builds, checks, linters, packages, containers, infrastructure, and
system-inspection commands. `context-guard run -- ...` accepts other explicit
commands through generic bounded compaction, but transparent hook rewriting is
limited to the registry and leaves compound or mutating/deployment operations
unchanged.

Run `context-guard doctor` and the relevant `--help` command against the
installed version before rollout.
