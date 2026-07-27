---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "release-slicing.md"
  path: "specs-refiniment/003-context-guard-product-goal/release-slicing.md"
  workspace: "refinement"
  skill: "ai-sdlc-release-slicing-and-backlog-readiness-review"
  flow_mode: "full"
  state_file: "specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "BR-101"
    - "BR-112"
    - "BR-201"
    - "BR-212"
    - "CAP-001"
    - "CAP-009"
    - "DEC-001"
    - "DEC-002"
    - "DEC-006"
    - "DEC-007"
    - "DEC-008"
    - "DEC-009"
    - "DEC-012"
    - "DEC-014"
    - "DEC-015"
    - "DEC-016"
    - "DEC-017"
    - "DEC-018"
    - "DEC-019"
    - "DEC-024"
    - "DEC-025"
    - "GOAL-001"
    - "GOAL-004"
  related_artifacts:
    - "specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md"
    - "specs-refiniment/003-context-guard-product-goal/backlog.md"
    - "specs-refiniment/003-context-guard-product-goal/business-context.md"
    - "specs-refiniment/003-context-guard-product-goal/change-impact.md"
    - "specs-refiniment/003-context-guard-product-goal/decision-log.md"
    - "specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md"
    - "specs-refiniment/003-context-guard-product-goal/discovery.md"
    - "specs-refiniment/003-context-guard-product-goal/goal-capability-map.md"
    - "specs-refiniment/003-context-guard-product-goal/prfaq.md"
    - "specs-refiniment/003-context-guard-product-goal/qa-strategy.md"
    - "specs-refiniment/003-context-guard-product-goal/qa.md"
    - "specs-refiniment/003-context-guard-product-goal/requirements-readiness.md"
    - "specs-refiniment/003-context-guard-product-goal/research.md"
    - "specs-refiniment/003-context-guard-product-goal/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-release-slicing-and-backlog-readiness-review"
    - "release-slicing"
    - "review"
---

# release-slicing.md

## Feature Summary
- Context Guard is a local MVP for developers actively using Claude Code and Codex. It aims to reduce avoidable provider-reported cache tokens before productive work while preserving complete required and safety-critical instructions, local evidence, and developer control.
- The accepted backlog contains 6 epics, 12 feature outcomes, 24 MVP stories, 48 acceptance criteria, 48 scenarios, and 18 cross-functional tasks. This artifact converts that scope into qualification slices; it does not claim implementation or savings evidence.
- DEC-019 fixes the delivery shape: shared foundation, Claude vertical, quality runner, Claude feasibility, Codex vertical and feasibility, then the combined decision gate. DEC-024 closes the remaining policy-contract exception.
- Planning verdict: **Ready with assumptions**, 8.5/10. The backlog is coherent enough for delivery specification and team sizing, but not for implementation commitment or an effectiveness claim until architecture, estimates, and EVID-401 evidence exist.

## Actors and Stakeholders
- Developer: primary user; starts guarded sessions, invokes skills, inspects receipts, bypasses optimization, and restores full-load behavior.
- Repository maintainer: owns versioned repository relevance rules within DEC-024 and cannot rewrite authoritative skills or weaken safety requirements.
- Product and Delivery: own value, scope, slice progression, provider decisions, and bounded claims.
- Engineering: owns policy, provider adapters, profile coordination, receipts, measurement adapters, instrumentation, and recovery.
- QA: owns frozen fixtures, hard gates, invalidation, paired evidence, and qualification signoff. Security/Privacy co-owns receipt threat review and forbidden-content proof.
- Claude Code and Codex are external, versioned host boundaries. Enterprise administration, centralized monitoring, and unqualified IDE/desktop surfaces are outside the customer MVP.

