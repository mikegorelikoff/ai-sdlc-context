---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-simple-install-policy-docs"
  artifact: "validation.md"
  path: "specs/005-simple-install-policy-docs/validation.md"
  workspace: "implementation"
  skill: "ai-sdlc-validation"
  flow_mode: "quick"
  state_file: "specs/005-simple-install-policy-docs/_ai_sdlc/state.toon"
  decision_log: "specs/005-simple-install-policy-docs/decision-log.md"
  status: "validated"
  owner: "Engineering and QA"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-001"
    - "AC-010"
    - "DEC-001"
    - "DEC-002"
    - "TC-001"
    - "TC-010"
  related_artifacts:
    - "specs/005-simple-install-policy-docs/qa.md"
    - "specs/005-simple-install-policy-docs/test-cases.md"
    - "specs/005-simple-install-policy-docs/tasks.md"
  validation:
    - "specs/005-simple-install-policy-docs/_ai_sdlc/validation-receipt.json"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-validation"
    - "validation"
    - "validated"
---

# Validation

## Scope

Validate the single packaged policy, one-line installer, README-only user
documentation, command proxy and Claude rewrite, full-output
artifacts, exit-code preservation, local gain accounting, package contents,
and SDD traceability.

## Commands

- V001 runs the complete repository regression suite.
- V002 validates Bash installer syntax.
- V003 validates the 005 SDD package.
- V004 validates whitespace and patch hygiene.
- Supplemental evidence builds the wheel, confirms the packaged policy and
  command proxy are present, installs the wheel into an isolated home, creates
  both provider configurations, runs the proxy, and reads the gain report.

## Result

The complete suite passes 238 tests. Installer syntax, Python compilation,
SDD structure, plan links, and diff hygiene pass. The final wheel and source
archive build successfully and contain the single policy plus command proxy.
An isolated wheel installation creates Claude and Codex configuration, validates
the packaged policy, runs a compact command with a recoverable artifact, and
emits the local gain report.

## Residual Risk

Claude command mutation follows the documented PreToolUse `updatedInput`
contract. Codex does not expose the same stable mutation mechanism, so Codex
uses the explicit `context-guard run -- ...` proxy. Specialized filters are
bounded and conservative; commands without a specialized filter use generic
deduplication and truncation when explicitly proxied.
