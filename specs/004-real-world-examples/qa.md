---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-real-world-examples"
  artifact: "qa.md"
  path: "specs/004-real-world-examples/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/004-real-world-examples/_ai_sdlc/state.toon"
  decision_log: "specs/004-real-world-examples/decision-log.md"
  status: "approved"
  owner: "QA"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-001"
    - "AC-007"
    - "TC-001"
    - "TC-008"
  related_artifacts:
    - "specs/004-real-world-examples/decision-log.md"
    - "specs/004-real-world-examples/design.md"
    - "specs/004-real-world-examples/plan.md"
    - "specs/004-real-world-examples/requirements.md"
    - "specs/004-real-world-examples/tasks.md"
    - "specs/004-real-world-examples/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "approved"
    - "examples"
---

# QA

## Change Summary
Add reproducible and real-local examples for the v0.1.0 Context Guard profile and measurement capabilities without changing production contracts.

## Acceptance Scenarios
Validate AC-001..AC-007 through TC-001..TC-008. Confirm fixture evidence is clearly labeled and no universal savings claim is made.

## Regression Targets
CLI imports, inventory, profiles, receipts, quality authorization, Claude/Codex measurement parsing, MkDocs navigation, Python 3.10 compatibility.

## Risk Notes
Highest risk is accidentally publishing local paths or session content. Mitigate with isolated temporary HOME, normalized schema allowlist, forbidden-key scan, and explicit local-log instructions.

## Validation Commands
- `python3 examples/run_demo.py --check`
- `python3 tests/run_pytest.py -q`
- `python3 -m mkdocs build --strict`
- `PYTHONPYCACHEPREFIX=/tmp/context-guard-pycache python3 -m compileall -q context_guard examples tests`
- `git diff --check`

## Manual Checks
Read the rendered examples page; confirm fixture vs local vs qualified evidence labels and copy/paste correctness of explicit-path commands.

## Signoff
Approved: deterministic demo check, four focused example tests, the complete 233-test repository suite, strict MkDocs build, compileall, and diff hygiene passed. Canonical receipt generation is owned by the validation stage.
