# Chat output contract registry

Generated from local contracts and executed deterministic simulations. Semantic review is separate; these are not live model runs.

| Skill | Primary table | Secondary table | Failure table | Scenarios | Eval |
| --- | --- | --- | --- | ---: | --- |
| ai-sdlc-approvals-sandbox | Command / Boundary / Escalation / Evidence | Omitted | Blocked command / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-architecture | Component / Responsibility / Decision / Dependency / Evidence | Decision ID / Alternative / Consequence / Evidence | Architecture constraint / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-ba | Requirement ID / Actor / Business rule / Acceptance / Evidence | Assumption / Validation question / Owner / Evidence | Business actor / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-backlog-decomposition-and-task-planning | Task ID / Story / Scope / Depends on / Verification | Story ID / Actor / Outcome / Acceptance | Approved epic / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-backlog-requirements-gap-review | Planning dimension / Gap / Impact / Evidence / Required action | Omitted | Planning scope / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-branching | Current branch / Expected branch / Base revision / Worktree / Decision | Omitted | Task scope / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-change-impact | Changed reference / Affected artifact / Staleness / Evidence / Reopen action | Omitted | Changed reference / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-change-set | Target / Operation / Before / after / Authority / Evidence | Omitted | Change target / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-code-review | Severity / Location / Finding / Evidence / Required fix | Check / Status / Evidence / Coverage gap | Review diff / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-commit-prep | Path group / Disposition / Reason / Verification / Evidence | Commit / Branch / Task ID / Evidence | Commit scope / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-conventional-commit | Subject / Specification / Task ID / Validation / Evidence | Omitted | Change summary / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-delivery-graph | Requirement ID / Task ID / Test ID / Coverage / Evidence | Omitted | Trace source / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-delivery-handoff-review | Delivery gate / Decision / Gap / Evidence / Required action | Omitted | Delivery package / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-delivery-package-gap-review | Workflow / Missing rule / Delivery impact / Evidence / Required action | Omitted | Workflow rule / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-delivery-spec-synthesis | Requirement ID / Behavior / Interface / Constraint / Evidence | Omitted | Accepted story / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-doctor | Check / Installed state / Expected state / Status / Remediation | Omitted | Installation root / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-evidence-council | Topic / Position / Agreement / conflict / Reviewer mode / Evidence | Omitted | Reviewer evidence / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-goal-capability-and-epic-mapping | Goal / Actor / Capability / Epic / Success measure | Capability / Dependency / Owner / Evidence | Business goal / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-host-adapter | Operation / Host mapping / Capability / Fallback / Evidence | Omitted | Host capability / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-navigator | Rank / Next skill / Reason / Expected artifact / Evidence | Omitted | Requested feature / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-package-trust | Control / Expected / Observed / Decision / Evidence | Metric / Count / Evidence | Package manifest / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-policy | Action / Matched rule / Decision / Required gate / Evidence | Omitted | Policy layer / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-prfaq-package-synthesis | Customer / Problem / Proposed outcome / Business evidence / Open decision | FAQ topic / Answer / Evidence / Unresolved choice | Validated discovery / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-project-context | Context fact / Value / Source / Freshness / Use | Omitted | Repository root / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-qa | Scenario ID / Actor / setup / Action / Expected result / Execution status / Evidence | Regression target / Risk / Execution status / Evidence | Acceptance outcome / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-qa-requirements-gap-review | Requirement ID / Testability gap / Risk / Evidence / Required action | Omitted | Requirement source / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-qa-traceability-and-readiness-review | Requirement ID / Test ID / Suite / Coverage status / Blocker / Evidence | Omitted | Test suite / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-quality-lenses | Lens / Severity / Finding / Requirement ID / Evidence / Next action | Omitted | Review artifact / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-release-slicing-and-backlog-readiness-review | Release slice / Included stories / Dependency / Exit criterion / Evidence | Omitted | Release constraint / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-requirements-readiness-review | Requirement dimension / Readiness / Contradiction / gap / Evidence / Required action | Omitted | Requirements package / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-research | Question / Finding / Confidence / Limitation / Evidence | Omitted | Research question / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-retrospective | Observation / Evidence / Improvement proposal / Decision status / Owner | Proposal / Decision reference / Next action / Owner | Observation evidence / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-runtime | Task ID / State / Attempts / Evidence / Next transition | Omitted | Run identity / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-sdd | Artifact / Change / Requirement ID / Validation / Evidence | Component / Responsibility / Decision / Dependency / Evidence | Approved behavior / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-security-testing | Severity / Trust boundary / Finding / Evidence / Remediation | Source / Supported claim / Freshness / Evidence | Trust boundary / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-shared-runtime | Runtime check / Expected / Actual / Status / Evidence | Omitted | Installed helper / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-test-case-and-suite-synthesis | Test ID / Requirement ID / Scenario / Suite / Expected result / Evidence | Omitted | QA strategy / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-test-cases | Test ID / Requirement ID / Setup / trigger / Expected result / Layer / Evidence | Omitted | Acceptance criterion / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-test-scope-and-strategy-design | Coverage target / Risk / Test approach / Data / environment / Exit criterion | Omitted | Testable scope / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-user-story-decomposition | Story ID / Actor / Desired outcome / Acceptance / Dependency | Omitted | Accepted workflow / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-ux | Journey / state / Actor / Behavior / Recovery / Acceptance / Evidence | Omitted | Journey actor / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-validation | Check / Expected / Actual / Status / Evidence | Omitted | Verification command / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-workflow | Stage / Owning skill / Eligibility / Dependency / Expected artifact | Omitted | Workflow intent / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-working-backwards-discovery | Discovery topic / Known evidence / Unresolved question / Decision impact / Owner | Assumption / Validation method / Owner / Evidence | Customer problem / Status / Blocker / Evidence / Required action | 8 | PASS |
