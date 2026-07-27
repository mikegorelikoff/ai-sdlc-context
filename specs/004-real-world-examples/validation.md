---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-real-world-examples"
  artifact: "validation.md"
  path: "specs/004-real-world-examples/validation.md"
  workspace: "implementation"
  skill: "ai-sdlc-validation"
  flow_mode: "quick"
  state_file: "specs/004-real-world-examples/_ai_sdlc/state.toon"
  decision_log: "specs/004-real-world-examples/decision-log.md"
  status: "validated"
  owner: "Engineering and QA"
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
    - "DEC-001"
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
  related_artifacts:
    - "specs/004-real-world-examples/qa.md"
    - "specs/004-real-world-examples/test-cases.md"
    - "specs/004-real-world-examples/tasks.md"
  validation:
    - "specs/004-real-world-examples/_ai_sdlc/validation-receipt.json"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-validation"
    - "validation"
    - "validated"
    - "examples"
---

# Validation

## Scope

Validate the isolated Claude/Codex demo, provider-native fixture measurement,
profile-planning output, privacy boundary, checked-in output drift detection,
documentation navigation, Python compatibility, full repository regression,
and patch hygiene for the real-world examples package.

## Commands

- V001: regenerate the isolated example in memory and compare it with the
  checked-in privacy-safe JSON.
- V002: run the complete repository suite, including the four example
  subprocess, privacy, native-token, and drift cases.
- Supplemental: build the documentation site with strict link and navigation
  checks; the canonical runner does not allow `mkdocs` as an executable.
- Supplemental: compile production, example, and test Python sources with
  `PYTHONPYCACHEPREFIX=/tmp/context-guard-example-pycache`; the canonical runner
  intentionally does not accept environment assignments.
- V005: validate whitespace and patch hygiene.

## Result

The canonical validation receipt records three zero-exit commands. The
deterministic output reports Claude cache creation/read totals of 1200/3800 and
Codex cached input of 4200 from provider-native fixtures. Paired examples
calculate exact 40% reductions (5000 to 3000 and 4200 to 2520), preserve an
explicitly invoked skill, and demonstrate fail-closed missing-quality and
unsupported-version paths. The extended demo also verifies byte-exact
apply/restore, a Codex cumulative delta of 3200, visible `-20%` regressions, and
stale-inventory denial. The complete
repository suite passes 235 tests, strict documentation build passes, Python
compilation passes, and diff hygiene passes. `uv build` produces a v0.1.1
universal wheel and source distribution, and an isolated wheel-only CLI smoke
test passes. A sanitized read-only smoke check
also found stable real inventories with 27 skills for Claude and 27 for Codex;
that local snapshot is not treated as a savings benchmark.

## Residual Risk

No raw provider session is committed or executed in CI. A real 30 percent
savings claim still requires separately authorized 5x3 baseline/guarded runs
per provider, model, and fixture set.
