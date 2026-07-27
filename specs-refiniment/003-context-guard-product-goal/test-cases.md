---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "test-cases.md"
  path: "specs-refiniment/003-context-guard-product-goal/test-cases.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-cases"
  flow_mode: "full"
  state_file: "specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  status: "review"
  owner: "Product and QA"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "BR-101"
    - "BR-112"
    - "BR-201"
    - "BR-212"
    - "DEC-024"
    - "DEC-026"
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
    - "TC-011"
    - "TC-012"
    - "TC-013"
    - "TC-014"
    - "TC-015"
    - "TC-016"
    - "TC-017"
    - "TC-018"
    - "TC-019"
    - "TC-020"
    - "TC-021"
    - "TC-022"
    - "TC-023"
    - "TC-024"
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
    - "specs-refiniment/003-context-guard-product-goal/qa-strategy.md"
    - "specs-refiniment/003-context-guard-product-goal/qa.md"
    - "specs-refiniment/003-context-guard-product-goal/release-slicing.md"
    - "specs-refiniment/003-context-guard-product-goal/requirements-readiness.md"
    - "specs-refiniment/003-context-guard-product-goal/research.md"
    - "specs-refiniment/003-context-guard-product-goal/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-cases"
    - "test-cases"
    - "review"
    - "gap-005"
---

# test-cases.md

## Feature Summary
- Full-flow executable case design for the 12 delivery requirement clusters (DSR-101–DSR-602). It covers deterministic local behavior, both provider boundaries, quality and privacy gates, recovery, measurement, and bounded rollout decisions.

## Actors and Stakeholders
- Developers and maintainers exercise local controls and diagnostics. Engineering supplies deterministic implementations and fixtures. QA owns oracles and invalidation. Security/Privacy owns receipt checks. Product and Delivery own UAT and claim gates.

## Scope and Boundaries
- In scope: WF-DS01–WF-DS09, policy v2, provider profiles, receipts, quality runner, measurement, performance, recovery, and evidence governance. Out of scope: excluded surfaces and generalized claims.
- Claude and Codex are always tested and reported separately.

## Workflows and Failure Paths
- Every DSR cluster has a primary and adverse scenario. Unsupported, ambiguous, mismatched, corrupt, concurrent, or unmeasurable states resolve to full load or invalid evidence without destructive mutation.
- Required/safety content, user edits, privacy, and quality gates are hard invariants.

## Requirements and Business Rules
- Cases trace to DSR-101–DSR-602 and inherit BR-101–BR-112, BR-201–BR-212, DEC-024, story acceptance criteria, and QG-301–QG-309.
- Savings never overrides quality, privacy, recovery, correlation, or performance failures.

## Data, Integrations, and Non-Functional Requirements
- Versioned synthetic fixtures cover policies, inventories, provider states, receipts, and usage events; frozen repository tasks cover end-to-end oracles. Live evidence uses pinned provider/model/client manifests.
- Assertions cover determinism, atomicity, locking, CAS restoration, redaction, provider isolation, p95 <=750 ms, maximum <=2 s, and prompt limits.

## Dependencies, Risks, and Constraints
- Execute by release-slice dependency order. Live cases require locally supplied supported clients and credentials; absence invalidates qualification but does not block deterministic implementation tests.
- Python 3.10+ is the qualification floor. Provider drift requires contract requalification.

## Decisions, Assumptions, and Open Questions
- Accepted authority through DEC-026. No coverage exclusion is accepted.
- Execution question TC-OQ01: live-provider placement is environment-dependent. Owner: QA + Engineering. Impact: qualification may be local-only. Resolution/next step: bind the runnable command and pinned provider versions in the implementation environment manifest.

## Success Measures
- 100% DSR primary/adverse design coverage; zero hard failures; provider-separated valid-pair statistics; complete receipt/privacy/recovery evidence; all net-value gates pass before qualification.

## Source Coverage
- Primary: `specs-refiniment/003-context-guard-product-goal/delivery-spec.md`; `specs-refiniment/003-context-guard-product-goal/qa.md`; `specs-refiniment/003-context-guard-product-goal/qa-gap-review.md`; `specs-refiniment/003-context-guard-product-goal/qa-strategy.md`; `specs-refiniment/003-context-guard-product-goal/user-stories.md`; `specs-refiniment/003-context-guard-product-goal/decision-log.md`.
- Supporting: `specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md`; `specs-refiniment/003-context-guard-product-goal/backlog.md`; `specs-refiniment/003-context-guard-product-goal/business-context.md`; `specs-refiniment/003-context-guard-product-goal/change-impact.md`; `specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md`; `specs-refiniment/003-context-guard-product-goal/discovery.md`; `specs-refiniment/003-context-guard-product-goal/goal-capability-map.md`; `specs-refiniment/003-context-guard-product-goal/prfaq.md`; `specs-refiniment/003-context-guard-product-goal/release-slicing.md`; `specs-refiniment/003-context-guard-product-goal/requirements-readiness.md`; `specs-refiniment/003-context-guard-product-goal/research.md`; `specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon`.

