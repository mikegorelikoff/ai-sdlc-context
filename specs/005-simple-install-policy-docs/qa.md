---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-simple-install-policy-docs"
  artifact: "qa.md"
  path: "specs/005-simple-install-policy-docs/qa.md"
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
    - "AC-007"
  related_artifacts:
    - "specs/005-simple-install-policy-docs/decision-log.md"
    - "specs/005-simple-install-policy-docs/design.md"
    - "specs/005-simple-install-policy-docs/requirements.md"
    - "specs/005-simple-install-policy-docs/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "review"
---

# QA

## Change Summary
Simplifies policy resolution, installation, and documentation without changing hook decision rules.

## Acceptance Scenarios
- Fresh isolated installation.
- Repeated installation.
- Existing unrelated Claude and Codex configuration.
- Existing ignored policy overrides.
- Direct README onboarding.

## Regression Targets
- Claude and Codex hook parsing and installation.
- Policy validation and skill classification.
- Context decisions and compact runtime commands.
- Package build contents.

## Risk Notes
- Public removal of customizable policy layers is intentional and must be visible in README.
- Installer must never require sudo or overwrite unrelated provider data.

## Validation Commands
- `bash -n install.sh`
- `uv run pytest`
- `uv build`
- `uv run python -m compileall context_guard tests`
- README local-link verification.

## Manual Checks
- Read README top to bottom as a fresh user.
- Inspect installer completion message and provider paths.

## Signoff
- Ready when AC-001 through AC-007 pass with current evidence.
