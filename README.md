# Context Guard

[![CI](https://github.com/mikegorelikoff/ai-sdlc-context/actions/workflows/ci.yml/badge.svg)](https://github.com/mikegorelikoff/ai-sdlc-context/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A local, deterministic hook-based policy engine that reduces avoidable context growth in Claude Code and Codex agent sessions — no proxy, vector database, or centralized data collector.

## Install

```bash
git clone https://github.com/mikegorelikoff/ai-sdlc-context.git
cd ai-sdlc-context
pipx install .
# or
uv tool install .
```

## Quickstart

```bash
# In your repository:
context-guard init             # creates .context-guard/policy.yaml (starts in observe mode)
context-guard install claude   # wires Context Guard into Claude Code hooks
context-guard install codex    # wires Context Guard into Codex hooks
context-guard validate         # checks policy schema + hook install status
context-guard test             # runs the bundled fixture smoke tests
```

## CLI reference

| Command | Purpose |
| --- | --- |
| `context-guard hook <claude\|codex>` | Invoked by the provider's hook runtime; reads a JSON payload on stdin and writes a decision to stdout. Not typically run by hand. |
| `context-guard install <claude\|codex>` | Adds (idempotently) the required hook entries to the provider's local config. |
| `context-guard validate` | Validates the resolved policy configuration; non-zero exit on error. |
| `context-guard test` | Runs the bundled fixture-based smoke tests covering the required high-cost patterns. |
| `context-guard doctor` | Reports Python version, resolved policy layer chain, and hook install status. |
| `context-guard report` | Summarizes the local JSONL audit log into a prevented-context estimate. |
| `context-guard init` | Creates a default repo-level `.context-guard/policy.yaml` (never overwrites an existing one). |

## Rollout recommendation

```text
Week 1: observe  — measure what would be blocked, tune the policy
Week 2: warn     — surface warnings without blocking
Week 3+: enforce — block for the rule groups that proved low-noise
```

See `docs/policy.md` for the full policy schema and `specs/001-context-guard/` for the requirements, design, and test-case package this implementation was built from.

## Contributing

Bug reports and PRs are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Report security issues per [SECURITY.md](SECURITY.md) rather than a public issue.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
