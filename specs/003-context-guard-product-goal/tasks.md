---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "tasks.md"
  path: "specs/003-context-guard-product-goal/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs/003-context-guard-product-goal/decision-log.md"
  status: "active"
  owner: "Engineering and QA"
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
    - "AC-011"
    - "AC-012"
    - "AC-013"
    - "AC-014"
    - "AC-015"
    - "AC-016"
    - "AC-017"
    - "AC-018"
    - "AC-019"
    - "AC-020"
    - "AC-021"
    - "AC-022"
    - "AC-023"
    - "AC-024"
    - "AC-025"
    - "AC-026"
    - "AC-027"
    - "AC-028"
    - "AC-029"
    - "AC-030"
    - "AC-031"
    - "AC-032"
    - "AC-033"
    - "AC-034"
    - "AC-035"
    - "AC-036"
    - "AC-037"
    - "AC-038"
    - "AC-039"
    - "AC-040"
    - "AC-041"
    - "AC-042"
    - "AC-043"
    - "AC-044"
    - "AC-045"
    - "AC-046"
    - "AC-047"
    - "AC-048"
    - "AC-049"
    - "AC-050"
    - "AC-051"
    - "AC-052"
    - "AC-053"
    - "AC-054"
    - "AC-055"
    - "AC-056"
    - "AC-057"
    - "AC-058"
    - "AC-059"
    - "AC-060"
    - "AC-061"
    - "AC-062"
    - "AC-063"
    - "DEC-004"
    - "DEC-005"
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
    - "TC-010"
    - "TC-011"
    - "TC-012"
    - "TC-013"
    - "TC-014"
    - "TC-015"
    - "TC-016"
    - "TC-017"
    - "TC-018"
    - "TC-019"
    - "TC-020"
    - "TC-021"
    - "TC-022"
    - "TC-023"
    - "TC-024"
    - "TC-025"
    - "TC-026"
    - "TC-027"
    - "TC-028"
    - "TC-029"
    - "TC-030"
    - "TC-031"
    - "TC-032"
    - "TC-033"
    - "TC-034"
    - "TC-035"
    - "TC-036"
    - "TC-037"
    - "TC-038"
    - "TC-039"
    - "TC-040"
    - "TC-041"
    - "TC-042"
    - "TC-043"
    - "TC-044"
    - "TC-045"
    - "TC-046"
    - "TC-047"
    - "TC-048"
    - "TC-049"
    - "TC-050"
    - "TC-051"
    - "TC-052"
    - "TC-053"
    - "TC-054"
    - "TC-055"
    - "TC-056"
    - "TC-057"
    - "TC-058"
    - "TC-059"
    - "TC-060"
    - "TC-061"
    - "TC-062"
    - "TC-063"
  related_artifacts:
    - "specs/003-context-guard-product-goal/branch-plan.md"
    - "specs/003-context-guard-product-goal/change-impact.md"
    - "specs/003-context-guard-product-goal/decision-log.md"
    - "specs/003-context-guard-product-goal/design.md"
    - "specs/003-context-guard-product-goal/plan.md"
    - "specs/003-context-guard-product-goal/qa.md"
    - "specs/003-context-guard-product-goal/requirements.md"
    - "specs/003-context-guard-product-goal/test-cases.md"
    - "specs/003-context-guard-product-goal/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "active"
    - "slice-5"
    - "slice-4"
    - "slice-3"
    - "slice-1"
---

# Tasks

## Implementation
- [x] T001. Implement policy-v2 core.
  Output: context_guard/policy_config.py, context_guard/cli.py
  Refs: AC-001, AC-002, AC-003, AC-004, AC-005
- [x] T002. Add policy-v2 tests.
  Output: tests/test_policy_v2.py, tests/cli/test_validate.py, tests/cli/test_doctor.py
  Refs: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006
- [x] T005. Implement v2 init and migration.
  Output: context_guard/policy_config.py, context_guard/cli.py
  Refs: AC-007, AC-008, AC-009
- [x] T006. Add migration tests.
  Output: tests/cli/test_init.py, tests/cli/test_migrate_policy.py
  Refs: TC-007, TC-008, TC-009
- [x] T007. Implement provider/version/surface preflight and stable authoritative inventory.
  Output: context_guard/inventory.py, context_guard/cli.py
  Refs: FR-011, FR-012, FR-013, FR-014, FR-015, AC-010, AC-011, AC-012, AC-013, AC-014, DSR-101
- [x] T008. Add inventory unit and CLI contract tests.
  Output: tests/test_inventory.py, tests/cli/test_inventory_cmd.py
  Refs: TC-010, TC-011, TC-012, TC-013, TC-014
  Depends on: T007
- [x] T009. Implement private versioned receipt storage, validation, atomic non-overwriting writes, writer locking, inspection, exact deletion, retention pruning, and corrupt-record quarantine.
  Output: context_guard/receipts.py, context_guard/cli.py
  Refs: FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023, FR-024, AC-015, AC-016, AC-017, AC-018, AC-019, AC-020, DSR-301, DSR-302
- [x] T010. Add receipt unit and CLI contract tests.
  Output: tests/test_receipts.py, tests/cli/test_receipt_cmd.py
  Refs: TC-015, TC-016, TC-017, TC-018, TC-019, TC-020
  Depends on: T009
