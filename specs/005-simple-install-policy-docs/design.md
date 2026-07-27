---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-simple-install-policy-docs"
  artifact: "design.md"
  path: "specs/005-simple-install-policy-docs/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/005-simple-install-policy-docs/_ai_sdlc/state.toon"
  decision_log: "specs/005-simple-install-policy-docs/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids: []
  related_artifacts:
    - "specs/005-simple-install-policy-docs/decision-log.md"
    - "specs/005-simple-install-policy-docs/plan.md"
    - "specs/005-simple-install-policy-docs/qa.md"
    - "specs/005-simple-install-policy-docs/requirements.md"
    - "specs/005-simple-install-policy-docs/tasks.md"
    - "specs/005-simple-install-policy-docs/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "review"
---

# Design

## Overview
Collapse configuration and onboarding to a single deterministic path while retaining the existing hook engine.

## Architecture
`install.sh` creates a private virtual environment, installs the repository package, exposes the executable in `$HOME/.local/bin`, then invokes the existing idempotent provider installers from the configured home directory. Runtime policy loading reads only the packaged YAML. The Claude PreToolUse hook uses one rewrite registry to route safe simple commands through a subprocess proxy; the proxy filters output by command family, stores raw evidence, records savings, and returns the original exit code.

## Components
- `install.sh`: prerequisite checks, isolated package install, executable link, provider setup, verification output.
- `context_guard/policy_config.py`: validation and construction of the one packaged policy.
- `context_guard/defaults/policy.yaml`: sole policy source.
- `context_guard/compact/ledger.py` and pipeline: local raw/compact byte and estimated-token aggregation.
- `context_guard gain`: alias for the combined local report.
- `README.md`: sole user guide.

## Interfaces and Contracts
- Installer environment overrides: `CONTEXT_GUARD_INSTALL_ROOT`, `CONTEXT_GUARD_BIN_DIR`, `CONTEXT_GUARD_CONFIG_ROOT`, and `CONTEXT_GUARD_PACKAGE` for deterministic testing or controlled deployment.
- Default config root is `$HOME`; default binary directory is `$HOME/.local/bin`.
- `load(repo_root)` remains callable for internal compatibility but ignores the argument.

## Data Model
The policy schema is version 2 and includes global mode, file/command/search limits, fail-closed rules, and skill relevance rules.

## Error Handling
The installer exits non-zero with a direct prerequisite or failed-command message. Policy validation errors identify the packaged policy source.

## Security Considerations
The installer uses HTTPS, does not use elevated privileges, writes only below the selected install/config/bin roots, and preserves unrelated hook configuration.

## Observability
`context-guard doctor`, `validate`, and `selftest` provide local verification. Installer completion output lists exact installed paths.

## Risks and Tradeoffs
Removing configuration layering intentionally removes per-user and per-repository tuning. Installing from the main branch prioritizes one-line simplicity over immutable release pinning.

## Validation Strategy
Unit-test single-source policy loading and CLI surface; run installer in an isolated root against the local repository; run the full test suite and README link checks.

## Migration Notes
Existing user or repository policy files remain on disk but are ignored. Existing hook entries continue working. Users rerun the one-line installer to configure both providers under home.
