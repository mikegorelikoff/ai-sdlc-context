---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "002-compact-runtime"
  artifact: "plan.md"
  path: "/Users/mikegorelikov/ai-sdlc-context/specs/002-compact-runtime/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "/Users/mikegorelikov/ai-sdlc-context/specs/002-compact-runtime/_ai_sdlc/state.toon"
  decision_log: "/Users/mikegorelikov/ai-sdlc-context/specs/002-compact-runtime/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-07-24"
  updated_at: "2026-07-24"
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
- AC-001: requirements.md -> test-cases.md (TC-001, TC-002) -> tasks.md (10) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-003) -> tasks.md (11) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-004) -> tasks.md (11) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-005) -> tasks.md (8) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-006) -> tasks.md (9) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-007) -> tasks.md (19) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-008) -> tasks.md (10) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-011) -> tasks.md (9) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] 1: Rename Stage-1's `context-guard test` fixture smoke-test subcommand to `context-guard selftest` in `context_guard/cli.py` (DEC-002); update its help text only, no behavior change.; refs: DEC-002, qa.md#Risk Notes; output: context_guard/cli.py (renamed subcommand)
- [x] 2: Scaffold `context_guard/compact/` package (`__init__.py`, `runner.py`, `artifact_store.py`, `result.py`, `ledger.py`, `fragments.py`, `parsers/__init__.py`).; refs: design.md#Components; output: context_guard/compact/ package skeleton
- [x] 3: Implement `compact/runner.py`: subprocess execution (argv list, shell=False) capturing stdout/stderr/exit_code/duration and best-effort git commit hash.; refs: FR-1, TC-014, TC-015; output: context_guard/compact/runner.py
- [x] 4: Implement `compact/artifact_store.py`: allocate/write/read_full/read_fragment against `.context-guard/artifacts/<kind>/<id>/`, plus `fragments.json` index.; refs: FR-2, FR-8, FR-9, TC-003, TC-004, TC-013; output: context_guard/compact/artifact_store.py
- [x] 5: Implement `compact/result.py`: `CompactResult`/`Failure` dataclasses and JSON serialization matching the PRFAQ's compact result shape.; refs: FR-6, FR-7, FR-10, TC-010; output: context_guard/compact/result.py
- [x] 6: Implement `compact/parsers/pytest_junitxml.py`: parse a `--junitxml` report into a `CompactResult`, returning None when unparseable.; refs: FR-3, TC-001, TC-012; output: context_guard/compact/parsers/pytest_junitxml.py
- [x] 7: Implement `compact/parsers/pytest_text.py`: deterministic text-based fallback parser for pytest's default summary/failure output.; refs: FR-4, TC-002, TC-009; output: context_guard/compact/parsers/pytest_text.py
- [x] 8: Implement `compact/parsers/fallback.py`: safe-fallback parser (exit status + bounded preview + artifact reference, no invented diagnosis).; refs: FR-5, TC-005, AC-004; output: context_guard/compact/parsers/fallback.py
- [x] 9: Implement `compact/ledger.py`: SQLite `invocations` table and `record(...)` function.; refs: FR-11, TC-006, TC-011, AC-005, AC-008; output: context_guard/compact/ledger.py
- [x] 10: Wire `context-guard test -- <command...>` CLI subcommand in `context_guard/cli.py`: runner -> artifact_store -> parser chain (junitxml -> text -> fallback) -> result -> ledger -> stdout JSON.; refs: design.md#Architecture, FR-1..FR-11, TC-001, TC-002, TC-005, TC-006, TC-008, AC-001, AC-007; output: context_guard/cli.py (test subcommand)
- [x] 11: Wire `context-guard artifact show <id> [--fragment <fragment-id>]` CLI subcommand.; refs: FR-8, FR-9, TC-003, TC-004, TC-013, AC-002, AC-003; output: context_guard/cli.py (artifact subcommand)
- [x] 12: Create `tests/fixtures/compact/` checked-in pytest fixture suite (many passing tests, deliberate failure(s)) for parser tests and the CTX-01 benchmark.; refs: design.md#Components, TC-001, TC-002, TC-007; output: tests/fixtures/compact/
- [x] 13: Implement CTX-01 benchmark script (`context_guard/compact/benchmark.py` or `scripts/benchmark_ctx01.py`) reporting the PRFAQ's Metrics Collected fields for CTX-01.; refs: FR-14, TC-007; output: context_guard/compact/benchmark.py
- [x] 14: Rename `tests/cli/test_test_cmd.py` (Stage-1) to `tests/cli/test_selftest_cmd.py` and update it to call `context-guard selftest` instead of `context-guard test`, confirming the rename preserves behavior.; refs: DEC-002, qa.md#Regression Targets; output: tests/cli/test_selftest_cmd.py (renamed and updated)
- [x] 15: Write unit tests for parsers (junitxml, text, fallback) covering TC-001, TC-002, TC-005, TC-009, TC-012.; refs: TC-001, TC-002, TC-005, TC-009, TC-012; output: tests/compact/parsers/test_pytest_junitxml.py, tests/compact/parsers/test_pytest_text.py, tests/compact/parsers/test_fallback.py
- [x] 16: Write unit tests for `artifact_store.py` covering TC-003, TC-004, TC-013.; refs: TC-003, TC-004, TC-013; output: tests/compact/test_artifact_store.py
- [x] 17: Write unit tests for `ledger.py` covering TC-006, TC-011.; refs: TC-006, TC-011; output: tests/compact/test_ledger.py
- [x] 18: Write CLI subprocess tests for `context-guard test` and `context-guard artifact show` covering TC-001, TC-002, TC-005, TC-006, TC-008, TC-013, TC-014, TC-015.; refs: TC-001, TC-002, TC-005, TC-006, TC-008, TC-013, TC-014, TC-015; output: tests/cli/test_compact_test_cmd.py, tests/cli/test_compact_artifact_cmd.py
- [x] 19: Write the CTX-01 benchmark test asserting the quality gate (compact smaller than baseline AND required evidence found) covering TC-007.; refs: TC-007, AC-006; output: tests/compact/test_benchmark_ctx01.py
- [x] 20: Update README.md CLI reference table: rename Stage-1 `test` row to `selftest`, add new `test -- <command>` and `artifact show` rows with usage examples matching the PRFAQ's worked example.; refs: DEC-002, qa.md#Manual Checks; output: README.md (updated)
- [x] 21: Add `docs/compact-runtime.md` documenting the artifact store layout, ledger schema, parser priority chain, and the CTX-01 benchmark, cross-linked from docs/policy.md.; refs: design.md#Data Model, design.md#Architecture; output: docs/compact-runtime.md

## Task Dependencies
- 1: depends on previous applicable task / none
- 2: depends on 1
- 3: depends on 2
- 4: depends on 2
- 5: depends on 2
- 6: depends on 4, 5
- 7: depends on 4, 5
- 8: depends on 4, 5
- 9: depends on 2
- 10: depends on 3, 4, 5, 6, 7, 8, 9
- 11: depends on 4, 10
- 12: depends on 1
- 13: depends on 10, 12
- 14: depends on 1
- 15: depends on 6, 7, 8
- 16: depends on 4
- 17: depends on 9
- 18: depends on 10, 11, 12
- 19: depends on 13
- 20: depends on 10, 11
- 21: depends on 13

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-24

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
