---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "002-compact-runtime"
  artifact: "qa.md"
  path: "specs/002-compact-runtime/qa.md"
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
    - "AC-008"
    - "DEC-002"
    - "TC-001"
    - "TC-002"
    - "TC-009"
  related_artifacts:
    - "specs/002-compact-runtime/decision-log.md"
    - "specs/002-compact-runtime/design.md"
    - "specs/002-compact-runtime/requirements.md"
    - "specs/002-compact-runtime/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "review"
---

# QA

## Change Summary
New capability: adds a `context_guard/compact/` subsystem (artifact store, SQLite ledger, pytest parser chain, compact result builder) and two new CLI subcommands (`context-guard test`, `context-guard artifact show`) implementing PRFAQ Increment 2.1 of the Compact Runtime stage. This is additive to the existing specs/001-context-guard implementation; no existing Stage-1 files are modified beyond `cli.py` gaining new subcommands.

## Acceptance Scenarios
- AC-001 through AC-008 (see requirements.md) exercised via the automated suite mapped in test-cases.md; all must pass before this feature is considered acceptance-ready.
- Manual smoke: run `context-guard test -- pytest` against this repo's own `tests/` (dogfooding specs/001-context-guard's suite) and confirm the compact result correctly summarizes an all-passing run, then intentionally break one test and confirm the compact result correctly isolates the new failure.
- Manual smoke: run the CTX-01 benchmark against `tests/fixtures/compact/` and manually inspect that the reported compression ratio and evidence-preservation outcome look sane before recording them in this file's Evidence Statement.

## Regression Targets
Regression scope for specs/001-context-guard (Stage 1): re-run its full pytest suite (70 tests) to confirm the new `cli.py` subcommands and `context_guard/compact/` package do not break existing `hook`/`install`/`validate`/`test`/`doctor`/`report`/`init` behavior — note the pre-existing Stage-1 `context-guard test` subcommand name must not collide with this increment's new test-execution subcommand (see Risk Notes). Regression scope for this feature going forward: re-run the full pytest suite plus the CTX-01 benchmark whenever parsers, the artifact store schema, or the ledger schema change, since those are the surfaces later increments (2.2-2.5) will build on directly.

## Risk Notes
- CLI name collision: specs/001-context-guard already defines `context-guard test` as the Stage-1 fixture smoke-test subcommand (running the bundled policy-decision fixtures), while this PRFAQ's worked example uses `context-guard test -- pytest` for Compact Runtime's test-execution wrapper. These cannot both be `test`. Resolution (recorded as DEC-002): rename the Stage-1 fixture smoke check to `context-guard selftest` and give Compact Runtime the `test` subcommand name, since the PRFAQ text explicitly shows that exact command form and Compact Runtime is the higher-value, user-facing surface. This is a breaking CLI rename for Stage-1's `test` subcommand; README/docs/tests are updated accordingly.
- Parser correctness risk: an incorrect pytest parser could silently misidentify the failing test; mitigated by TC-001/TC-002/TC-009 asserting exact name/file/line against a known fixture, and by the safe-fallback path never fabricating a diagnosis when uncertain.
- Unbounded artifact retention (see requirements.md Open Questions) is a known residual risk carried forward, not resolved in this increment.
- Benchmark overclaiming risk: mitigated by keeping this qa.md's Evidence Statement as TBD until a clean run is recorded, per the PRFAQ's "Evidence status" notice.

## Validation Commands
- `python3 -m pytest tests/ -q` — full automated suite including new `tests/compact/` and `tests/cli/test_compact_*.py` cases, plus the existing specs/001-context-guard suite (regression).
- `python3 -m pytest tests/compact/test_benchmark_ctx01.py -q` (or equivalent) — CTX-01 benchmark quality gate (compact smaller than baseline AND evidence preserved).
- `context-guard test -- pytest tests/fixtures/compact` — manual dogfood run of the new subcommand itself.
- `context-guard selftest` — confirms the renamed Stage-1 fixture smoke check still passes after the rename (DEC-002).
- `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py specs/002-compact-runtime` and `validate_spec.py specs/002-compact-runtime` — SDD structural gates.
- Defer exact command selection for a given change to `$ai-sdlc-validation`.

## Manual Checks
- Manually run `context-guard test -- pytest` against a suite with an intentionally noisy but all-passing run, then again after introducing one failure, and visually confirm the compact result stays small and correctly isolates the new failure.
- Manually run `context-guard artifact show <id>` and `--fragment <fragment-id>` after a real run and confirm the returned content matches what was actually printed by the underlying test command.
- Manually inspect `.context-guard/ledger.sqlite` (e.g. via the `sqlite3` CLI) after a few runs to confirm rows look correct and no secret/environment values are present.

## Signoff
Signoff requires: all automated tests in test-cases.md passing (including regression of specs/001-context-guard's suite after the `test`/`selftest` rename), the CTX-01 benchmark quality gate passing, AC-001 through AC-008 demonstrated, and at least one manual dogfood run against this repo's own test suite. The benchmark's numeric Evidence Statement (see Benchmark Results below) must be populated from a clean run before any public savings claim is made, per the PRFAQ's "Evidence status" notice. Owner: Dev (implementer); reviewer: user/PM before this claim is published anywhere external.

**Benchmark Results** — populate from a clean run against a named Context Guard version and commit; do not publish with invented or estimated values.

Test environment:

| Field | Value |
| --- | --- |
| Context Guard version | TBD |
| Context Guard commit | TBD |
| Benchmark repository commit | TBD |
| Operating system | TBD |
| Python/runtime version | TBD |
| Benchmark date | TBD |

CTX-01 local context-output benchmark:

| Scenario | Baseline bytes | Compact bytes | Reduction | Evidence preserved | Result |
| --- | --- | --- | --- | --- | --- |
| CTX-01 Noisy test suite | TBD | TBD | TBD | TBD | TBD |

Evidence statement (replace after the benchmark): "In the reproducible local benchmark, Compact Runtime reduced model-facing tool output from TBD bytes to TBD bytes, a reduction of TBD%. The required diagnostic evidence remained available in TBD of 1 scenario tested (CTX-01)."

