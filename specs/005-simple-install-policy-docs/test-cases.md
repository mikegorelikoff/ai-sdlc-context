---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-simple-install-policy-docs"
  artifact: "test-cases.md"
  path: "specs/005-simple-install-policy-docs/test-cases.md"
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
    - "specs/005-simple-install-policy-docs/tasks.md"
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
Single-policy resolution, reduced CLI surface, Bash installer behavior, README completeness, and removed docs site.

## Scenario Matrix
| ID | Requirement | Scenario | Expected |
| --- | --- | --- | --- |
| TC-001 | AC-001 | Load policy with no overrides | Exactly packaged policy source and version 2 |
| TC-002 | AC-002 | Create user/repo policies and set mode environment variable | Effective policy remains packaged values |
| TC-003 | AC-003 | Render CLI help | No init or migrate-policy commands |
| TC-004 | AC-004 | Run installer with isolated roots and local package | Executable plus both provider configs exist |
| TC-005 | AC-005 | Run installer twice with unrelated hooks/config | Output configuration is stable and unrelated data remains |
| TC-006 | AC-006 | Check README sections and local links | Installation through removal guidance is present; links resolve |
| TC-007 | AC-007 | Inspect tracked tree | docs directory and mkdocs.yml are absent |
| TC-008 | AC-008 | Run compact command and request report/gain | Local aggregate contains byte reduction and estimated tokens with billing caveat |
| TC-009 | AC-009 | Proxy successful, repetitive, and failing commands | Output is bounded/deduplicated, artifact is complete, exit code is preserved |
| TC-010 | AC-010 | Rewrite supported simple and compound/mutating commands | Simple supported command receives updatedInput; other commands pass through |

## Layer Mapping
- Unit: TC-001 through TC-003.
- Installer integration: TC-004 and TC-005.
- Repository/documentation: TC-006 and TC-007.

## Automation Plan
Add policy/CLI tests and `tests/test_install_script.py`; run all tests through `uv run pytest`; run shell syntax validation with `bash -n install.sh`.

## Open Gaps
- None.