## Scope and Boundaries
- **Customer MVP:** independently qualified Claude Code and Codex guarded startup for supported surfaces, local evidence and recovery, quality-first paired measurement, net-value gates, and explicit per-provider plus combined rollout decisions.
- **Internal qualification slices:** Claude-only and Codex-only results may advance learning but are not the customer-facing combined MVP.
- **Must-have:** S-101 through S-604 and T-001 through T-016 plus T-018 where needed for claim bounds. Every accepted story remains MVP because each maps to a safety, quality, privacy, measurement, recovery, or rollout gate.
- **Post-MVP unless separately qualified:** T-017 Codex IDE/desktop parity; Claude plugin optimization; repository-local Codex filtering; additional repositories; enterprise administration; centralized telemetry.
- **Excluded:** semantic/model relevance classification, skill rewriting or summarization, a compact skill index as the customer solution, mid-session interception, pooled provider metrics, billed-cost claims, and remote raw-content collection.
- No sprint dates, capacity, or effort values are invented. Release slices are logical evidence milestones, not calendar commitments.

## Workflows and Failure Paths
- Normal sequence: preflight -> authoritative inventory -> DEC-024 policy validation -> deterministic classification -> supported provider profile -> actual-state verification -> fresh session -> frozen task -> hard quality gates -> provider measurement -> sanitized receipt -> restoration -> bounded decision.
- Baseline and guarded attempts use the same frozen task, model, repository fingerprint, provider version, and quality oracles. Five valid alternating warm-cache pairs are required per fixture/provider.
- Unsupported, ambiguous, stale, conflicting, duplicate, unmeasurable, or unverifiable states fall back to full load and receive no savings credit.
- Contention, abandoned state, and user edits use the DEC-017 lease, liveness, compare-and-swap, idempotent restoration, and one-action recovery rules.
- Any instruction loss, task failure, privacy leak, receipt failure, counter/correlation drift, recovery failure, or net-value breach invalidates the affected evidence. Invalid and negative attempts remain visible; no outlier is silently removed.
- A provider may fail qualification without blocking honest completion of its evidence package; it does block that provider's rollout and the combined MVP claim.

## Requirements and Business Rules
- BR-101 through BR-112 and BR-201 through BR-212 remain authoritative. Only exact, explicit `irrelevant` may reduce visibility; safety-critical, required, explicit invocation, conflict, or uncertainty retains complete authoritative content.
- DEC-024 governs version-2 layered YAML policy, exact identity, rule-id replacement/disable semantics, diagnostics, v1 compatibility, future-version rejection, and explicit atomic migration.
- Quality precedes token evaluation. QG-301 through QG-309 are hard gates with zero accepted bypass.
- Claude measures deduplicated cache-creation plus cache-read tokens. Codex measures exact cached-input events or a validated cumulative delta; missing boundaries are unmeasurable, not zero.
- Provider pass requires median reduction >=30%, nearest-rank Q1 >=0%, every fixture median >=0%, five valid pairs for each of three fixtures, and all quality/privacy/recovery requirements.
- The combined MVP may pass only if both providers independently qualify. One provider's result never offsets the other.

## Data, Integrations, and Non-Functional Requirements
- Receipts are local and unsynchronized by default in an application-owned location with user-only access equivalent to 0700 directories and 0600 files, atomic per-run writes, schema/version validation, 30-day retention, inspect/delete operations, completed-unreferenced pruning, corruption quarantine, and single-writer behavior.
- Allowed evidence includes provider/client versions, run/pair IDs, fingerprints/digests, stable identities, reason codes, classifications, requested/actual actions, fallback reasons, quality/measurement references, and timestamps. Raw prompts, responses, source, credentials, secrets, and full skill bodies are prohibited.
- Provider integrations are version/capability gated and must verify actual state before model work. Claude MVP is non-plugin startup `skillOverrides`; Codex MVP is CLI absolute-path `skills.config` and qualified app-server user-level state before `thread/start`.
- Added local overhead must have p95 <=750 ms and no qualifying run above 2 seconds, excluding provider network/model time. Happy path adds zero prompts; unsafe recovery permits at most one actionable prompt.
- Qualification tooling requires Python 3.10+. All reports remain provider-, version-, repository-, model-, and fixture-bounded.