## Scenario Matrix
| Scenario ID | Requirement Ref | Type | Preconditions | Expected Outcome |
| --- | --- | --- | --- | --- |
| TC-S01P | DSR-101 | happy | supported surface and stable inventory | preflight records exact authoritative identities and fingerprints |
| TC-S01N | DSR-101 | negative | unsupported surface, duplicate, or stale inventory | no mutation; full-load reason is recorded |
| TC-S02P | DSR-102 | happy | valid v2 policy and exact irrelevant identity | deterministic effective classification permits bounded reduction |
| TC-S02N | DSR-102 | boundary | invalid version, conflict, or explicit required rule | diagnostic is stable and complete content remains visible |
| TC-S03P | DSR-201 | integration | supported Claude profile and uncontended lease | requested state is verified before a fresh session |
| TC-S03N | DSR-201 | recovery | mismatch, contention, or user edit during Claude run | full load or CAS-safe restore preserves the edit |
| TC-S04P | DSR-202 | integration | supported Codex CLI/app-server profile | actual state is verified before thread start and restored |
| TC-S04N | DSR-202 | recovery | unsupported profile, dead lease, or user edit | no unsafe mutation; recovery is bounded and non-destructive |
| TC-S05P | DSR-301 | storage | valid sanitized attempt data | atomic schema-valid receipt is written with restrictive access |
| TC-S05N | DSR-301 | privacy | interrupted write or prohibited content supplied | no partial valid receipt and prohibited content is rejected |
| TC-S06P | DSR-302 | lifecycle | completed unreferenced local receipts | inspect/delete/retention/prune behave deterministically |
| TC-S06N | DSR-302 | concurrency | active, referenced, corrupt, or concurrently accessed receipt | record is retained/locked/quarantined without data loss |
| TC-S07P | DSR-401 | E2E | three frozen tasks with complete instruction oracle | guarded result matches baseline quality and instructions |
| TC-S07N | DSR-401 | negative | fingerprint drift or missing explicit instruction | attempt fails its quality gate and cannot reach savings |
| TC-S08P | DSR-402 | gate | QG-301–QG-309 all pass | token evaluation is enabled and evidence references are retained |
| TC-S08N | DSR-402 | gate | any quality/privacy/recovery gate fails | savings is inaccessible and attempt is marked invalid |
| TC-S09P | DSR-501 | measurement | five correlated Claude pairs per fixture | deduplicated creation+read totals and statistics are correct |
| TC-S09N | DSR-501 | negative | duplicate, drifted, or uncorrelated Claude event | attempt is invalid with no zero substitution |
| TC-S10P | DSR-502 | measurement | exact Codex event or validated cumulative boundary | cached-input total and delta are correct and traceable |
| TC-S10N | DSR-502 | negative | missing boundary, reset, or ambiguous correlation | measurement is invalid and excluded with reason |
| TC-S11P | DSR-601 | performance | qualifying local run | p95, maximum, and prompt gates pass |
| TC-S11N | DSR-601 | boundary | threshold or prompt limit exceeded | rollout is blocked regardless of savings |
| TC-S12P | DSR-602 | UAT | both provider packages independently pass | bounded combined MVP decision may be approved |
| TC-S12N | DSR-602 | governance | stale authority or either provider fails | combined decision is blocked and claim scope stays bounded |

