---
title: Deterministic execution
description: Product-specific execution boundaries, fixed inputs, serialization and reproducibility checks.
---

# Deterministic execution boundaries

Mechanical discovery, parsing, state validation and serialization belong to Python helpers. Semantic interpretation remains with the skill, using the evidence and native output named in its own execution contract. A successful helper is evidence of its implemented checks, not proof of semantic correctness or user approval.

The table maps each skill to its existing entry point. Other local helpers retain their existing contracts; this registry does not replace CLI help or install a new workflow engine. Source order remains semantic for histories; mappings and generated file collections use canonical ordering.

| Skill | Python entry point | Owned Python files |
| --- | --- | ---: |
| `ai-sdlc-approvals-sandbox` | `.claude/skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py` | 1 |
| `ai-sdlc-architecture` | `.claude/skills/ai-sdlc-architecture/scripts/architecture.py` | 1 |
| `ai-sdlc-ba` | `.claude/skills/ai-sdlc-ba/scripts/ba_context_scaffold.py` | 1 |
| `ai-sdlc-backlog-decomposition-and-task-planning` | `.claude/skills/ai-sdlc-backlog-decomposition-and-task-planning/scripts/backlog_matrix.py` | 1 |
| `ai-sdlc-backlog-requirements-gap-review` | `.claude/skills/ai-sdlc-backlog-requirements-gap-review/scripts/backlog_gap_scan.py` | 1 |
| `ai-sdlc-branching` | `.claude/skills/ai-sdlc-branching/scripts/branch_plan.py` | 1 |
| `ai-sdlc-change-impact` | `.claude/skills/ai-sdlc-change-impact/scripts/change_impact.py` | 1 |
| `ai-sdlc-change-set` | `.claude/skills/ai-sdlc-change-set/scripts/change_set.py` | 4 |
| `ai-sdlc-code-review` | `.claude/skills/ai-sdlc-code-review/scripts/review_readiness.py` | 1 |
| `ai-sdlc-commit-prep` | `.claude/skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py` | 1 |
| `ai-sdlc-conventional-commit` | `.claude/skills/ai-sdlc-conventional-commit/scripts/validate_commit_msg.py` | 1 |
| `ai-sdlc-delivery-graph` | `.claude/skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py` | 2 |
| `ai-sdlc-delivery-handoff-review` | `.claude/skills/ai-sdlc-delivery-handoff-review/scripts/handoff_readiness_score.py` | 1 |
| `ai-sdlc-delivery-package-gap-review` | `.claude/skills/ai-sdlc-delivery-package-gap-review/scripts/delivery_gap_scan.py` | 1 |
| `ai-sdlc-delivery-spec-synthesis` | `.claude/skills/ai-sdlc-delivery-spec-synthesis/scripts/delivery_spec_scaffold.py` | 1 |
| `ai-sdlc-doctor` | `.claude/skills/ai-sdlc-doctor/scripts/doctor.py` | 1 |
| `ai-sdlc-evidence-council` | `.claude/skills/ai-sdlc-evidence-council/scripts/evidence_council.py` | 1 |
| `ai-sdlc-goal-capability-and-epic-mapping` | `.claude/skills/ai-sdlc-goal-capability-and-epic-mapping/scripts/goal_capability_map.py` | 1 |
| `ai-sdlc-host-adapter` | `.claude/skills/ai-sdlc-host-adapter/scripts/adapter.py` | 1 |
| `ai-sdlc-navigator` | `.claude/skills/ai-sdlc-navigator/scripts/navigate.py` | 1 |
| `ai-sdlc-package-trust` | `.claude/skills/ai-sdlc-package-trust/scripts/metrics.py` | 2 |
| `ai-sdlc-policy` | `.claude/skills/ai-sdlc-policy/scripts/policy.py` | 1 |
| `ai-sdlc-prfaq-package-synthesis` | `.claude/skills/ai-sdlc-prfaq-package-synthesis/scripts/prfaq_outline.py` | 1 |
| `ai-sdlc-project-context` | `.claude/skills/ai-sdlc-project-context/scripts/project_context.py` | 3 |
| `ai-sdlc-qa-requirements-gap-review` | `.claude/skills/ai-sdlc-qa-requirements-gap-review/scripts/qa_gap_scan.py` | 1 |
| `ai-sdlc-qa-traceability-and-readiness-review` | `.claude/skills/ai-sdlc-qa-traceability-and-readiness-review/scripts/traceability_matrix.py` | 1 |
| `ai-sdlc-qa` | `.claude/skills/ai-sdlc-qa/scripts/qa_plan_scaffold.py` | 1 |
| `ai-sdlc-quality-lenses` | `.claude/skills/ai-sdlc-quality-lenses/scripts/quality_lens_report.py` | 1 |
| `ai-sdlc-release-slicing-and-backlog-readiness-review` | `.claude/skills/ai-sdlc-release-slicing-and-backlog-readiness-review/scripts/release_slice_plan.py` | 1 |
| `ai-sdlc-requirements-readiness-review` | `.claude/skills/ai-sdlc-requirements-readiness-review/scripts/requirements_readiness_score.py` | 1 |
| `ai-sdlc-research` | `.claude/skills/ai-sdlc-research/scripts/research.py` | 1 |
| `ai-sdlc-retrospective` | `.claude/skills/ai-sdlc-retrospective/scripts/retrospective.py` | 1 |
| `ai-sdlc-runtime` | `.claude/skills/ai-sdlc-runtime/scripts/runtime.py` | 1 |
| `ai-sdlc-sdd` | `.claude/skills/ai-sdlc-sdd/scripts/sdd_context.py` | 11 |
| `ai-sdlc-security-testing` | `.claude/skills/ai-sdlc-security-testing/scripts/security_review_matrix.py` | 1 |
| `ai-sdlc-shared-runtime` | `.claude/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_state_machine.py` | 22 |
| `ai-sdlc-test-case-and-suite-synthesis` | `.claude/skills/ai-sdlc-test-case-and-suite-synthesis/scripts/suite_outline.py` | 1 |
| `ai-sdlc-test-cases` | `.claude/skills/ai-sdlc-test-cases/scripts/case_matrix.py` | 1 |
| `ai-sdlc-test-scope-and-strategy-design` | `.claude/skills/ai-sdlc-test-scope-and-strategy-design/scripts/strategy_scaffold.py` | 1 |
| `ai-sdlc-user-story-decomposition` | `.claude/skills/ai-sdlc-user-story-decomposition/scripts/story_map.py` | 1 |
| `ai-sdlc-ux` | `.claude/skills/ai-sdlc-ux/scripts/ux.py` | 1 |
| `ai-sdlc-validation` | `.claude/skills/ai-sdlc-validation/scripts/run_validation.py` | 2 |
| `ai-sdlc-workflow` | `.claude/skills/ai-sdlc-workflow/scripts/workflow.py` | 1 |
| `ai-sdlc-working-backwards-discovery` | `.claude/skills/ai-sdlc-working-backwards-discovery/scripts/discovery_interview_plan.py` | 1 |

## Reproducibility and failure policy

State serialization rejects unknown fields, duplicate stage identities, invalid statuses and ambiguous mapping keys. Quoted values preserve commas, line breaks and control characters. The state API accepts an explicit `observed_on` date; default observation time remains a domain input. Equal-content atomic writes are safe no-ops; failed replacement preserves the previous artifact. Repeated identical assumptions are not duplicated.

Each skill bounds semantic repair to two attempts and preserves the owning runtime's stricter retry policy. Validation errors do not authorize a new route or overwrite valid evidence. Native formats remain native; presentation statuses never control lifecycle transitions.

Contributor-skill test files are executed by the normal product suite despite their hidden directory. Isolated fixtures verify installed runtime independence, SDD projection drift and first-write journal references; retired mirror paths are not recreated.