## Dependencies, Risks, and Constraints
| Dependency ID | Backlog Item | Depends On | Dependency Type | Owner | Needed By | Risk If Delayed | Mitigation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEP-R01 | S-103/T-001 policy engine | DEC-024 and S-102 inventory identity | Hard contract | Engineering + QA | Slice 1 | Unsafe or non-reproducible omission | Implement validation and migration tests first |
| DEP-R02 | S-201/S-202 Claude vertical | S-104; S-301/S-302; T-002 | Hard technical | Engineering | Slice 2 | No safe Claude experiment | Full-load fallback; version pin |
| DEP-R03 | S-401 through S-404 quality runner | A working provider vertical; receipt foundation; T-007/T-008 | Hard evidence | QA + Engineering | Slice 3 | Savings evaluated without quality proof | Keep token access gated |
| DEP-R04 | S-501/S-502 measurement | S-403; provider adapter; correlation receipts | Hard evidence | QA + Engineering | Slices 4/5 | Misattributed or unmeasurable counters | Versioned adapters; invalidate ambiguity |
| DEP-R05 | S-603/S-604 rollout | Both provider packages; S-602; CONS-401 | Hard governance | Product + Delivery | Slice 6 | Unsupported combined claim | Per-provider decisions; cleanup gate |

- Primary risks are provider drift, required-instruction loss, profile corruption, receipt leakage, measurement misattribution, benchmark variance, local overhead erasing value, and one-repository overclaim.
- EVID-401 is planned implementation and qualification work, not evidence already obtained. CONS-401 is a required authority cleanup before S-603. There are no unresolved product-contract blockers after DEC-024.

## Decisions, Assumptions, and Open Questions
- Accepted authority: DEC-002 through DEC-006, DEC-009 through DEC-014, and DEC-016 through DEC-025. DEC-001, DEC-007, DEC-008, and DEC-015 are superseded.
- **Accepted DEC-025:** adopt the six-slice allocation and 8.5/10 Ready-with-assumptions verdict in this artifact, keep all 24 stories in the customer MVP, and treat T-017 as post-MVP unless qualification makes it necessary.
- Assumption A-R01: role owners shown in the accepted backlog are the planning owners; named assignees and team capacity are not provided. Owner: Delivery + Engineering. Impact: no calendar commitment can be made. Resolution/next step: assign people and capacity during team estimation.
- Assumption A-R02: slice ordering is evidence-driven and may overlap only where the dependency tables explicitly permit; it is not a promise of sequential calendar phases.
- Open planning input OQ-R01: team sizing, capacity, and target dates are not provided. Owner: Delivery + Engineering. Impact: roadmap dates cannot be committed. Resolution/next step: size after delivery specification and architecture boundaries are reviewed.
- Open qualification input OQ-R02: live Claude/Codex adapter behavior, counter eligibility, variance, and the causal contribution of skills require execution evidence. Owner: Engineering + QA + Product. Impact: rollout result may be pass, revise, or reject. Resolution/next step: execute Slices 2 through 5.
- Open compatibility input OQ-R03: Codex IDE/desktop parity. Owner: Engineering. Impact: post-MVP surface only. Resolution/next step: run T-017 after the Codex CLI vertical.

## Success Measures
- **Planning completeness:** 24/24 stories have actor, value, priority, MVP status, dependency, two acceptance criteria, and primary plus adverse scenario coverage.
- **Foundation exit:** deterministic replay, accepted policy behavior, safe fallback, privacy-safe atomic receipts, lifecycle controls, and no mutation on unsupported state.
- **Provider qualification:** five valid baseline/guarded pairs for each of three frozen fixtures; zero hard failures; median >=30%, Q1 >=0%, every fixture median >=0%; negative valid results retained.
- **Recovery/privacy:** bypass, contention, crash recovery, CAS protection, retention, quarantine, inspect/delete, and forbidden-content tests pass.
- **Net value:** local p95 <=750 ms, maximum <=2 seconds, zero happy-path prompts, and at most one unsafe-recovery prompt.
- **Claim control:** every decision is provider-specific and evidence-bounded; combined MVP only when both providers independently pass. This planning stage claims none of these outcomes as achieved.