## Detailed Test Cases
| Test ID | Scenario Ref | Steps | Expected Result | Priority | Automation |
| --- | --- | --- | --- | --- | --- |
| TC-001 | TC-S01P | run preflight twice over supported fixture | identical ordered identities/fingerprints and supported status | P0 | pytest provider contract |
| TC-002 | TC-S01N | inject unsupported/duplicate/stale inventory | no provider mutation; explicit full-load code | P0 | pytest negative contract |
| TC-003 | TC-S02P | load layered v2 policy and classify exact ID twice | same effective source/classification and bounded action | P0 | pytest unit/property |
| TC-004 | TC-S02N | load invalid/conflicting/required variants | nonzero diagnostic; complete content retained | P0 | pytest unit/CLI |
| TC-005 | TC-S03P | acquire lease, request Claude profile, verify, start | verified state precedes fresh session | P0 | pytest integration |
| TC-006 | TC-S03N | inject mismatch/contention/edit then restore | full load or safe CAS; user edit unchanged | P0 | pytest fault injection |
| TC-007 | TC-S04P | apply Codex profile then start thread and restore | verified state and exact baseline restoration | P0 | pytest integration |
| TC-008 | TC-S04N | inject unsupported/dead lease/edit | bounded recovery and no destructive overwrite | P0 | pytest fault injection |
| TC-009 | TC-S05P | write sanitized attempt then reopen | complete atomic receipt, schema and mode pass | P0 | pytest storage/privacy |
| TC-010 | TC-S05N | interrupt write and submit prohibited fields | partial quarantined/absent; prohibited data rejected | P0 | pytest fault/privacy |
| TC-011 | TC-S06P | inspect, delete target, age and prune records | only eligible target/data is removed | P1 | pytest CLI/storage |
| TC-012 | TC-S06N | prune active/referenced/corrupt/concurrent records | active retained, corrupt quarantined, locking enforced | P0 | pytest concurrency |
| TC-013 | TC-S07P | run baseline/guarded frozen fixtures | all machine and instruction oracles pass | P0 | pytest E2E |
| TC-014 | TC-S07N | alter fingerprint/remove required instruction | gate fails before measurement | P0 | pytest E2E negative |
| TC-015 | TC-S08P | provide passing QG evidence | measurement transition becomes eligible | P0 | pytest gate state machine |
| TC-016 | TC-S08N | fail each QG in table-driven runs | every failure blocks token access | P0 | pytest gate parameterization |
| TC-017 | TC-S09P | replay correlated Claude events and aggregate | totals, median, Q1, fixture results match oracle | P0 | pytest contract/statistics |
| TC-018 | TC-S09N | replay duplicate/drift/uncorrelated events | invalid ledger records reason; no fabricated value | P0 | pytest negative replay |
| TC-019 | TC-S10P | replay exact and cumulative Codex fixtures | exact/delta totals match oracle | P0 | pytest contract/statistics |
| TC-020 | TC-S10N | remove/reset/ambiguate boundary | invalid measurement with explicit reason | P0 | pytest negative replay |
| TC-021 | TC-S11P | benchmark qualifying fixture population | p95 <=750 ms, max <=2 s, prompt limits pass | P0 | benchmark suite |
| TC-022 | TC-S11N | inject latency and prompt threshold breaches | rollout gate fails despite positive savings | P0 | benchmark negative |
| TC-023 | TC-S12P | assemble two independently passing packages | report permits bounded combined approval | P0 | pytest report + UAT |
| TC-024 | TC-S12N | fail one provider or use stale authority | report blocks combined approval and explains scope | P0 | pytest report + UAT |

## Permission and Negative Cases
- Only repository maintainers change repository policy; developer controls apply only to the local guarded run and local receipts. QA may invalidate evidence but cannot alter provider data. Product/Delivery cannot override safety, privacy, quality, recovery, or net-value gates.
- Negative cases cover unsupported versions/surfaces, duplicate/conflicting identity, invalid policy, contention, stale/dead leases, user edits, corrupt receipts, prohibited content, quality failure, counter ambiguity, performance breach, and incomplete provider qualification.

## Expected Results
- Each automated result asserts observable status/reason code, persisted or restored state, receipt presence/schema, visible CLI diagnostic, and forbidden side effects. Missing data is never reported as zero.
- Invalid attempts remain traceable but excluded; valid negative/extreme observations remain in aggregation. A failing hard gate prevents downstream token access and rollout decisions.

## Layer Mapping
- Order: (1) unit/property policy, identity, statistics, redaction; (2) CLI/storage and lifecycle; (3) provider contracts; (4) integration/concurrency/recovery; (5) frozen-fixture E2E; (6) performance/privacy; (7) live eligibility and qualification; (8) UAT/report governance.
- TC-001–004 map to layers 1–3; TC-005–012 to 2–4; TC-013–016 to 5; TC-017–020 to 3/7; TC-021–022 to 6; TC-023–024 to 8.

## Automation Plan
- Implement deterministic cases under `tests/unit/`, `tests/cli/`, `tests/storage/`, `tests/providers/`, `tests/integration/`, `tests/e2e/`, and `tests/performance/`; run fast gates with `python -m pytest tests/unit tests/cli tests/storage tests/providers tests/integration`.
- Run frozen E2E with `python -m pytest tests/e2e`; performance with `python -m pytest tests/performance`; live qualification through a provider-version-bound local manifest. UAT records reviewer, manifest fingerprint, result, and evidence references.
