---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "002-compact-runtime"
  artifact: "decision-log.md"
  path: "specs/002-compact-runtime/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/002-compact-runtime/_ai_sdlc/state.toon"
  decision_log: "specs/002-compact-runtime/decision-log.md"
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
    - "decision-log"
    - "draft"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-07-24 | accepted | Dev | Scope this spec to PRFAQ Increment 2.1 (test-output compaction vertical slice: artifact store, deterministic pytest parser, compact result, drill-down, minimal ledger) and defer logs/build/diff/search/dedup/cost-correlation to later increments. | Compact Runtime PRFAQ explicitly recommends "one complete vertical slice" before extending the pattern; specs/001-context-guard already ships the hook-based blocking stage. | Build all 5 increments now; build Increment 2.1 only first (recommended). | requirements.md; design.md; tasks.md | AC-001..AC-008 |
| DEC-002 | 2026-07-24 | accepted | Dev | Rename Stage-1's fixture smoke-test CLI subcommand from `context-guard test` to `context-guard selftest`, freeing `context-guard test -- <command>` for Compact Runtime's test-execution wrapper. | PRFAQ Compact Runtime worked example uses the literal command `context-guard test -- pytest`, which collides with specs/001-context-guard's existing `test` subcommand (bundled fixture smoke check). | Keep Stage-1 name and pick a different Compact Runtime name (e.g. `run-test`); rename Stage-1's subcommand to `selftest` (recommended, preserves the PRFAQ's exact documented UX). | context_guard/cli.py; README.md; docs/policy.md; specs/001-context-guard/tasks.md; tests/cli/test_test_cmd.py | AC-001..AC-008 |
