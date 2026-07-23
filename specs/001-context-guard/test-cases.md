---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-context-guard"
  artifact: "test-cases.md"
  path: "specs/001-context-guard/test-cases.md"
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
    - "AC-010"
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
    - "specs/001-context-guard/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "review"
---

# Test Cases

## Scope
Covers deterministic policy evaluation (files, commands, searches, sessions), both provider adapters (Claude Code, Codex), the config-layering resolution order, the three enforcement modes (observe/warn/enforce), fail-open/fail-closed error handling, CLI subcommands (install/validate/test/doctor/report/init), and the latency NFR. Excludes load/stress testing beyond the single latency benchmark and excludes live-provider integration testing (fixture-based only, per NFR-8).

## Scenario Matrix
| TC-001 | AC-001 | Full read of `dist/bundle.min.js` (deny glob + oversized) with no bounded range, mode=enforce | decision=block, message present, suggestion includes bounded-range example |
| TC-002 | AC-002 | Same event as TC-001 but mode=observe | decision=allow; audit record shows would-block with matched rule id |
| TC-003 | AC-003 | Command `docker compose logs api`, mode=enforce | decision=block; suggestions include `--tail` and `--since` forms |
| TC-004 | AC-003 | Command `docker compose logs --tail 200 api`, mode=enforce | decision=allow |
| TC-005 | AC-004 | Command `rg "PaymentService" src/payment`, mode=enforce | decision=allow, no warning |
| TC-006 | AC-005 | Command `find . -type f`, search.require_path_scope=true, mode=enforce | decision=block with explanation |
| TC-007 | AC-005 | Command `grep -R "term" .`, mode=enforce | decision=block with explanation |
| TC-008 | AC-001 | Bounded read of large source file (explicit line range requested), mode=enforce | decision=allow |
| TC-009 | FR-7 | Same block-eligible event evaluated once per mode (observe, warn, enforce) | observe=allow+would-block audit; warn=allow+warning message; enforce=block |
| TC-010 | FR-8 | Policy layering: repo config overrides user config overrides built-in default for `max_full_read_bytes` | effective value equals repo-config value |
| TC-011 | AC-006 | Policy module raises unhandled exception during evaluation of a cost/token rule | decision=allow (fail-open); audit record rule="internal-error" |
| TC-012 | FR-10 | Policy module raises unhandled exception for a rule id in `fail_closed_rules` | decision=block (fail-closed); generic verification-failure message |
| TC-013 | FR-1/FR-2 | Adapter parses each required Claude Code event (PreToolUse, PostToolUse, PostToolUseFailure, SessionStart, PreCompact, Stop) from fixture JSON | Event populated with correct operation_kind and fields for each |
| TC-014 | FR-2 | Adapter parses each required Codex event (PreToolUse, PostToolUse, PreCompact, PostCompact, SessionStart, Stop) from fixture JSON | Event populated with correct operation_kind and fields for each |
| TC-015 | FR-6 | Decision.render for Claude Code vs Codex for the same internal Decision(status=block) | each adapter emits its own provider-shaped JSON, both containing message and suggestions |
| TC-016 | FR-11 | Any evaluated event | exactly one JSONL audit record appended; record excludes full prompt/file/output/env/secret content by default |
| TC-017 | AC-007 | Run `context-guard install claude` twice against a temp config containing a pre-existing unrelated hook | config identical after 2nd run; unrelated hook entry still present |
| TC-018 | FR-13 | Run `context-guard install codex` against a temp config.toml | Context Guard hook entries added for required events; existing unrelated keys untouched |
| TC-019 | AC-008 | Run `context-guard validate` against an invalid `policy.yaml` (bad YAML/schema) | non-zero exit; explicit error message identifying the invalid field |
| TC-020 | AC-009 | Run `context-guard test` with >=5 fixtures covering the 5 required high-cost patterns | all fixtures pass with expected decision |
| TC-021 | FR-16 | Run `context-guard doctor` | reports Python version, resolved policy layer chain, hook install status |
| TC-022 | FR-17 | Run `context-guard report` after several audit events including blocks | summary shows prevented-bytes/lines/operation counts labeled as an estimate |
| TC-023 | FR-18 | Run `context-guard init` in a repo with an existing `policy.yaml` | existing file left unmodified; warning printed, no overwrite |
| TC-024 | FR-19/FR-20 | SessionStart followed by repeated large reads of the same path, then PreCompact | session state records repeated-read count and cumulative prevented-context estimate; compaction checkpoint audit event recorded |
| TC-025 | AC-010 | Run 100 sequential fixture evaluations via the CLI subprocess path | median wall-clock latency < 100 ms |

## Layer Mapping
- Unit layer (`tests/policies/`): TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012.
- Adapter/contract layer (`tests/adapters/`, fixture-based): TC-013, TC-014, TC-015.
- Audit layer (`tests/audit/`): TC-016.
- CLI/subprocess layer (`tests/cli/`): TC-017, TC-018, TC-019, TC-020, TC-021, TC-022, TC-023, TC-024.
- Performance layer (`tests/perf/`): TC-025.

## Automation Plan
- All test cases are automated with `pytest`; no manual-only test cases in this MVP.
- Fixture JSON payloads for Claude Code and Codex hook events live under `tests/fixtures/claude_code/` and `tests/fixtures/codex/` and are versioned in the repo so adapter contract tests do not depend on a live provider.
- `context-guard test` (FR-15) runs a curated subset of the fixture-based CLI/adapter tests as an end-user-facing smoke check; the full suite runs via `pytest` in CI/local dev.
- The latency benchmark (TC-025) runs as a marked `@pytest.mark.perf` test excluded from default fast test runs but included in `$ai-sdlc-validation` full-flow checks before commit prep.
- Install idempotency tests (TC-017, TC-018) operate against temp directories (`tmp_path` fixture) and never touch the developer's real `~/.claude` or Codex config.

## Open Gaps
- No test coverage yet for real Claude Code / Codex hook schema drift beyond captured fixtures; a contract-test refresh process against future provider schema releases is not yet defined (tracks requirements Open Questions on hook schema versions).
- No automated test for the exact repo-level policy file path/name (`.context-guard/policy.yaml` vs alternatives) since that path is not yet decided (see requirements Open Questions).
- No test for behavior on Windows; NFR-4 only requires macOS/Linux support for MVP.
- Pilot false-positive rate (<5%) from the PRFAQ success criteria is a field metric gathered during the Phase 2 repository pilot, not something unit/CLI tests can directly assert.

