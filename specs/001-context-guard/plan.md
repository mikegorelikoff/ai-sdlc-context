---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-context-guard"
  artifact: "plan.md"
  path: "/Users/mikegorelikov/ai-sdlc-context/specs/001-context-guard/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "/Users/mikegorelikov/ai-sdlc-context/specs/001-context-guard/_ai_sdlc/state.toon"
  decision_log: "/Users/mikegorelikov/ai-sdlc-context/specs/001-context-guard/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-07-23"
  updated_at: "2026-07-23"
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
- AC-001: requirements.md -> test-cases.md (TC-001, TC-008) -> tasks.md (17) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-002) -> tasks.md (17) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-003, TC-004) -> tasks.md (17) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-005) -> tasks.md (17) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-006, TC-007) -> tasks.md (17) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-011) -> tasks.md (18) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-017) -> tasks.md (21) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-019) -> tasks.md (21) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-020) -> tasks.md (21) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-025) -> tasks.md (22) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] 1: Scaffold the `context_guard` package structure (cli.py, events.py, engine.py, decisions.py, adapters/, policies/, audit/, policy_config.py) with empty/stub modules and `pyproject.toml` packaging metadata.; refs: design.md#Components, design.md#Architecture; output: context_guard/ package skeleton, pyproject.toml
- [x] 2: Implement `events.py` internal Event model and operation_kind classification table.; refs: design.md#Interfaces and Contracts; output: context_guard/events.py
- [x] 3: Implement `decisions.py` Decision model and decision-building helpers (allow/warn/block).; refs: design.md#Interfaces and Contracts; output: context_guard/decisions.py
- [x] 4: Implement `defaults/policy.yaml` and `policy_config.py` layered config loader (built-in -> user -> repo -> env).; refs: design.md#Data Model, FR-8; output: context_guard/defaults/policy.yaml, context_guard/policy_config.py
- [x] 5: Implement `policies/files.py` (deny globs, size thresholds, bounded-range detection).; refs: FR-3, TC-001, TC-002, TC-008; output: context_guard/policies/files.py
- [x] 6: Implement `policies/commands.py` (unbounded log/command pattern detection and require_bounds).; refs: FR-4, TC-003, TC-004; output: context_guard/policies/commands.py
- [x] 7: Implement `policies/searches.py` (path-scope and result-limit enforcement).; refs: FR-5, TC-005, TC-006, TC-007; output: context_guard/policies/searches.py
- [x] 8: Implement `policies/sessions.py` (SessionStart/PreCompact/PostCompact/Stop session-state tracking).; refs: FR-19, FR-20, TC-024; output: context_guard/policies/sessions.py
- [x] 9: Implement `engine.py` dispatch (route Event to policy modules, fail-open/fail-closed error handling by rule group, mode handling).; refs: FR-7, FR-9, FR-10, TC-009, TC-010, TC-011, TC-012; output: context_guard/engine.py
- [x] 10: Implement `audit/jsonl.py` append-only JSONL writer and `summarize()` for reporting.; refs: FR-11, TC-016; output: context_guard/audit/jsonl.py
- [x] 11: Implement `adapters/claude_code.py` parse/render for required Claude Code hook events.; refs: FR-1, TC-013, TC-015; output: context_guard/adapters/claude_code.py, tests/fixtures/claude_code/*.json
- [x] 12: Implement `adapters/codex.py` parse/render for required Codex hook events.; refs: FR-2, TC-014, TC-015; output: context_guard/adapters/codex.py, tests/fixtures/codex/*.json
- [x] 13: Implement `cli.py` `hook` subcommand wiring adapters + engine + audit together (stdin -> stdout, exit 0 always for parse/policy errors).; refs: design.md#Interfaces and Contracts; output: context_guard/cli.py (hook subcommand)
- [x] 14: Implement `cli.py` `install claude` and `install codex` subcommands plus `integrations/claude-code/` and `integrations/codex/` templates.; refs: FR-12, FR-13, TC-017, TC-018; output: context_guard/cli.py (install subcommands), integrations/claude-code/, integrations/codex/
- [x] 15: Implement `cli.py` `validate`, `doctor`, `init` subcommands.; refs: FR-14, FR-16, FR-18, TC-019, TC-021, TC-023; output: context_guard/cli.py (validate/doctor/init subcommands)
- [x] 16: Implement `cli.py` `test` and `report` subcommands.; refs: FR-15, FR-17, TC-020, TC-022; output: context_guard/cli.py (test/report subcommands)
- [x] 17: Write unit tests for policies/files.py, commands.py, searches.py covering TC-001 through TC-008.; refs: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, AC-001, AC-002, AC-003, AC-004, AC-005; output: tests/policies/test_files.py, tests/policies/test_commands.py, tests/policies/test_searches.py
- [x] 18: Write unit tests for engine.py mode handling and fail-open/fail-closed behavior covering TC-009 through TC-012.; refs: TC-009, TC-010, TC-011, TC-012, AC-006; output: tests/test_engine.py
- [x] 19: Write adapter contract tests for Claude Code and Codex covering TC-013 through TC-015.; refs: TC-013, TC-014, TC-015; output: tests/adapters/test_claude_code.py, tests/adapters/test_codex.py
- [x] 20: Write audit log tests covering TC-016.; refs: TC-016; output: tests/audit/test_jsonl.py
- [x] 21: Write CLI subprocess tests covering TC-017 through TC-024.; refs: TC-017, TC-018, TC-019, TC-020, TC-021, TC-022, TC-023, TC-024, AC-007, AC-008, AC-009; output: tests/cli/test_install.py, tests/cli/test_validate.py, tests/cli/test_test_cmd.py, tests/cli/test_doctor.py, tests/cli/test_report.py, tests/cli/test_init.py, tests/cli/test_sessions.py
- [x] 22: Write latency benchmark test covering TC-025.; refs: TC-025, NFR-1, AC-010; output: tests/perf/test_latency.py
- [x] 23: Write README.md covering install (pipx/uv), quickstart, CLI command reference, and the observe->warn->enforce rollout recommendation from the PRFAQ.; refs: qa.md#Manual Checks; output: README.md
- [x] 24: Document the default policy schema (fields in defaults/policy.yaml) and config-layering precedence in README.md or a docs/policy.md file.; refs: FR-8, design.md#Data Model; output: docs/policy.md

## Task Dependencies
- 1: depends on previous applicable task / none
- 2: depends on 1
- 3: depends on 1
- 4: depends on 1
- 5: depends on 2, 3, 4
- 6: depends on 2, 3, 4
- 7: depends on 2, 3, 4
- 8: depends on 2, 3, 4
- 9: depends on 5, 6, 7, 8
- 10: depends on 3
- 11: depends on 2, 3
- 12: depends on 2, 3
- 13: depends on 9, 10, 11, 12
- 14: depends on 13
- 15: depends on 4, 13
- 16: depends on 13, 10
- 17: depends on 5, 6, 7
- 18: depends on 9
- 19: depends on 11, 12
- 20: depends on 10
- 21: depends on 14, 15, 16
- 22: depends on 13
- 23: depends on 14, 15, 16
- 24: depends on 4

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-23

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
