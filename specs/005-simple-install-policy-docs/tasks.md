---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-simple-install-policy-docs"
  artifact: "tasks.md"
  path: "specs/005-simple-install-policy-docs/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/005-simple-install-policy-docs/_ai_sdlc/state.toon"
  decision_log: "specs/005-simple-install-policy-docs/decision-log.md"
  status: "review"
  owner: "TBD"
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
    - "AC-008"
    - "AC-009"
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
  related_artifacts:
    - "specs/005-simple-install-policy-docs/decision-log.md"
    - "specs/005-simple-install-policy-docs/design.md"
    - "specs/005-simple-install-policy-docs/plan.md"
    - "specs/005-simple-install-policy-docs/qa.md"
    - "specs/005-simple-install-policy-docs/requirements.md"
    - "specs/005-simple-install-policy-docs/test-cases.md"
    - "specs/005-simple-install-policy-docs/validation.md"
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
- [x] T001 Replace policy layering with one packaged version-2 policy.
  Output: context_guard/policy_config.py, context_guard/defaults/policy.yaml, context_guard/cli.py
  Refs: FR-001, FR-002, AC-001, AC-002, AC-003, TC-001, TC-002, TC-003

- [x] T002 Add the idempotent one-line Bash installer.
  Output: install.sh
  Refs: FR-003, AC-004, AC-005, TC-004, TC-005
  Depends on: T001

- [x] T006 Add local output-reduction analytics and `gain` alias.
  Output: context_guard/compact/ledger.py, context_guard/compact/pipeline.py, context_guard/cli.py
  Refs: FR-006, AC-008, TC-008
  Depends on: T001

- [x] T007 Add command-specific compact proxy and transparent Claude rewrite.
  Output: context_guard/compact/command_proxy.py, context_guard/adapters/claude_code.py
  Refs: FR-007, FR-008, AC-009, AC-010, TC-009, TC-010
  Depends on: T002, T006

## Testing
- [x] T003 Update policy tests and add installer integration tests.
  Output: tests/test_policy_v2.py, tests/test_install_script.py, tests/cli/test_command_proxy_cmd.py, tests/compact/test_command_proxy.py
  Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-009, AC-010, TC-001, TC-002, TC-003, TC-004, TC-005, TC-009, TC-010
  Depends on: T001, T002, T007

- [x] T004 Run focused and full validation.
  Output: specs/005-simple-install-policy-docs/validation.md, specs/005-simple-install-policy-docs/_ai_sdlc/validation-receipt.json
  Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010
  Depends on: T003

## Documentation
- [x] T005 Rewrite README as the sole user guide and remove the docs site.
  Output: README.md; removed docs/ and mkdocs.yml
  Refs: FR-004, FR-005, AC-006, AC-007, TC-006, TC-007
  Depends on: T002, T007
