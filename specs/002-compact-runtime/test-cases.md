---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "002-compact-runtime"
  artifact: "test-cases.md"
  path: "specs/002-compact-runtime/test-cases.md"
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
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
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
  related_artifacts:
    - "specs/002-compact-runtime/decision-log.md"
    - "specs/002-compact-runtime/design.md"
    - "specs/002-compact-runtime/requirements.md"
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
Covers the Increment 2.1 vertical slice: subprocess execution/capture, artifact storage, the pytest parser priority chain (junitxml -> text -> safe fallback), compact result construction, drill-down retrieval, minimal ledger recording, and the CTX-01 benchmark. Excludes Increments 2.2-2.5 (logs/build, diff/search, dedup, provider correlation) and excludes live Claude Code/Codex hook integration testing (no live provider available), consistent with specs/001-context-guard's testing approach.

## Scenario Matrix
| TC-001 | AC-001 | Run `context-guard test -- pytest` against the fixture suite (many pass, 1 fail) with junitxml available | compact result reports correct collected/passed/failed totals and the correct failing test name/file/line |
| TC-002 | AC-001 | Same fixture, junitxml disabled/unavailable | text-parser fallback produces the same correct totals and failure identification |
| TC-003 | AC-002 | Compact result's `failures[0].evidence` passed to `artifact show --fragment` | returns the exact diagnostic/traceback fragment for that failure |
| TC-004 | AC-003 | `artifact show <id>` with no `--fragment` | returns the complete raw stdout/stderr captured during the run |
| TC-005 | AC-004 | Run a command whose output no parser recognizes | result includes correct exit status, bounded preview, valid artifact reference, and no fabricated failure |
| TC-006 | AC-005 | Any successful `context-guard test` invocation | exactly one new row appended to `.context-guard/ledger.sqlite` referencing the correct artifact id |
| TC-007 | AC-006 | Run CTX-01 benchmark against the fixture suite | reports all required metrics; compact_output_bytes < baseline_output_bytes; required_evidence_found = true |
| TC-008 | AC-007 | Underlying test command itself fails to launch (e.g. nonexistent binary) | `context-guard test` still returns a structured result with correct exit status and artifact reference, no unhandled crash |
| TC-009 | FR-4 | Multiple distinct failures in one run | each failure has a distinct, correctly identified name/file/line and a distinct evidence reference |
| TC-010 | FR-10 | Any compact result where output was truncated or partially unparsed | `notes` field explicitly states what was grouped/excluded/truncated/unparsed |
| TC-011 | AC-008 | Inspect artifact files and ledger row after a run | no environment-variable values present in either (capture path does not read os.environ) |
| TC-012 | NFR-6 | Malformed junitxml (corrupt XML) | junitxml parser returns None; text parser or fallback produces a valid result without raising |
| TC-013 | design.md#Error Handling | `artifact show` called with an unknown artifact id or unknown fragment id | returns a clear non-zero-exit error, not empty/unrelated content |
| TC-014 | FR-1 | Any `context-guard test` run inside a git repository | artifact meta.json records the correct current commit hash |
| TC-015 | FR-1 | `context-guard test` run outside a git repository (or in a repo with no commits) | commit field is None/absent rather than raising an error |

## Layer Mapping
- Unit layer (`tests/compact/parsers/`): TC-001 (junitxml parser), TC-002 (text parser), TC-005 (fallback parser), TC-009, TC-012.
- Unit layer (`tests/compact/`): TC-003, TC-004, TC-006, TC-011, TC-013, TC-014, TC-015 (artifact_store.py and ledger.py).
- CLI/subprocess layer (`tests/cli/test_compact_test_cmd.py`, `tests/cli/test_compact_artifact_cmd.py`): TC-001, TC-005, TC-006, TC-008.
- Benchmark layer (`tests/compact/test_benchmark_ctx01.py` or a standalone script invoked by CI): TC-007.

## Automation Plan
- All test cases are automated with `pytest`, consistent with specs/001-context-guard.
- `tests/fixtures/compact/` holds a small checked-in pytest fixture suite (e.g. 200 generated passing tests plus 1-2 deliberately failing tests) used by both TC-001/TC-002/TC-007 and the CTX-01 benchmark; the fixture is generated small enough to keep CI fast while still demonstrating a real compression ratio (thousands-line PRFAQ example is illustrative, not a literal CI requirement).
- The CTX-01 benchmark (TC-007) runs as part of the automated suite but its numeric results are also captured into qa.md's evidence section on a clean run against a named commit, per the PRFAQ's "Evidence status" requirement; the automated test only asserts the pass/fail quality gate (compact smaller than baseline AND evidence preserved), not a specific percentage.
- Fixture-based parser tests avoid depending on a live `pytest` subprocess where feasible (feeding captured junitxml/text samples directly to parser functions) to keep unit tests fast and deterministic; TC-001/TC-002/TC-008 use the real subprocess path for end-to-end confidence.

## Open Gaps
- No coverage yet for test frameworks other than pytest (Jest, Go test, JUnit/Java); the parser priority-chain pattern is designed to extend to these, but no parser or fixture exists for them in this increment.
- No automated coverage of the "provider-facing" savings claim (PRFAQ FAQ #11) — this spec only measures local byte/line reduction, not provider-reported tokens, since that requires Increment 2.5's provider usage correlation.
- No retention/cleanup test exists because the retention policy itself is an open question (see requirements.md Open Questions); artifact growth over many runs is not yet bounded or tested.
- No test for concurrent `context-guard test` invocations racing on the same ledger/artifact sequence counter; this increment assumes single-invocation-at-a-time local developer usage.

