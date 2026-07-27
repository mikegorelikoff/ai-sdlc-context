# Context Guard

[![CI](https://github.com/mikegorelikoff/ai-sdlc-context/actions/workflows/ci.yml/badge.svg)](https://github.com/mikegorelikoff/ai-sdlc-context/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

Context Guard is a local, deterministic hook engine for Claude Code and Codex. It prevents common operations that waste context tokens: complete reads of oversized or generated files, unbounded log/history commands, and repository-wide searches without a path or result limit.

It sends no data to a proxy, vector database, or centralized collector.

## Requirements

- macOS or Linux
- Bash
- `curl`
- Python 3.10 or newer with `venv`
- Claude Code, Codex, or both

## Install

Run:

```bash
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-context/main/install.sh | bash
```

The installer:

1. Creates a private Python environment at `~/.local/share/context-guard/venv`.
2. Creates `~/.local/bin/context-guard`.
3. Adds Context Guard hooks to `~/.claude/settings.json`.
4. Adds Context Guard hooks to `~/.codex/config.toml`.
5. Validates the installed policy.

It does not use `sudo`. It preserves unrelated Claude and Codex configuration and is safe to run again.

If `~/.local/bin` is not on `PATH`, add it:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Verify

```bash
cd "$HOME"
context-guard validate
context-guard doctor
context-guard selftest
```

`validate` must report one policy source whose name starts with `packaged:`. `doctor` reports the Python version, policy status, and installation status for both providers.

## The one policy

Context Guard has exactly one policy: [`context_guard/defaults/policy.yaml`](context_guard/defaults/policy.yaml). User files, repository files, and environment variables do not override it.

```yaml
version: 2
mode: observe

files:
  max_full_read_bytes: 200000
  require_range_above_bytes: 50000
  deny:
    - "**/node_modules/**"
    - "**/vendor/**"
    - "**/dist/**"
    - "**/build/**"
    - "**/coverage/**"
    - "**/.git/**"
    - "**/*.min.js"
    - "**/*.map"
    - "**/package-lock.json"
    - "**/yarn.lock"
    - "**/pnpm-lock.yaml"
    - "**/Cargo.lock"

commands:
  maximum_expected_output_lines: 500
  require_bounds:
    - "docker logs"
    - "docker compose logs"
    - "kubectl logs"
    - "git log"

search:
  require_path_scope: true
  maximum_results: 100

fail_closed_rules: []

skills:
  rules: []
```

`observe` records what the policy would prevent without blocking the agent. The policy is shipped with the package and changes only when Context Guard is updated.

## Use

Hooks call Context Guard automatically. These commands are for direct inspection and compact execution:

```bash
context-guard report
context-guard gain
context-guard sessions
context-guard run -- git status
context-guard run -- git diff
context-guard run -- rg "pattern" src
context-guard run -- docker logs api
context-guard run -- pytest
context-guard inventory --provider claude --version 2.1.218 --surface cli
context-guard inventory --provider codex --version 0.144.1 --surface cli
context-guard test -- pytest
context-guard artifact show <artifact-id>
context-guard artifact show <artifact-id> --fragment <fragment-id>
```

`gain` and `report` include local raw-output bytes, compact-output bytes, the reduction percentage, and an estimate of input tokens saved using `bytes / 4`. This is output-reduction evidence, not a provider-reported token count or an estimate of billing reduction.

Compact test output is failure-first. The complete stdout, stderr, metadata, and exact failure fragments remain available through the reported artifact ID, so an agent can recover evidence without rerunning the command.

For Claude Code Bash calls, the installed `PreToolUse` hook transparently rewrites supported commands to `context-guard run -- ...`. Codex can call the same proxy directly.

| Family | Supported commands |
| --- | --- |
| Git/GitHub | `git status/log/diff/show`; read-only `gh pr/issue/run/workflow/release` list, view, status, and checks |
| Files/search | `ls`, `tree`, `cat`, `head`, `tail`, `wc`, `du`, `df`, `ps`, `rg`, `grep`, `find`, `fd`, `ag`, `ack` |
| Tests | Pytest, Jest, Vitest, RSpec, Cargo test, Go test, npm/pnpm/yarn test, Playwright |
| Build/check | Cargo, Go, make, CMake, Ninja, npm/pnpm/yarn build/check/typecheck, .NET, Maven, Gradle, SBT |
| Lint | Ruff, mypy, TypeScript, ESLint, Biome, Prettier, RuboCop, golangci-lint |
| Packages | pip and uv list/show/check, Cargo tree/metadata, npm/pnpm/yarn list/outdated |
| Containers | Docker ps/images/logs/stats/compose ps/logs; Kubernetes get/describe/logs/top |
| Infrastructure | Terraform plan/show/validate/output, Pulumi preview/stack, read-only AWS describe/get/list operations |

Additional automatic families include Python module test/lint commands, Bun, Deno, Poetry, Bundler/Rake, Swift/Xcode, Podman/OpenShift, Helm, Terragrunt, Azure CLI and Google Cloud read operations, journal/system status, and Homebrew/APT/dpkg inspection.

Language coverage:

- .NET: `dotnet test/build/format/list/msbuild`, `msbuild`, and `csc`.
- Java/JVM: Maven/Maven Wrapper `test/package/verify/dependencies`, Gradle/Gradle Wrapper `test/build/check/dependencies`, SBT `test/compile`, `javac`, and `javadoc`.
- JavaScript/TypeScript: npm, pnpm, Yarn, Bun, Deno, Node test/check, Jest, Vitest, Playwright, Cypress, Mocha, AVA, TypeScript, ESLint, Biome, and Prettier.
- Go: `go test/build/vet/list/version/env`, read-only `gofmt -d/-l`, staticcheck, govulncheck, and golangci-lint.

`context-guard run -- ...` accepts any explicitly supplied command and applies generic bounded compaction when no specialized filter exists. Transparent hook rewriting uses only the recognized registry. Compound shell expressions and mutating/deployment commands such as `git push`, package installation, `terraform apply`, and `pulumi up` are left unchanged.

The inventory commands read skill metadata from `~/.claude/skills` and `~/.agents/skills`. They emit identities and digests, not raw skill instructions.

## Reproducible examples

The repository includes local fixtures for positive reductions, regressions, cumulative token accounting, profile apply/restore, fail-closed cases, and privacy checks:

```bash
git clone https://github.com/mikegorelikoff/ai-sdlc-context.git
cd ai-sdlc-context
python3 examples/run_demo.py --check
```

The checked output is stored in [`examples/output/demo-output.json`](examples/output/demo-output.json).

## Update

Run the installation command again:

```bash
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-context/main/install.sh | bash
```

## Uninstall

Remove Context Guard hook entries containing `context-guard` from:

- `~/.claude/settings.json`
- `~/.codex/config.toml`

Then remove the installed files:

```bash
rm -f "$HOME/.local/bin/context-guard"
rm -rf "$HOME/.local/share/context-guard"
```

## Project

- Bugs and changes: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security reports: [SECURITY.md](SECURITY.md)
- License: [Apache-2.0](LICENSE)
