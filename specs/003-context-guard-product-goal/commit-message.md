---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "commit-message.md"
  path: "specs/003-context-guard-product-goal/commit-message.md"
  workspace: "implementation"
  skill: "ai-sdlc-conventional-commit"
  flow_mode: "full"
  state_file: "specs/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs/003-context-guard-product-goal/decision-log.md"
  status: "approved"
  owner: "Engineering"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "T001"
    - "T020"
    - "AC-001"
    - "AC-063"
    - "DEC-005"
  related_artifacts:
    - "specs/003-context-guard-product-goal/commit-readiness.md"
    - "specs/003-context-guard-product-goal/validation.md"
  validation:
    - "conventional commit validator: passed with full traceability"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-conventional-commit"
    - "commit-message"
    - "approved"
---

# Commit Message

feat(context-guard): add guarded cache-token optimization

Spec: specs/003-context-guard-product-goal
Task: T001, T002, T003, T004, T005, T006, T007, T008, T009, T010, T011, T012, T013, T014, T015, T016, T017, T018, T019, T020

Business context:
Reduce avoidable Claude Code and Codex cache-token usage while preserving required instructions, task quality, local privacy, and safe recovery.

Implementation details:

- Add policy-v2 skill classification, authoritative inventories, privacy-safe receipts, reversible guarded profiles, and provider-neutral quality gates.
- Measure native Claude cache read and write tokens plus Codex cached input through exact or cumulative evidence.
- Add exact paired statistics, five-by-three provider qualification, documentation, lifecycle traceability, and symlink-safe private storage.

Change flow:

```text
Stable inventory -> guarded profile -> quality-authorized measurement -> 30 percent qualification
```

How to test:

1. Run the repository suite and inspect the profile, receipt, quality, and measurement negative paths.
2. Build documentation strictly and verify the SDD, code-review, security-review, and validation artifacts.

Validation:

- `python3 tests/run_pytest.py -q` -> 229 passed
- `python3 -m mkdocs build --strict` -> passed
- `PYTHONPYCACHEPREFIX=/tmp/context-guard-pycache python3 -m compileall -q context_guard tests` -> passed
- `git diff --check` -> passed
