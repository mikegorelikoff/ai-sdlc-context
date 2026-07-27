---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "qa-strategy.md"
  path: "specs-refiniment/003-context-guard-product-goal/qa-strategy.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-scope-and-strategy-design"
  flow_mode: "full"
  state_file: "specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  status: "review"
  owner: "Product and QA"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "DEC-026"
  related_artifacts:
    - "specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md"
    - "specs-refiniment/003-context-guard-product-goal/backlog.md"
    - "specs-refiniment/003-context-guard-product-goal/business-context.md"
    - "specs-refiniment/003-context-guard-product-goal/change-impact.md"
    - "specs-refiniment/003-context-guard-product-goal/decision-log.md"
    - "specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md"
    - "specs-refiniment/003-context-guard-product-goal/delivery-spec.md"
    - "specs-refiniment/003-context-guard-product-goal/discovery.md"
    - "specs-refiniment/003-context-guard-product-goal/goal-capability-map.md"
    - "specs-refiniment/003-context-guard-product-goal/prfaq.md"
    - "specs-refiniment/003-context-guard-product-goal/qa-gap-review.md"
    - "specs-refiniment/003-context-guard-product-goal/qa.md"
    - "specs-refiniment/003-context-guard-product-goal/release-slicing.md"
    - "specs-refiniment/003-context-guard-product-goal/requirements-readiness.md"
    - "specs-refiniment/003-context-guard-product-goal/research.md"
    - "specs-refiniment/003-context-guard-product-goal/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-scope-and-strategy-design"
    - "qa-strategy"
    - "review"
    - "gap-004"
---

# qa-strategy.md

## Feature Summary
- Full-flow risk-based strategy for DSR-101–DSR-602 across six slices. Objective: catch unsafe omission, configuration loss, privacy leakage, invalid measurement, and overclaim before live qualification.
- Strategy ready for detailed case synthesis; execution evidence remains pending.

## Actors and Stakeholders
- QA owns strategy, oracles, invalidation, suites, and signoff. Engineering owns testability and provider/recovery fixtures. Security/Privacy owns receipt gates. Product/Delivery own UAT and claim gates. Developers/maintainers cover operator journeys.

## Scope and Boundaries
- In: policy/relevance, supported provider profiles, receipts, runner, measurement, recovery, performance, evidence governance. Out: excluded/post-MVP surfaces and generalized claims.
- Both providers receive separate contract, integration, E2E, performance, and UAT evidence.

## Workflows and Failure Paths
- Cover WF-DS01–WF-DS09 at unit/contract/integration/E2E layers. Every normal flow has safe failure assertions and receipt evidence.
- Invalid/unmeasurable/full-load outcomes are valid expected results; no test infers missing data.

## Requirements and Business Rules
- DSR, BR, story AC, BA AC, and QG mappings are authoritative. Quality/privacy/recovery gates dominate savings.
- Detailed cases must retain valid negatives, exclude invalid attempts, and avoid provider pooling.

## Data, Integrations, and Non-Functional Requirements
- Use versioned synthetic policy/provider/receipt/usage corpora plus frozen repository tasks; live data remains sanitized/local.
- Cover determinism, permissions, atomicity, concurrency, recovery, performance, privacy, and provider isolation.

## Dependencies, Risks, and Constraints
- Execute in slice order; Python 3.10+; provider versions/config supplied locally. Live suites cannot run until adapters and eligibility preflight exist.
- EVID-401 is accumulated suite evidence; CONS-401 is a final governance gate.

## Decisions, Assumptions, and Open Questions
- Accepted authority through DEC-026.
- TS-A01: automation-first below live-provider/UAT layers. Owner: QA + Engineering. Impact: fast deterministic feedback. Resolution/next step: implement fixtures with each slice.
- TS-OQ01: exact CI/local split depends on provider access. Owner: QA + Engineering. Impact: live suites may be local-only. Resolution/next step: bind in environment manifest.

## Success Measures
- 100% DSR coverage; primary/adverse cases per cluster; critical gates in smoke; unchanged behavior in regression; stakeholder-readable UAT; provider-specific qualification evidence.
- Zero hard failures in valid pairs and all statistical/performance/privacy/recovery gates satisfied before release.

