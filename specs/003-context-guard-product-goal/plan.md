---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "plan.md"
  path: "specs/003-context-guard-product-goal/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs/003-context-guard-product-goal/decision-log.md"
  status: "active"
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
    - "active"
    - "slice-5"
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
- AC-001: requirements.md -> test-cases.md (TC-001) -> tasks.md (T001, T003) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-002) -> tasks.md (T001, T003) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-003) -> tasks.md (T001, T003) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-004) -> tasks.md (T001, T003) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-005) -> tasks.md (T001, T003) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-006) -> tasks.md (T003, T004) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-007) -> tasks.md (T005) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-008) -> tasks.md (T005) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-009) -> tasks.md (T005) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-010) -> tasks.md (T007) -> qa.md -> decision-log.md
- AC-011: requirements.md -> test-cases.md (TC-011) -> tasks.md (T007) -> qa.md -> decision-log.md
- AC-012: requirements.md -> test-cases.md (TC-012) -> tasks.md (T007) -> qa.md -> decision-log.md
- AC-013: requirements.md -> test-cases.md (TC-013) -> tasks.md (T007) -> qa.md -> decision-log.md
- AC-014: requirements.md -> test-cases.md (TC-014) -> tasks.md (T007) -> qa.md -> decision-log.md
- AC-015: requirements.md -> test-cases.md (TC-015) -> tasks.md (T009) -> qa.md -> decision-log.md
- AC-016: requirements.md -> test-cases.md (TC-016) -> tasks.md (T009) -> qa.md -> decision-log.md
- AC-017: requirements.md -> test-cases.md (TC-017) -> tasks.md (T009) -> qa.md -> decision-log.md
- AC-018: requirements.md -> test-cases.md (TC-018) -> tasks.md (T009) -> qa.md -> decision-log.md
- AC-019: requirements.md -> test-cases.md (TC-019) -> tasks.md (T009) -> qa.md -> decision-log.md
- AC-020: requirements.md -> test-cases.md (TC-020) -> tasks.md (T009) -> qa.md -> decision-log.md
- AC-021: requirements.md -> test-cases.md (TC-021) -> tasks.md (T011) -> qa.md -> decision-log.md
- AC-022: requirements.md -> test-cases.md (TC-022) -> tasks.md (T011) -> qa.md -> decision-log.md
- AC-023: requirements.md -> test-cases.md (TC-023) -> tasks.md (T011) -> qa.md -> decision-log.md
- AC-024: requirements.md -> test-cases.md (TC-024) -> tasks.md (T011) -> qa.md -> decision-log.md
- AC-025: requirements.md -> test-cases.md (TC-025) -> tasks.md (T011) -> qa.md -> decision-log.md
- AC-026: requirements.md -> test-cases.md (TC-026) -> tasks.md (T011) -> qa.md -> decision-log.md
- AC-027: requirements.md -> test-cases.md (TC-027) -> tasks.md (T011) -> qa.md -> decision-log.md
- AC-028: requirements.md -> test-cases.md (TC-028) -> tasks.md (T013) -> qa.md -> decision-log.md
- AC-029: requirements.md -> test-cases.md (TC-029) -> tasks.md (T013) -> qa.md -> decision-log.md
- AC-030: requirements.md -> test-cases.md (TC-030) -> tasks.md (T013) -> qa.md -> decision-log.md
- AC-031: requirements.md -> test-cases.md (TC-031) -> tasks.md (T013) -> qa.md -> decision-log.md
- AC-032: requirements.md -> test-cases.md (TC-032) -> tasks.md (T013) -> qa.md -> decision-log.md
- AC-033: requirements.md -> test-cases.md (TC-033) -> tasks.md (T013) -> qa.md -> decision-log.md
- AC-034: requirements.md -> test-cases.md (TC-034) -> tasks.md (T013) -> qa.md -> decision-log.md
- AC-035: requirements.md -> test-cases.md (TC-035) -> tasks.md (T013) -> qa.md -> decision-log.md
- AC-036: requirements.md -> test-cases.md (TC-036) -> tasks.md (T013) -> qa.md -> decision-log.md
- AC-037: requirements.md -> test-cases.md (TC-037) -> tasks.md (T015) -> qa.md -> decision-log.md
- AC-038: requirements.md -> test-cases.md (TC-038) -> tasks.md (T015) -> qa.md -> decision-log.md
- AC-039: requirements.md -> test-cases.md (TC-039) -> tasks.md (T015) -> qa.md -> decision-log.md
- AC-040: requirements.md -> test-cases.md (TC-040) -> tasks.md (T015) -> qa.md -> decision-log.md
- AC-041: requirements.md -> test-cases.md (TC-041) -> tasks.md (T015) -> qa.md -> decision-log.md
- AC-042: requirements.md -> test-cases.md (TC-042) -> tasks.md (T015) -> qa.md -> decision-log.md
- AC-043: requirements.md -> test-cases.md (TC-043) -> tasks.md (T015) -> qa.md -> decision-log.md
- AC-044: requirements.md -> test-cases.md (TC-044) -> tasks.md (T015) -> qa.md -> decision-log.md
- AC-045: requirements.md -> test-cases.md (TC-045) -> tasks.md (T015) -> qa.md -> decision-log.md
- AC-046: requirements.md -> test-cases.md (TC-046) -> tasks.md (T017) -> qa.md -> decision-log.md
- AC-047: requirements.md -> test-cases.md (TC-047) -> tasks.md (T017) -> qa.md -> decision-log.md
- AC-048: requirements.md -> test-cases.md (TC-048) -> tasks.md (T017) -> qa.md -> decision-log.md
- AC-049: requirements.md -> test-cases.md (TC-049) -> tasks.md (T017) -> qa.md -> decision-log.md
- AC-050: requirements.md -> test-cases.md (TC-050) -> tasks.md (T017) -> qa.md -> decision-log.md
- AC-051: requirements.md -> test-cases.md (TC-051) -> tasks.md (T017) -> qa.md -> decision-log.md
- AC-052: requirements.md -> test-cases.md (TC-052) -> tasks.md (T017) -> qa.md -> decision-log.md
- AC-053: requirements.md -> test-cases.md (TC-053) -> tasks.md (T019) -> qa.md -> decision-log.md
- AC-054: requirements.md -> test-cases.md (TC-054) -> tasks.md (T019) -> qa.md -> decision-log.md
- AC-055: requirements.md -> test-cases.md (TC-055) -> tasks.md (T019) -> qa.md -> decision-log.md
- AC-056: requirements.md -> test-cases.md (TC-056) -> tasks.md (T019) -> qa.md -> decision-log.md
- AC-057: requirements.md -> test-cases.md (TC-057) -> tasks.md (T019) -> qa.md -> decision-log.md
- AC-058: requirements.md -> test-cases.md (TC-058) -> tasks.md (T019) -> qa.md -> decision-log.md
- AC-059: requirements.md -> test-cases.md (TC-059) -> tasks.md (T019) -> qa.md -> decision-log.md
- AC-060: requirements.md -> test-cases.md (TC-060) -> tasks.md (T019) -> qa.md -> decision-log.md
- AC-061: requirements.md -> test-cases.md (TC-061) -> tasks.md (T019) -> qa.md -> decision-log.md
- AC-062: requirements.md -> test-cases.md (TC-062) -> tasks.md (T019) -> qa.md -> decision-log.md
- AC-063: requirements.md -> test-cases.md (TC-063) -> tasks.md (T019) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: Implement policy-v2 core.; refs: AC-001, AC-002, AC-003, AC-004, AC-005; output: context_guard/policy_config.py, context_guard/cli.py
- [x] T002: Add policy-v2 tests.; refs: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006; output: tests/test_policy_v2.py, tests/cli/test_validate.py, tests/cli/test_doctor.py
- [x] T005: Implement v2 init and migration.; refs: AC-007, AC-008, AC-009; output: context_guard/policy_config.py, context_guard/cli.py
- [x] T006: Add migration tests.; refs: TC-007, TC-008, TC-009; output: tests/cli/test_init.py, tests/cli/test_migrate_policy.py
- [x] T007: Implement provider/version/surface preflight and stable authoritative inventory.; refs: FR-011, FR-012, FR-013, FR-014, FR-015, AC-010, AC-011, AC-012, AC-013, AC-014, DSR-101; output: context_guard/inventory.py, context_guard/cli.py
- [x] T008: Add inventory unit and CLI contract tests.; refs: TC-010, TC-011, TC-012, TC-013, TC-014; output: tests/test_inventory.py, tests/cli/test_inventory_cmd.py
- [x] T009: Implement private versioned receipt storage, validation, atomic non-overwriting writes, writer locking, inspection, exact deletion, retention pruning, and corrupt-record quarantine.; refs: FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023, FR-024, AC-015, AC-016, AC-017, AC-018, AC-019, AC-020, DSR-301, DSR-302; output: context_guard/receipts.py, context_guard/cli.py
- [x] T010: Add receipt unit and CLI contract tests.; refs: TC-015, TC-016, TC-017, TC-018, TC-019, TC-020; output: tests/test_receipts.py, tests/cli/test_receipt_cmd.py
- [x] T011: Implement the Claude guarded-profile planner, persistent lease, private snapshot, atomic verified mutation, full-load fallback, CAS restore, disabled marker, dead-owner recovery, and sanitized receipt integration.; refs: FR-025, FR-026, FR-027, FR-028, FR-029, FR-030, FR-031, FR-032, FR-033, FR-034, AC-021, AC-022, AC-023, AC-024, AC-025, AC-026, AC-027, DSR-201; output: context_guard/claude_profile.py, context_guard/cli.py
- [x] T012: Add Claude profile unit and CLI fault-injection tests.; refs: TC-021, TC-022, TC-023, TC-024, TC-025, TC-026, TC-027; output: tests/test_claude_profile.py, tests/cli/test_claude_profile_cmd.py
- [x] T013: Implement exact quality manifest/attempt schemas, three-fixture validation, QG-301–QG-309 pair evaluation, append-only private ledger, QA invalidation, measurement authorization, and sanitized receipt integration.; refs: FR-035, FR-036, FR-037, FR-038, FR-039, FR-040, FR-041, FR-042, FR-043, FR-044, AC-028, AC-029, AC-030, AC-031, AC-032, AC-033, AC-034, AC-035, AC-036, DSR-401, DSR-402; output: context_guard/quality.py, context_guard/cli.py
- [x] T014: Add quality evaluator, ledger, privacy, gate-parameterization, and CLI tests.; refs: TC-028, TC-029, TC-030, TC-031, TC-032, TC-033, TC-034, TC-035, TC-036; output: tests/test_quality.py, tests/cli/test_quality_cmd.py
- [x] T015: Implement explicit-path Claude JSONL extraction, strict correlation/deduplication, minimized run evidence, authorized pair comparison, exact statistics, five-by-three qualification gates, append-only storage, receipts, and CLI controls.; refs: FR-045, FR-046, FR-047, FR-048, FR-049, FR-050, FR-051, FR-052, FR-053, FR-054, FR-055, AC-037, AC-038, AC-039, AC-040, AC-041, AC-042, AC-043, AC-044, AC-045, DSR-501, DEC-004; output: context_guard/claude_measurement.py, context_guard/cli.py, docs/claude-measurement.md
- [x] T016: Add Claude extraction, pairing, aggregation, privacy, fault-injection, authorization, and CLI tests.; refs: TC-037, TC-038, TC-039, TC-040, TC-041, TC-042, TC-043, TC-044, TC-045; output: tests/test_claude_measurement.py, tests/cli/test_claude_measurement_cmd.py
- [x] T017: Align Codex inventory with HOME/.agents/skills and implement exact irrelevant profile planning, explicit dedicated-profile mutation, private lease/snapshot, atomic verification, fresh-thread selector, CAS restore, disabled-marker recovery, and receipts.; refs: FR-012, FR-056, FR-057, FR-058, FR-059, FR-060, FR-061, FR-062, FR-063, FR-075, AC-046, AC-047, AC-048, AC-049, AC-050, AC-051, AC-052, DSR-101, DSR-202, DEC-005; output: context_guard/inventory.py, context_guard/codex_profile.py, context_guard/cli.py, docs/codex-profile.md
- [x] T018: Add Codex inventory migration, profile planning, mutation, restoration, recovery, privacy, fault-injection, and CLI tests.; refs: TC-046, TC-047, TC-048, TC-049, TC-050, TC-051, TC-052; output: tests/test_inventory.py, tests/test_codex_profile.py, tests/cli/test_codex_profile_cmd.py
- [x] T019: Implement Codex exact-event and cumulative cached-input extraction, quality correlation, signed pairing, exact five-by-three qualification, private append-only evidence, receipts, and CLI controls.; refs: FR-064, FR-065, FR-066, FR-067, FR-068, FR-069, FR-070, FR-071, FR-072, FR-073, FR-074, AC-053, AC-054, AC-055, AC-056, AC-057, AC-058, AC-059, AC-060, AC-061, AC-062, AC-063, DSR-502, DEC-005; output: context_guard/codex_measurement.py, context_guard/cli.py, docs/codex-measurement.md
- [x] T020: Add Codex exact/cumulative measurement, ambiguity, pairing, statistics, privacy, invalidation, persistence, and CLI tests.; refs: TC-053, TC-054, TC-055, TC-056, TC-057, TC-058, TC-059, TC-060, TC-061, TC-062, TC-063; output: tests/test_codex_measurement.py, tests/cli/test_codex_measurement_cmd.py
- [x] T003: Run focused policy/CLI tests and full regression validation; capture and verify the validation receipt.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006; output: specs/003-context-guard-product-goal/_ai_sdlc/validation-receipt.json, specs/003-context-guard-product-goal/validation.md
- [x] T004: Document policy v2 schema, replacement semantics, diagnostics, precedence, and v1 compatibility.; refs: FR-001, FR-002, FR-003, FR-005, FR-007, AC-006; output: docs/policy.md

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on previous applicable task / none
- T005: depends on previous applicable task / none
- T006: depends on previous applicable task / none
- T007: depends on previous applicable task / none
- T008: depends on T007
- T009: depends on previous applicable task / none
- T010: depends on T009
- T011: depends on previous applicable task / none
- T012: depends on T011
- T013: depends on previous applicable task / none
- T014: depends on T013
- T015: depends on T013, T014
- T016: depends on T015
- T017: depends on T007, T009
- T018: depends on T017
- T019: depends on T014, T017
- T020: depends on T019
- T003: depends on T001, T002
- T004: depends on T001

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-27

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
