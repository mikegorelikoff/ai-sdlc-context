---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-simple-install-policy-docs"
  artifact: "plan.md"
  path: "specs/005-simple-install-policy-docs/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/005-simple-install-policy-docs/_ai_sdlc/state.toon"
  decision_log: "specs/005-simple-install-policy-docs/decision-log.md"
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
- AC-001: requirements.md -> test-cases.md (TC-001) -> tasks.md (T001, T003, T004) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-002) -> tasks.md (T001, T003, T004) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-003) -> tasks.md (T001, T003, T004) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-004) -> tasks.md (T002, T003, T004) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-005) -> tasks.md (T002, T003, T004) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-006) -> tasks.md (T004, T005) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-007) -> tasks.md (T004, T005) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-008) -> tasks.md (T006, T004) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-009) -> tasks.md (T007, T003, T004) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-010) -> tasks.md (T007, T003, T004) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: Replace policy layering with one packaged version-2 policy.; refs: FR-001, FR-002, AC-001, AC-002, AC-003, TC-001, TC-002, TC-003; output: context_guard/policy_config.py, context_guard/defaults/policy.yaml, context_guard/cli.py
- [x] T002: Add the idempotent one-line Bash installer.; refs: FR-003, AC-004, AC-005, TC-004, TC-005; output: install.sh
- [x] T006: Add local output-reduction analytics and `gain` alias.; refs: FR-006, AC-008, TC-008; output: context_guard/compact/ledger.py, context_guard/compact/pipeline.py, context_guard/cli.py
- [x] T007: Add command-specific compact proxy and transparent Claude rewrite.; refs: FR-007, FR-008, AC-009, AC-010, TC-009, TC-010; output: context_guard/compact/command_proxy.py, context_guard/adapters/claude_code.py
- [x] T003: Update policy tests and add installer integration tests.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-009, AC-010, TC-001, TC-002, TC-003, TC-004, TC-005, TC-009, TC-010; output: tests/test_policy_v2.py, tests/test_install_script.py, tests/cli/test_command_proxy_cmd.py, tests/compact/test_command_proxy.py
- [x] T004: Run focused and full validation.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010; output: specs/005-simple-install-policy-docs/validation.md, specs/005-simple-install-policy-docs/_ai_sdlc/validation-receipt.json
- [x] T005: Rewrite README as the sole user guide and remove the docs site.; refs: FR-004, FR-005, AC-006, AC-007, TC-006, TC-007; output: README.md; removed docs/ and mkdocs.yml

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on T001
- T006: depends on T001
- T007: depends on T002, T006
- T003: depends on T001, T002, T007
- T004: depends on T003
- T005: depends on T002, T007

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-27

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
