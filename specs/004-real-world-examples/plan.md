---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-real-world-examples"
  artifact: "plan.md"
  path: "specs/004-real-world-examples/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/004-real-world-examples/_ai_sdlc/state.toon"
  decision_log: "specs/004-real-world-examples/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "plan"
    - "draft"
---

# plan.md

## Upstream Refinement Sources
- Refinement index: `specs-refiniment/_ai_sdlc/specs-index.toon`
- Refinement state: `specs-refiniment/<feature-name>/_ai_sdlc/state.toon`
- Delivery spec: `specs-refiniment/<feature-name>/delivery-spec.md`
- QA readiness: `specs-refiniment/<feature-name>/qa-readiness.md`
- Decision trace: `decision-log.md`

## SDD Artifact Links
- Requirements: `requirements.md`
- Design: `design.md`
- Test cases: `test-cases.md`
- QA: `qa.md`
- Tasks: `tasks.md`
- Machine plan: `_ai_sdlc/plan.toon`
- Decision log: `decision-log.md`

## Cross-Artifact Trace Map
- AC-001: requirements.md -> test-cases.md (TC-001) -> tasks.md (T001, T002, T003) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-002) -> tasks.md (T001, T002, T003) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-003, TC-004) -> tasks.md (T001, T002, T003) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-005) -> tasks.md (T001, T002, T003) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-008) -> tasks.md (T003, T004) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-006, TC-007) -> tasks.md (T002, T003) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-008) -> tasks.md (T003, T005) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: Create deterministic fixtures and isolated demo runner.; refs: FR-001, FR-002, FR-003, FR-007, AC-001, AC-002, AC-003, AC-004; output: examples/
- [x] T002: Add subprocess/privacy/drift tests for the demo.; refs: AC-001, AC-002, AC-003, AC-004, AC-006, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007; output: tests/examples/test_run_demo.py
- [x] T003: Run focused and full validation.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008; output: specs/004-real-world-examples/validation.md and _ai_sdlc/validation-receipt.json
- [x] T004: Add the real-world examples guide with fixture, local Claude, local Codex, and qualification workflows.; refs: FR-004, FR-005, FR-006, AC-005; output: docs/real-world-examples.md
- [x] T005: Link examples from README, docs index, and MkDocs navigation.; refs: AC-007, TC-008; output: README.md, docs/index.md, mkdocs.yml

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on T001
- T003: depends on T002
- T004: depends on T001
- T005: depends on T004

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-27

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
