---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-real-world-examples"
  artifact: "design.md"
  path: "specs/004-real-world-examples/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/004-real-world-examples/_ai_sdlc/state.toon"
  decision_log: "specs/004-real-world-examples/decision-log.md"
  status: "review"
  owner: "Dev"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids: []
  related_artifacts:
    - "specs/004-real-world-examples/decision-log.md"
    - "specs/004-real-world-examples/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "review"
    - "examples"
---

# Design

## Overview
Add an `examples/` package around existing Context Guard production modules. The demo creates a temporary HOME, installs minimal synthetic skills and provider fixtures, invokes the same inventory/profile/measurement code paths as the CLI, normalizes volatile fields, and compares the result with checked-in output.

## Architecture
`examples/run_demo.py` owns orchestration only. Production logic remains in `context_guard`. Fixture files model provider-native JSONL. The runner writes no state outside `tempfile.TemporaryDirectory` unless `--write` explicitly refreshes `examples/output/demo-output.json`.

## Components
- Demo runner: isolated setup, command invocation, normalization, drift checking.
- Fixtures: minimal Claude usage JSONL, Codex exec JSONL, and synthetic skill manifests.
- Output: one stable JSON document labeled `fixture_evidence`.
- Documentation: sandbox demo, real-local workflow, interpretation and privacy boundary.
- Tests: subprocess execution, output schema, drift, and forbidden-data scan.

## Interfaces and Contracts
`python3 examples/run_demo.py` prints normalized JSON. `--check` compares it with the checked-in output and returns non-zero on drift. `--write` updates only the checked-in output. The JSON top level contains `evidence_kind`, `privacy`, `claude`, and `codex`.

## Data Model
Provider sections contain inventory counts/fingerprint, profile classification outcome, and measured native cache-token counters. Volatile timestamps, PIDs, temporary paths, raw messages, prompts, responses, and source rows are excluded.

## Error Handling
Every subprocess or production API failure terminates with a concise stderr message and non-zero status. Missing fixtures and drift are explicit errors. Temporary state is cleaned automatically.

## Security Considerations
The runner rejects output containing the temporary HOME, current HOME, keys named prompt/response/content/raw/path, or common secret prefixes. Real-local documentation uses explicit paths and never asks users to copy raw logs into the repository.

## Observability
The demo output exposes status, sanitized counts, fingerprints, source digests, and native token totals. It labels evidence as fixture-derived and does not infer cost.

## Risks and Tradeoffs
Fixture output is reproducible but not proof of a 30 percent real-world reduction. The docs make this distinction prominent and direct users to the existing 5x3 qualification workflow for claims.

## Validation Strategy
Run the demo in check mode, its focused tests, the full repository suite, strict MkDocs build, compileall, and `git diff --check`.

## Migration Notes
Additive only. No policy, receipt, profile, measurement, or CLI schema migration.