## Source Coverage
- `specs-refiniment/003-context-guard-product-goal/backlog.md`: 6 epics, 12 features, 24 stories, 18 tasks, Definition of Ready, and DEC-019 priority labels.
- `specs-refiniment/003-context-guard-product-goal/user-stories.md`: story detail, 48 acceptance criteria, 48 scenarios, dependencies, and readiness after DEC-024.
- `specs-refiniment/003-context-guard-product-goal/goal-capability-map.md`: GOAL-001 through GOAL-004, CAP-001 through CAP-009, actor ownership, and outcome traceability.
- `specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md`: verified zero planning blockers, EVID-401 delivery work, and CONS-401 cleanup.
- `specs-refiniment/003-context-guard-product-goal/decision-log.md`: accepted and superseded authority through DEC-024.
- `specs-refiniment/003-context-guard-product-goal/discovery.md`, `specs-refiniment/003-context-guard-product-goal/prfaq.md`, `specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md`, and `specs-refiniment/003-context-guard-product-goal/requirements-readiness.md`: customer, promise, boundaries, launch posture, and historical gate evolution.
- `specs-refiniment/003-context-guard-product-goal/business-context.md` and `specs-refiniment/003-context-guard-product-goal/research.md`: workflow, permissions, provider surfaces, version limits, and remaining compatibility questions.
- `specs-refiniment/003-context-guard-product-goal/qa.md` and `specs-refiniment/003-context-guard-product-goal/qa-strategy.md`: fixtures, hard gates, invalidation, measurement windows, pairing, aggregation, privacy, and recovery expectations.
- `specs-refiniment/003-context-guard-product-goal/change-impact.md`: strict DEC-024/POL-401/S-103 owner impact and refreshed downstream sources.
- `specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon` and refinement indexes: lifecycle and routing evidence. The full-flow 24,000-token context pack and its deferred source ranges were reviewed before synthesis.

## MVP Slice
- The customer MVP is the union of Slices 1 through 6. It is not releasable after a single provider pilot.
- **Must-have:** S-101 through S-604; T-001 through T-016; T-018 for causal bounds and claim review. These items establish relevance safety, provider control, local evidence, quality, measurement, net value, and governance.
- **Should-have within qualification if cheap:** reusable adapter fixtures and automation beyond the minimum accepted scenarios; these must not delay hard-gate evidence.
- **Post-MVP:** T-017 Codex IDE/desktop parity, broader repositories, Claude plugins, repository-local Codex controls, enterprise policy, centralized operations, and generalized/public savings claims.
- Manual operation may orchestrate the first pilot, but no manual workaround may replace policy validation, actual-state verification, hard quality gates, privacy scanning, recovery proof, or reproducible counter extraction.

## Release Slice Matrix
| Slice | Value | Stories | Dependencies | Exit Criteria | Risks |
| --- | --- | --- | --- | --- | --- |
| Slice 1 — Trusted foundation | Safe, reproducible relevance plus local evidence | S-101–S-104; S-301–S-304; T-001; T-005; T-006; adapter-contract foundations in T-002/T-003 | DEC-009; DEC-012; DEC-016; DEC-024 | Supported/unsupported preflight, stable inventory, v2 policy validation/migration, deterministic classifications, atomic privacy-safe receipts, inspect/delete/retention/quarantine tests pass | Policy errors; identity drift; receipt leakage |
| Slice 2 — Claude guarded vertical | First end-to-end supported control and recovery path | S-201; S-202; T-002; Claude portion of T-004 | Slice 1; DEC-017 | Requested/actual state verified before fresh session; bypass, fallback, CAS restore, contention, and crash recovery pass on version-pinned Claude fixtures | Host drift; configuration loss |
| Slice 3 — Quality gate runner | Prevent token savings from masking regressions | S-401–S-404; T-007; T-008; quality portion of T-016 | Slice 1; one provider vertical | Three frozen fixtures, machine oracles, QG-301–QG-309 enforcement, invalidation, retention, and replay pass; token access remains gated until quality passes | Nondeterminism; false oracle equivalence |
| Slice 4 — Claude feasibility | Determine whether Claude can meet the target honestly | S-501; Claude portions of S-503/S-504; T-009; T-011; relevant T-018 | Slices 2 and 3 | Five valid pairs x three fixtures; deduplicated Claude window; provider-separated statistics and causal bounds; explicit pass/revise/reject result | Duplicate events; variance; target miss |
| Slice 5 — Codex vertical and feasibility | Qualify the second required provider | S-203; S-204; S-502; Codex portions of S-503/S-504; T-003; Codex portion of T-004; T-010; T-011; relevant T-018 | Slices 1 and 3; lessons from Slice 4 | Verified CLI/qualified app-server state, safe recovery, five valid pairs x three fixtures, valid Codex event/delta window, explicit provider result | App-server drift; missing event boundary; user edits |
| Slice 6 — Net value and combined decision | Produce a defensible customer-MVP outcome | S-601–S-604; T-012–T-016; remaining T-018 | Both provider evidence packages; CONS-401 | DEC-018 performance/prompt gates, end-to-end qualification matrix, bounded evidence package, explicit per-provider decisions, and combined decision only if both pass | Overclaim; stale authority; overhead erases benefit |

