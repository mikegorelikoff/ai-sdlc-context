---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-simple-install-policy-docs"
  artifact: "requirements.md"
  path: "specs/005-simple-install-policy-docs/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/005-simple-install-policy-docs/_ai_sdlc/state.toon"
  decision_log: "specs/005-simple-install-policy-docs/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "AC-009"
    - "AC-010"
    - "DEC-001"
    - "DEC-002"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
  related_artifacts:
    - "specs/005-simple-install-policy-docs/decision-log.md"
    - "specs/005-simple-install-policy-docs/design.md"
    - "specs/005-simple-install-policy-docs/plan.md"
    - "specs/005-simple-install-policy-docs/qa.md"
    - "specs/005-simple-install-policy-docs/tasks.md"
    - "specs/005-simple-install-policy-docs/test-cases.md"
    - "specs/005-simple-install-policy-docs/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "review"
---

# Requirements

## Goal
Provide one deterministic product policy, one Bash installation command, and one user-facing documentation file.

## Problem Statement
Policy layering, separate provider installation commands, and multiple documentation pages make initial use harder to understand and verify.

## Scope
- Replace layered policy resolution with the single packaged `context_guard/defaults/policy.yaml`.
- Remove repository policy initialization and migration commands.
- Add root `install.sh` that installs Context Guard and configures both providers under the user home directory.
- Make `README.md` the complete user guide and remove the rendered documentation site content.
- Add local compact-output savings analytics and a `gain` command.

## Actors
- Developer using Claude Code and/or Codex.

## Inputs
- Bash with `curl` and Python 3.10 or newer.
- The repository one-line install command.

## Outputs
- Installed `context-guard` executable.
- Claude hooks in `$HOME/.claude/settings.json`.
- Codex hooks in `$HOME/.codex/config.toml`.
- One effective packaged policy.

## Functional Requirements
- FR-001: Runtime policy loading MUST read only the packaged `context_guard/defaults/policy.yaml`.
- FR-002: The CLI MUST NOT expose policy initialization or migration commands.
- FR-003: `install.sh` MUST install the package and idempotently configure Claude Code and Codex under the selected home/config root.
- FR-004: README MUST contain installation, behavior, policy, verification, examples, and uninstall guidance.
- FR-005: User-facing pages under `docs/` and the MkDocs configuration MUST be removed.
- FR-006: Compact executions MUST record raw and compact output bytes, estimated tokens saved, and aggregate reduction locally; `gain` MUST expose the same report as `report`.
- FR-007: A `run` proxy MUST execute supported Git-read, file, search, log, test, and lint commands with command-specific compact output, preserve exit codes, and retain full raw artifacts.
- FR-008: Claude Code PreToolUse MUST transparently rewrite simple supported Bash commands to the proxy; compound and unsupported commands MUST remain unchanged.

## Non-Functional Requirements
- NFR-001: Installation MUST fail with a clear message when Bash, curl, Python 3.10+, or venv support is unavailable.
- NFR-002: Installation MUST be non-interactive and safe to rerun.
- NFR-003: The installer MUST support isolated test overrides without changing default user paths.

## Constraints
- The canonical one-line command is `curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-context/main/install.sh | bash`.
- The single policy remains local and deterministic.
- Existing Claude and Codex unrelated configuration must be preserved.

## Acceptance Criteria
- AC-001: Policy resolution reports exactly one source: the packaged policy.
- AC-002: User and repository policy files and `CONTEXT_GUARD_MODE` do not alter the effective policy.
- AC-003: CLI help has no `init` or `migrate-policy` command.
- AC-004: An isolated installer run creates an executable and both provider hook configurations.
- AC-005: A second installer run is idempotent and preserves unrelated provider configuration.
- AC-006: README is sufficient to install, verify, use, and remove Context Guard without links to removed product docs.
- AC-007: `docs/` and `mkdocs.yml` are absent.
- AC-008: Compact runtime ledger/report output includes raw bytes, compact bytes, reduction percentage, and estimated tokens saved; documentation states this is not provider billing.
- AC-009: Supported proxy commands return bounded command-specific output with a recoverable artifact reference and the original exit code.
- AC-010: Claude simple supported commands use documented `updatedInput`; compound, mutating, and unsupported commands are not rewritten.

## Out of Scope
- Publishing a package to PyPI.
- Supporting shells other than Bash.
- Removing repository governance files, specifications, licenses, or contribution/security policies.

## Assumptions
- None. Paths, supported providers, prerequisites, installer command, and policy behavior are fixed by this specification.

## Open Questions
- None.

## Decision Status
- DEC-001 accepted: one packaged policy, one Bash installer for both providers, and README as the sole user guide.
- DEC-002 accepted: safe command rewriting, compact proxy output, recoverable raw artifacts, and local gain accounting for .NET, Java, JavaScript/TypeScript, Go, and other common developer command families.
- Resolved blockers: none.
- Accepted assumptions: none.
- TODO(dm): none.