## Source Coverage
- Primary: `specs-refiniment/003-context-guard-product-goal/delivery-spec.md`; `specs-refiniment/003-context-guard-product-goal/qa.md`; `specs-refiniment/003-context-guard-product-goal/qa-gap-review.md`; `specs-refiniment/003-context-guard-product-goal/user-stories.md`; `specs-refiniment/003-context-guard-product-goal/release-slicing.md`; `specs-refiniment/003-context-guard-product-goal/decision-log.md`.
- Supporting: `specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md`; `specs-refiniment/003-context-guard-product-goal/backlog.md`; `specs-refiniment/003-context-guard-product-goal/business-context.md`; `specs-refiniment/003-context-guard-product-goal/change-impact.md`; `specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md`; `specs-refiniment/003-context-guard-product-goal/discovery.md`; `specs-refiniment/003-context-guard-product-goal/goal-capability-map.md`; `specs-refiniment/003-context-guard-product-goal/prfaq.md`; `specs-refiniment/003-context-guard-product-goal/requirements-readiness.md`; `specs-refiniment/003-context-guard-product-goal/research.md`; `specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon`.

## Test Scope
- Must test P0: policy/precedence, required-content preservation, actual-state verification, full-load fallback, CAS recovery/user edits, receipt privacy/atomicity, QG enforcement, provider windows/correlation, aggregation, net value, bounded decisions.
- P1: lifecycle ergonomics, diagnostics quality, replay usability, drift messages. Post-MVP: IDE parity and broader repositories.
- Test types: unit/property, CLI, contract, storage/concurrency, integration, frozen-fixture E2E, privacy/security, performance, smoke, regression, UAT, live qualification.

## Risk and Coverage Priorities
| Risk | Likelihood | Impact | Coverage Layer | Priority | Owner |
| --- | --- | --- | --- | --- | --- |
| Required instruction loss | Medium | Critical | unit/property + fixture E2E + UAT | P0 | QA + Engineering |
| Config overwrite/recovery failure | Medium | Critical | concurrency/integration/fault injection | P0 | Engineering |
| Receipt leakage | Medium | Critical | schema/privacy/security/lifecycle | P0 | Security/Privacy + QA |
| Counter/correlation error | High | High | contract + integration + replay | P0 | QA + Engineering |
| Provider drift | High | High | version contract + live smoke | P0 | Engineering |
| Variance/overclaim | High | High | aggregation/property + UAT | P0 | Product + QA |
| Performance regression | Medium | High | benchmark/performance | P0 | Engineering |
| Operator diagnostics | Medium | Medium | CLI/manual/UAT | P1 | QA |

## Layer and Suite Strategy
- Unit/property: precedence, policy merge/migration, fingerprints, statistics, redaction. Contract: provider inventories/actions/events. Integration: leases, filesystem, CLI, adapters. E2E: three frozen tasks and injected failures.
- Smoke: preflight/full-load fallback; valid policy/classification; atomic clean receipt; one supported profile verify/restore; QG blocks failure.
- Regression: existing CLI/hooks/v1 policy, authoritative file stability, unrelated config, local-only/privacy, provider isolation.
- Negative suite: every adverse scenario. UAT: maintainer diagnostics, developer control, QA report, Product/Delivery decisions. Qualification: five valid pairs x three fixtures x provider.

## Test Data Strategy
- Generate immutable fixtures for policy versions/errors, inventory states, profile states, receipts, and provider usage events; use seeded identifiers and known digests.
- Freeze repository/task/model/provider manifests per attempt. Do not store raw prompts/source in evidence.
- Maintain invalid and negative ledgers; never mutate evidence to reach target counts.

## Environment Dependencies
- Fast deterministic suites run without live providers. Adapter contract suites use recorded sanitized fixtures.
- Live smoke/qualification requires pinned supported clients, local credentials/configuration, warm-cache controls, fresh sessions, Python 3.10+, isolated repository state, and clock/timing instrumentation.
- Environment mismatch invalidates rather than skips into a claim.

## Automation Strategy
- Automate all deterministic P0 rules, negative paths, schema/privacy scans, recovery fault injection, measurement math, and report validation.
- Keep manual review for client UX/diagnostics, task semantic equivalence, instruction wording, and claim language; record versioned evidence.
- Gate sequence in CI/local workflow: unit -> contract/storage -> integration/recovery -> fixture E2E -> performance/privacy -> live eligibility -> qualification/UAT.

## Strategy Risks
- Provider-dependent suites may be local and slower; isolate them from fast regression while keeping them mandatory for qualification.
- Frozen fixtures can become stale; version and review them on provider/repository change.
- False oracles are controlled by machine completion plus explicit instruction checks and bounded manual review.
- Strategy verdict: ready for detailed test cases; no definition blockers.
