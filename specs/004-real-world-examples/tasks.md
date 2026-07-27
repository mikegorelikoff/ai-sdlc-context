---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-real-world-examples"
  artifact: "tasks.md"
  path: "specs/004-real-world-examples/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/004-real-world-examples/_ai_sdlc/state.toon"
  decision_log: "specs/004-real-world-examples/decision-log.md"
  status: "review"
  owner: "Dev"
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
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
  related_artifacts:
    - "specs/004-real-world-examples/decision-log.md"
    - "specs/004-real-world-examples/design.md"
    - "specs/004-real-world-examples/plan.md"
    - "specs/004-real-world-examples/qa.md"
    - "specs/004-real-world-examples/requirements.md"
    - "specs/004-real-world-examples/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "review"
    - "examples"
    - "active"
---

# Tasks

## Implementation
- [x] T001 Create deterministic fixtures and isolated demo runner.
  Output: examples/
  Refs: FR-001, FR-002, FR-003, FR-007, AC-001, AC-002, AC-003, AC-004

## Testing
- [x] T002 Add subprocess/privacy/drift tests for the demo.
  Output: tests/examples/test_run_demo.py
  Refs: AC-001, AC-002, AC-003, AC-004, AC-006, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007
  Depends on: T001

- [x] T003 Run focused and full validation.
  Output: specs/004-real-world-examples/validation.md and _ai_sdlc/validation-receipt.json
  Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008
  Depends on: T002

## Documentation
- [x] T004 Add the real-world examples guide with fixture, local Claude, local Codex, and qualification workflows.
  Output: docs/real-world-examples.md
  Refs: FR-004, FR-005, FR-006, AC-005
  Depends on: T001

- [x] T005 Link examples from README, docs index, and MkDocs navigation.
  Output: README.md, docs/index.md, mkdocs.yml
  Refs: AC-007, TC-008
  Depends on: T004