- [x] T011. Implement the Claude guarded-profile planner, persistent lease, private snapshot, atomic verified mutation, full-load fallback, CAS restore, disabled marker, dead-owner recovery, and sanitized receipt integration.
  Output: context_guard/claude_profile.py, context_guard/cli.py
  Refs: FR-025, FR-026, FR-027, FR-028, FR-029, FR-030, FR-031, FR-032, FR-033, FR-034, AC-021, AC-022, AC-023, AC-024, AC-025, AC-026, AC-027, DSR-201
- [x] T012. Add Claude profile unit and CLI fault-injection tests.
  Output: tests/test_claude_profile.py, tests/cli/test_claude_profile_cmd.py
  Refs: TC-021, TC-022, TC-023, TC-024, TC-025, TC-026, TC-027
  Depends on: T011
- [x] T013. Implement exact quality manifest/attempt schemas, three-fixture validation, QG-301–QG-309 pair evaluation, append-only private ledger, QA invalidation, measurement authorization, and sanitized receipt integration.
  Output: context_guard/quality.py, context_guard/cli.py
  Refs: FR-035, FR-036, FR-037, FR-038, FR-039, FR-040, FR-041, FR-042, FR-043, FR-044, AC-028, AC-029, AC-030, AC-031, AC-032, AC-033, AC-034, AC-035, AC-036, DSR-401, DSR-402
- [x] T014. Add quality evaluator, ledger, privacy, gate-parameterization, and CLI tests.
  Output: tests/test_quality.py, tests/cli/test_quality_cmd.py
  Refs: TC-028, TC-029, TC-030, TC-031, TC-032, TC-033, TC-034, TC-035, TC-036
  Depends on: T013

- [x] T015. Implement explicit-path Claude JSONL extraction, strict correlation/deduplication, minimized run evidence, authorized pair comparison, exact statistics, five-by-three qualification gates, append-only storage, receipts, and CLI controls.
  Output: context_guard/claude_measurement.py, context_guard/cli.py, docs/claude-measurement.md
  Refs: FR-045, FR-046, FR-047, FR-048, FR-049, FR-050, FR-051, FR-052, FR-053, FR-054, FR-055, AC-037, AC-038, AC-039, AC-040, AC-041, AC-042, AC-043, AC-044, AC-045, DSR-501, DEC-004
  Depends on: T013, T014
- [x] T016. Add Claude extraction, pairing, aggregation, privacy, fault-injection, authorization, and CLI tests.
  Output: tests/test_claude_measurement.py, tests/cli/test_claude_measurement_cmd.py
  Refs: TC-037, TC-038, TC-039, TC-040, TC-041, TC-042, TC-043, TC-044, TC-045
  Depends on: T015

- [x] T017. Align Codex inventory with HOME/.agents/skills and implement exact irrelevant profile planning, explicit dedicated-profile mutation, private lease/snapshot, atomic verification, fresh-thread selector, CAS restore, disabled-marker recovery, and receipts.
  Output: context_guard/inventory.py, context_guard/codex_profile.py, context_guard/cli.py, docs/codex-profile.md
  Refs: FR-012, FR-056, FR-057, FR-058, FR-059, FR-060, FR-061, FR-062, FR-063, FR-075, AC-046, AC-047, AC-048, AC-049, AC-050, AC-051, AC-052, DSR-101, DSR-202, DEC-005
  Depends on: T007, T009
- [x] T018. Add Codex inventory migration, profile planning, mutation, restoration, recovery, privacy, fault-injection, and CLI tests.
  Output: tests/test_inventory.py, tests/test_codex_profile.py, tests/cli/test_codex_profile_cmd.py
  Refs: TC-046, TC-047, TC-048, TC-049, TC-050, TC-051, TC-052
  Depends on: T017
- [x] T019. Implement Codex exact-event and cumulative cached-input extraction, quality correlation, signed pairing, exact five-by-three qualification, private append-only evidence, receipts, and CLI controls.
  Output: context_guard/codex_measurement.py, context_guard/cli.py, docs/codex-measurement.md
  Refs: FR-064, FR-065, FR-066, FR-067, FR-068, FR-069, FR-070, FR-071, FR-072, FR-073, FR-074, AC-053, AC-054, AC-055, AC-056, AC-057, AC-058, AC-059, AC-060, AC-061, AC-062, AC-063, DSR-502, DEC-005
  Depends on: T014, T017
- [x] T020. Add Codex exact/cumulative measurement, ambiguity, pairing, statistics, privacy, invalidation, persistence, and CLI tests.
  Output: tests/test_codex_measurement.py, tests/cli/test_codex_measurement_cmd.py
  Refs: TC-053, TC-054, TC-055, TC-056, TC-057, TC-058, TC-059, TC-060, TC-061, TC-062, TC-063
  Depends on: T019

## Testing
- [x] T003. Run focused policy/CLI tests and full regression validation; capture and verify the validation receipt.
  Output: specs/003-context-guard-product-goal/_ai_sdlc/validation-receipt.json, specs/003-context-guard-product-goal/validation.md
  Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006
  Depends on: T001, T002

## Documentation
- [x] T004. Document policy v2 schema, replacement semantics, diagnostics, precedence, and v1 compatibility.
  Output: docs/policy.md
  Refs: FR-001, FR-002, FR-003, FR-005, FR-007, AC-006
  Depends on: T001