## Sequencing and Dependencies
| Sequence | Backlog Item ID | Item Summary | Reason for Position | Can Run in Parallel? | Blocks | Blocked By |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | S-101–S-104; S-301–S-304 | Relevance and receipt foundation | Unlocks every safe provider experiment and audit path | Receipt work can parallel policy work after identity contract | All provider verticals and evidence | Accepted contracts only |
| 2 | S-201/S-202 | Claude control and recovery | Earlier provider learning per DEC-019 | Limited T-007 fixture preparation may parallel | Claude quality and measurement | Sequence 1 |
| 3 | S-401–S-404 | Shared quality runner | Establishes non-negotiable gates before token evaluation | Adapter-neutral runner work may overlap late Slice 2 | S-501–S-504 | Sequence 1 and one provider vertical |
| 4 | S-501/S-503/S-504 | Claude measurement and decision | Tests feasibility early and informs Codex execution | Codex adapter contract work may parallel | Cross-provider lessons and final package | Sequences 2 and 3 |
| 5 | S-203/S-204/S-502/S-503/S-504 | Codex control, recovery, and measurement | Completes the second required provider without hiding its distinct risks | Some net-value instrumentation may parallel after stable verticals | Combined MVP decision | Sequences 1 and 3; reusable lessons from 4 |
| 6 | S-601–S-604 | Net-value, evidence, and rollout governance | Requires complete provider packages and authority cleanup | Per-provider report assembly may parallel | Customer MVP release decision | Sequences 4 and 5; CONS-401 |

- T-017 follows the Codex CLI vertical and does not block the MVP unless Product explicitly expands the supported surface. No calendar dates are assigned until owners size the delivery specification.

## Milestones and Readiness
| Milestone | Objective | Key Backlog Items | Exit Criteria | Dependencies | Risks |
| --- | --- | --- | --- | --- | --- |
| M1 Foundation ready | Make guarded decisions safe and auditable | S-101–S-104; S-301–S-304 | All Slice 1 contract and negative-path tests pass | DEC-024 | False irrelevance; privacy defect |
| M2 Claude vertical ready | Prove supported mutation and recovery behavior | S-201/S-202 | Version-pinned control, verification, fallback, bypass, and restore pass | M1 | Provider drift |
| M3 Quality gate ready | Make correctness the entry condition for measurement | S-401–S-404 | Three fixtures and all hard gates execute reproducibly | M2 | Flaky fixtures |
| M4 Claude decision ready | Produce the first honest feasibility result | S-501/S-503/S-504 | Complete valid-pair ledger and bounded Claude decision | M3 | Variance or target miss |
| M5 Codex decision ready | Produce the second independent result | S-203/S-204/S-502/S-503/S-504 | Safe Codex vertical and bounded Codex decision | M1; M3 | Unmeasurable counters |
| M6 MVP decision ready | Decide net value and combined release | S-601–S-604 | Performance, privacy, recovery, evidence, CONS-401, and governance gates pass | M4; M5 | Overclaim |

