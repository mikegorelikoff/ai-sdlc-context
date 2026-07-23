---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "002-compact-runtime"
  artifact: "tasks.md"
  path: "specs/002-compact-runtime/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/002-compact-runtime/_ai_sdlc/state.toon"
  decision_log: "specs/002-compact-runtime/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-07-24"
  updated_at: "2026-07-24"
  trace_ids:
    - "AC-006"
    - "DEC-002"
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
    - "TC-011"
    - "TC-012"
    - "TC-013"
    - "TC-014"
    - "TC-015"
  related_artifacts:
    - "specs/002-compact-runtime/decision-log.md"
    - "specs/002-compact-runtime/design.md"
    - "specs/002-compact-runtime/qa.md"
    - "specs/002-compact-runtime/requirements.md"
    - "specs/002-compact-runtime/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "review"
---

# Tasks

## Implementation
- [x] 1. Rename Stage-1's `context-guard test` fixture smoke-test subcommand to `context-guard selftest` in `context_guard/cli.py` (DEC-002); update its help text only, no behavior change.
  Output: context_guard/cli.py (renamed subcommand)
  Refs: DEC-002, qa.md#Risk Notes

- [x] 2. Scaffold `context_guard/compact/` package (`__init__.py`, `runner.py`, `artifact_store.py`, `result.py`, `ledger.py`, `fragments.py`, `parsers/__init__.py`).
  Output: context_guard/compact/ package skeleton
  Refs: design.md#Components
  Depends on: 1

- [x] 3. Implement `compact/runner.py`: subprocess execution (argv list, shell=False) capturing stdout/stderr/exit_code/duration and best-effort git commit hash.
  Output: context_guard/compact/runner.py
  Refs: FR-1, TC-014, TC-015
  Depends on: 2

- [x] 4. Implement `compact/artifact_store.py`: allocate/write/read_full/read_fragment against `.context-guard/artifacts/<kind>/<id>/`, plus `fragments.json` index.
  Output: context_guard/compact/artifact_store.py
  Refs: FR-2, FR-8, FR-9, TC-003, TC-004, TC-013
  Depends on: 2

- [x] 5. Implement `compact/result.py`: `CompactResult`/`Failure` dataclasses and JSON serialization matching the PRFAQ's compact result shape.
  Output: context_guard/compact/result.py
  Refs: FR-6, FR-7, FR-10, TC-010
  Depends on: 2

- [x] 6. Implement `compact/parsers/pytest_junitxml.py`: parse a `--junitxml` report into a `CompactResult`, returning None when unparseable.
  Output: context_guard/compact/parsers/pytest_junitxml.py
  Refs: FR-3, TC-001, TC-012
  Depends on: 4, 5

- [x] 7. Implement `compact/parsers/pytest_text.py`: deterministic text-based fallback parser for pytest's default summary/failure output.
  Output: context_guard/compact/parsers/pytest_text.py
  Refs: FR-4, TC-002, TC-009
  Depends on: 4, 5

- [x] 8. Implement `compact/parsers/fallback.py`: safe-fallback parser (exit status + bounded preview + artifact reference, no invented diagnosis).
  Output: context_guard/compact/parsers/fallback.py
  Refs: FR-5, TC-005, AC-004
  Depends on: 4, 5

- [x] 9. Implement `compact/ledger.py`: SQLite `invocations` table and `record(...)` function.
  Output: context_guard/compact/ledger.py
  Refs: FR-11, TC-006, TC-011, AC-005, AC-008
  Depends on: 2

- [x] 10. Wire `context-guard test -- <command...>` CLI subcommand in `context_guard/cli.py`: runner -> artifact_store -> parser chain (junitxml -> text -> fallback) -> result -> ledger -> stdout JSON.
  Output: context_guard/cli.py (test subcommand)
  Refs: design.md#Architecture, FR-1..FR-11, TC-001, TC-002, TC-005, TC-006, TC-008, AC-001, AC-007
  Depends on: 3, 4, 5, 6, 7, 8, 9

- [x] 11. Wire `context-guard artifact show <id> [--fragment <fragment-id>]` CLI subcommand.
  Output: context_guard/cli.py (artifact subcommand)
  Refs: FR-8, FR-9, TC-003, TC-004, TC-013, AC-002, AC-003
  Depends on: 4, 10

- [x] 12. Create `tests/fixtures/compact/` checked-in pytest fixture suite (many passing tests, deliberate failure(s)) for parser tests and the CTX-01 benchmark.
  Output: tests/fixtures/compact/
  Refs: design.md#Components, TC-001, TC-002, TC-007
  Depends on: 1

- [x] 13. Implement CTX-01 benchmark script (`context_guard/compact/benchmark.py` or `scripts/benchmark_ctx01.py`) reporting the PRFAQ's Metrics Collected fields for CTX-01.
  Output: context_guard/compact/benchmark.py
  Refs: FR-14, TC-007
  Depends on: 10, 12

## Testing
- [x] 14. Rename `tests/cli/test_test_cmd.py` (Stage-1) to `tests/cli/test_selftest_cmd.py` and update it to call `context-guard selftest` instead of `context-guard test`, confirming the rename preserves behavior.
  Output: tests/cli/test_selftest_cmd.py (renamed and updated)
  Refs: DEC-002, qa.md#Regression Targets
  Depends on: 1

- [x] 15. Write unit tests for parsers (junitxml, text, fallback) covering TC-001, TC-002, TC-005, TC-009, TC-012.
  Output: tests/compact/parsers/test_pytest_junitxml.py, tests/compact/parsers/test_pytest_text.py, tests/compact/parsers/test_fallback.py
  Refs: TC-001, TC-002, TC-005, TC-009, TC-012
  Depends on: 6, 7, 8

- [x] 16. Write unit tests for `artifact_store.py` covering TC-003, TC-004, TC-013.
  Output: tests/compact/test_artifact_store.py
  Refs: TC-003, TC-004, TC-013
  Depends on: 4

- [x] 17. Write unit tests for `ledger.py` covering TC-006, TC-011.
  Output: tests/compact/test_ledger.py
  Refs: TC-006, TC-011
  Depends on: 9

- [x] 18. Write CLI subprocess tests for `context-guard test` and `context-guard artifact show` covering TC-001, TC-002, TC-005, TC-006, TC-008, TC-013, TC-014, TC-015.
  Output: tests/cli/test_compact_test_cmd.py, tests/cli/test_compact_artifact_cmd.py
  Refs: TC-001, TC-002, TC-005, TC-006, TC-008, TC-013, TC-014, TC-015
  Depends on: 10, 11, 12

- [x] 19. Write the CTX-01 benchmark test asserting the quality gate (compact smaller than baseline AND required evidence found) covering TC-007.
  Output: tests/compact/test_benchmark_ctx01.py
  Refs: TC-007, AC-006
  Depends on: 13

## Documentation
- [x] 20. Update README.md CLI reference table: rename Stage-1 `test` row to `selftest`, add new `test -- <command>` and `artifact show` rows with usage examples matching the PRFAQ's worked example.
  Output: README.md (updated)
  Refs: DEC-002, qa.md#Manual Checks
  Depends on: 10, 11

- [x] 21. Add `docs/compact-runtime.md` documenting the artifact store layout, ledger schema, parser priority chain, and the CTX-01 benchmark, cross-linked from docs/policy.md.
  Output: docs/compact-runtime.md
  Refs: design.md#Data Model, design.md#Architecture
  Depends on: 13

