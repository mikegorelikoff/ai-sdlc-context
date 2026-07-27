# Context Guard

Stop predictable context waste before it reaches the active model context while
preserving full local evidence for later inspection.

[![CI](https://github.com/mikegorelikoff/ai-sdlc-context/actions/workflows/ci.yml/badge.svg)](https://github.com/mikegorelikoff/ai-sdlc-context/actions/workflows/ci.yml)
[![Documentation](https://github.com/mikegorelikoff/ai-sdlc-context/actions/workflows/docs.yml/badge.svg)](https://github.com/mikegorelikoff/ai-sdlc-context/actions/workflows/docs.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

Context Guard is a local hook and compact-output tool for Claude Code and Codex.
It observes policy-relevant file reads, commands, and searches; compacts
supported command output; and retains full evidence under the working
repository. The packaged policy starts in observe mode.

## Why use it?

- See predictable context-risk events before choosing enforcement.
- Keep full command and test evidence outside the active model context.
- Inspect local audit, artifact, receipt, profile, and measurement records.
- Roll out from observe to warn to enforce with explicit review.

## Quick start

Review a local clone, then install from that source:

```bash
git clone https://github.com/mikegorelikoff/ai-sdlc-context.git
cd ai-sdlc-context
CONTEXT_GUARD_PACKAGE="$PWD" ./install.sh
context-guard validate
context-guard selftest
context-guard report
```

The installer creates a private virtual environment, installs the CLI, and
initializes Claude Code and Codex hooks. It modifies user configuration; read
the [installation guide](docs/start-here/install.md) before running it.

## Expected first result

`validate` reports one policy source beginning with `packaged:`. `selftest`
prints a fixture summary with no `FAIL` lines. `report` returns JSON; before
normal use it may report zero events. That is a valid empty baseline.

## Product workflow

```text
Observe → Warn → Enforce → Compact → Inspect
```

Stage 1 evaluates hook events and records what policy would allow, warn about,
or block. Stage 2 runs supported commands through a compact-output path, sends
the bounded result onward, and keeps complete stdout, stderr, metadata, and
failure fragments locally.

## What it does and does not do

Context Guard applies its packaged policy to recognized events and provides an
explicit proxy for commands. It does not intercept every provider operation,
rewrite compound or mutating shell commands, change model-provider behavior,
or guarantee lower billing. Output byte reductions and the `bytes / 4` token
estimate are local evidence, not provider-reported token or cost measurements.

## Documentation paths

- [Start here](docs/start-here/index.md) for prerequisites, install, validation,
  self-test, and first report.
- [How it works](docs/how-it-works/index.md) for Stage 1, Stage 2, rollout, and
  trust boundaries.
- [Guides](docs/guides/index.md) for safe rollout, compact commands, examples,
  evidence inspection, and advanced measurement.
- [Reference](docs/reference/index.md) for CLI, policy, receipts, artifacts,
  profiles, parsers, files, and compatibility.
- [Project](docs/project/index.md) for status, limitations, privacy, security,
  decisions, and contribution.

## AI SDLC product family

**Structure delivery. Control context. Measure adoption.**

- [AI SDLC Harness](https://github.com/mikegorelikoff/ai-sdlc-harness)
  structures AI-assisted software delivery.
- **Context Guard — current:** controls avoidable context growth and retains
  full evidence locally.
- [AI SDLC Metrics](https://github.com/mikegorelikoff/ai-sdlc-metrics)
  measures local Codex CLI and Claude Code adoption from available evidence.

The products are complementary and independently installed. This repository
does not claim a built-in technical integration with the other two.

## Security and privacy

Context Guard does not upload its audit, artifact, receipt, profile, or
measurement records. Full captured output can still contain source, paths,
logs, test data, or secrets, so protect `.context-guard/` as sensitive local
evidence. Executed commands, agent hosts, package installers, and model
providers retain their own network and data behavior. Report vulnerabilities
through [SECURITY.md](SECURITY.md).

## Project status

The package version is `0.1.1`. The packaged version 2 policy is fixed to
observe mode and is not overridden by repository files, user files, or
environment variables. Review [limitations](docs/project/status-limitations.md)
before advancing beyond an evaluation.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Run:

```bash
python3 tests/run_pytest.py -q
python3 docs/scripts/validate_docs.py
python3 -m unittest discover -s docs/tests -v
mkdocs build --strict
```

## License

Licensed under the [Apache License 2.0](LICENSE).