- **Definition of Ready:** 24/24 stories are ready for delivery specification and team estimation. Implementation start additionally requires architecture/interface decisions, engineering sizing, named assignees, environment access, and test-data/fixture readiness.
- **Definition of Done:** code and contract tests pass; negative/failure paths pass; actual provider state is verified; sanitized receipts and replay evidence exist; hard quality/privacy/recovery gates pass; documentation and authority are current; no claim exceeds evidence.
- **Estimation readiness:** 8.5/10. Story intent, acceptance, dependencies, and owners are strong. Effort, capacity, architecture boundaries, and live-provider uncertainty remain. Use spikes/evidence tasks inside the slices rather than hiding uncertainty in estimates.

## Release Risks
| Risk ID | Risk | Category | Related Backlog Items | Likelihood | Impact | Mitigation | Owner | Early Warning Signal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RR-001 | Provider surface or schema drifts | External dependency | S-101; S-201; S-203; S-501; S-502 | High | High | Version/capability preflight, contract fixtures, full-load/unmeasurable result | Engineering | Actual state or event schema differs from pinned fixture |
| RR-002 | Required or safety instruction is omitted | Safety/quality | S-104; S-201; S-203; S-402/S-403 | Medium | Critical | Exact identity, precedence, complete-content oracle, zero hard-failure tolerance | Engineering + QA | Instruction digest/oracle mismatch |
| RR-003 | Guarded profile corrupts user configuration | Recovery | S-202; S-204 | Medium | Critical | Lease, snapshot/digest, CAS, liveness, idempotent restore, preserve user edits | Engineering | Restore digest mismatch or second writer |
| RR-004 | Receipt exposes prohibited content | Privacy | S-301–S-304 | Medium | Critical | Field allowlist, forbidden-content fixtures, permissions, atomic writes, quarantine | Security/Privacy + QA | Forbidden field/value detected |
| RR-005 | Counter window is wrong or uncorrelated | Measurement | S-501/S-502 | High | High | Versioned adapters, dedupe/delta validation, unmeasurable rather than inference | QA + Engineering | Duplicate, missing, or non-monotonic event |
| RR-006 | Variance or causal ambiguity overstates savings | Evidence | S-503/S-504; T-018 | High | High | Alternating valid pairs, no outlier deletion, quartile/fixture gates, causal bounds | Product + QA | Wide distribution or negative fixture median |
| RR-007 | Local overhead or prompts erase value | Product value | S-601/S-602 | Medium | High | Separate instrumentation and DEC-018 hard gate | Product + Engineering | p95 >750 ms, max >2 s, or prompt added |
| RR-008 | One provider or one repository is generalized | Governance | S-603/S-604 | Medium | High | Provider-separated decisions, bounded labels, CONS-401, combined two-provider gate | Product + Delivery | Report language drops provider/version/repository qualifiers |

## Release Verdict
- **Verdict: Ready with assumptions (8.5/10) for delivery specification, architecture refinement, and team estimation.**
- Top reason 1: the accepted 24-story MVP has complete actor/value/priority/dependency coverage plus 48 testable acceptance criteria and 48 primary/adverse scenarios.
- Top reason 2: DEC-019 gives a coherent dependency and learning sequence, DEC-024 closes the last story-definition exception, and accepted DEC-025 authorizes the release plan.
- Top reason 3: privacy, quality, recovery, provider measurement, performance, and claim controls are explicit gates rather than implied work.
- This is **not** implementation readiness, release approval, or proof of 30% savings. EVID-401 must be generated by Slices 2–6; CONS-401 must close before S-603; estimates, capacity, target dates, and architecture remain downstream work.
- Required next action: proceed to the full-flow business-analysis/context stage, then delivery specification and engineering sizing.
- Optional next action: Engineering may prepare T-017 after the Codex CLI vertical; it does not block the accepted customer MVP.
