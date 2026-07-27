---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-real-world-examples"
  artifact: "test-cases.md"
  path: "specs/004-real-world-examples/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/004-real-world-examples/_ai_sdlc/state.toon"
  decision_log: "specs/004-real-world-examples/decision-log.md"
  status: "review"
  owner: "QA"
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
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
  related_artifacts:
    - "specs/004-real-world-examples/decision-log.md"
    - "specs/004-real-world-examples/design.md"
    - "specs/004-real-world-examples/plan.md"
    - "specs/004-real-world-examples/qa.md"
    - "specs/004-real-world-examples/requirements.md"
    - "specs/004-real-world-examples/tasks.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "review"
    - "examples"
---

# Test Cases

## Scope
Cover deterministic execution, provider evidence, privacy, drift, and documentation links.

## Scenario Matrix
| ID | Requirement | Scenario | Expected |
| --- | --- | --- | --- |
| TC-001 | AC-001 | Run demo with `--check` | Exit 0 and output equals checked-in JSON. |
| TC-002 | AC-002 | Run demo from a HOME containing sentinel private data | Sentinel and absolute HOME never appear in output. |
| TC-003 | AC-003 | Inspect Claude fixture evidence | Cache creation/read totals match native JSONL counters. |
| TC-004 | AC-003 | Inspect Codex fixture evidence | Cached input total matches native JSONL counter. |
| TC-005 | AC-004 | Inspect inventory/profile summaries | Both providers show stable counts and only irrelevant skills disabled. |
| TC-006 | AC-006 | Mutate expected output | Check mode exits non-zero with drift error. |
| TC-007 | AC-006 | Scan generated JSON | Forbidden raw/path/prompt/response/content keys are absent. |
| TC-008 | AC-005, AC-007 | Build docs strictly | Example page and navigation resolve. |

## Layer Mapping
- Unit/subprocess: TC-001..TC-007.
- Documentation integration: TC-008.
- Full regression: existing repository suite.

## Automation Plan
Add `tests/examples/test_run_demo.py` invoking the runner in a subprocess, parsing JSON, verifying fixture totals, forcing drift against a copied expected file, and scanning recursively for forbidden keys and home paths.

## Open Gaps
Real 5x3 provider qualification requires 15 authorized paired runs per provider and remains an operator workflow, not CI.
