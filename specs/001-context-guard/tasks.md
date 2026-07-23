---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-context-guard"
  artifact: "tasks.md"
  path: "specs/001-context-guard/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/001-context-guard/_ai_sdlc/state.toon"
  decision_log: "specs/001-context-guard/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-07-23"
  updated_at: "2026-07-23"
  trace_ids:
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
  related_artifacts:
    - "specs/001-context-guard/decision-log.md"
    - "specs/001-context-guard/design.md"
    - "specs/001-context-guard/qa.md"
    - "specs/001-context-guard/requirements.md"
    - "specs/001-context-guard/test-cases.md"
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
- [x] 1. Scaffold the `context_guard` package structure (cli.py, events.py, engine.py, decisions.py, adapters/, policies/, audit/, policy_config.py) with empty/stub modules and `pyproject.toml` packaging metadata.
  Output: context_guard/ package skeleton, pyproject.toml
  Refs: design.md#Components, design.md#Architecture

- [x] 2. Implement `events.py` internal Event model and operation_kind classification table.
  Output: context_guard/events.py
  Refs: design.md#Interfaces and Contracts
  Depends on: 1

- [x] 3. Implement `decisions.py` Decision model and decision-building helpers (allow/warn/block).
  Output: context_guard/decisions.py
  Refs: design.md#Interfaces and Contracts
  Depends on: 1

- [x] 4. Implement `defaults/policy.yaml` and `policy_config.py` layered config loader (built-in -> user -> repo -> env).
  Output: context_guard/defaults/policy.yaml, context_guard/policy_config.py
  Refs: design.md#Data Model, FR-8
  Depends on: 1

- [x] 5. Implement `policies/files.py` (deny globs, size thresholds, bounded-range detection).
  Output: context_guard/policies/files.py
  Refs: FR-3, TC-001, TC-002, TC-008
  Depends on: 2, 3, 4

- [x] 6. Implement `policies/commands.py` (unbounded log/command pattern detection and require_bounds).
  Output: context_guard/policies/commands.py
  Refs: FR-4, TC-003, TC-004
  Depends on: 2, 3, 4

- [x] 7. Implement `policies/searches.py` (path-scope and result-limit enforcement).
  Output: context_guard/policies/searches.py
  Refs: FR-5, TC-005, TC-006, TC-007
  Depends on: 2, 3, 4

- [x] 8. Implement `policies/sessions.py` (SessionStart/PreCompact/PostCompact/Stop session-state tracking).
  Output: context_guard/policies/sessions.py
  Refs: FR-19, FR-20, TC-024
  Depends on: 2, 3, 4

- [x] 9. Implement `engine.py` dispatch (route Event to policy modules, fail-open/fail-closed error handling by rule group, mode handling).
  Output: context_guard/engine.py
  Refs: FR-7, FR-9, FR-10, TC-009, TC-010, TC-011, TC-012
  Depends on: 5, 6, 7, 8

- [x] 10. Implement `audit/jsonl.py` append-only JSONL writer and `summarize()` for reporting.
  Output: context_guard/audit/jsonl.py
  Refs: FR-11, TC-016
  Depends on: 3

- [x] 11. Implement `adapters/claude_code.py` parse/render for required Claude Code hook events.
  Output: context_guard/adapters/claude_code.py, tests/fixtures/claude_code/*.json
  Refs: FR-1, TC-013, TC-015
  Depends on: 2, 3

- [x] 12. Implement `adapters/codex.py` parse/render for required Codex hook events.
  Output: context_guard/adapters/codex.py, tests/fixtures/codex/*.json
  Refs: FR-2, TC-014, TC-015
  Depends on: 2, 3

- [x] 13. Implement `cli.py` `hook` subcommand wiring adapters + engine + audit together (stdin -> stdout, exit 0 always for parse/policy errors).
  Output: context_guard/cli.py (hook subcommand)
  Refs: design.md#Interfaces and Contracts
  Depends on: 9, 10, 11, 12

- [x] 14. Implement `cli.py` `install claude` and `install codex` subcommands plus `integrations/claude-code/` and `integrations/codex/` templates.
  Output: context_guard/cli.py (install subcommands), integrations/claude-code/, integrations/codex/
  Refs: FR-12, FR-13, TC-017, TC-018
  Depends on: 13

- [x] 15. Implement `cli.py` `validate`, `doctor`, `init` subcommands.
  Output: context_guard/cli.py (validate/doctor/init subcommands)
  Refs: FR-14, FR-16, FR-18, TC-019, TC-021, TC-023
  Depends on: 4, 13

- [x] 16. Implement `cli.py` `test` and `report` subcommands.
  Output: context_guard/cli.py (test/report subcommands)
  Refs: FR-15, FR-17, TC-020, TC-022
  Depends on: 13, 10

## Testing
- [x] 17. Write unit tests for policies/files.py, commands.py, searches.py covering TC-001 through TC-008.
  Output: tests/policies/test_files.py, tests/policies/test_commands.py, tests/policies/test_searches.py
  Refs: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, AC-001, AC-002, AC-003, AC-004, AC-005
  Depends on: 5, 6, 7

- [x] 18. Write unit tests for engine.py mode handling and fail-open/fail-closed behavior covering TC-009 through TC-012.
  Output: tests/test_engine.py
  Refs: TC-009, TC-010, TC-011, TC-012, AC-006
  Depends on: 9

- [x] 19. Write adapter contract tests for Claude Code and Codex covering TC-013 through TC-015.
  Output: tests/adapters/test_claude_code.py, tests/adapters/test_codex.py
  Refs: TC-013, TC-014, TC-015
  Depends on: 11, 12

- [x] 20. Write audit log tests covering TC-016.
  Output: tests/audit/test_jsonl.py
  Refs: TC-016
  Depends on: 10

- [x] 21. Write CLI subprocess tests covering TC-017 through TC-024.
  Output: tests/cli/test_install.py, tests/cli/test_validate.py, tests/cli/test_test_cmd.py, tests/cli/test_doctor.py, tests/cli/test_report.py, tests/cli/test_init.py, tests/cli/test_sessions.py
  Refs: TC-017, TC-018, TC-019, TC-020, TC-021, TC-022, TC-023, TC-024, AC-007, AC-008, AC-009
  Depends on: 14, 15, 16

- [x] 22. Write latency benchmark test covering TC-025.
  Output: tests/perf/test_latency.py
  Refs: TC-025, NFR-1, AC-010
  Depends on: 13

## Documentation
- [x] 23. Write README.md covering install (pipx/uv), quickstart, CLI command reference, and the observe->warn->enforce rollout recommendation from the PRFAQ.
  Output: README.md
  Refs: qa.md#Manual Checks
  Depends on: 14, 15, 16

- [x] 24. Document the default policy schema (fields in defaults/policy.yaml) and config-layering precedence in README.md or a docs/policy.md file.
  Output: docs/policy.md
  Refs: FR-8, design.md#Data Model
  Depends on: 4

