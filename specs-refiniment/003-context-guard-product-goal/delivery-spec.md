---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "delivery-spec.md"
  path: "specs-refiniment/003-context-guard-product-goal/delivery-spec.md"
  workspace: "refinement"
  skill: "ai-sdlc-delivery-spec-synthesis"
  flow_mode: "full"
  state_file: "specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-301"
    - "AC-302"
    - "AC-303"
    - "AC-304"
    - "AC-305"
    - "AC-306"
    - "AC-307"
    - "AC-308"
    - "AC-309"
    - "AC-310"
    - "AC-311"
    - "AC-312"
    - "AC-313"
    - "AC-314"
    - "AC-315"
    - "AC-316"
    - "BR-101"
    - "BR-102"
    - "BR-103"
    - "BR-104"
    - "BR-105"
    - "BR-106"
    - "BR-107"
    - "BR-108"
    - "BR-109"
    - "BR-110"
    - "BR-111"
    - "BR-112"
    - "BR-201"
    - "BR-202"
    - "BR-203"
    - "BR-204"
    - "BR-205"
    - "BR-206"
    - "BR-207"
    - "BR-208"
    - "BR-209"
    - "BR-210"
    - "BR-211"
    - "BR-212"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-006"
    - "DEC-007"
    - "DEC-008"
    - "DEC-009"
    - "DEC-010"
    - "DEC-011"
    - "DEC-012"
    - "DEC-014"
    - "DEC-015"
    - "DEC-016"
    - "DEC-017"
    - "DEC-018"
    - "DEC-024"
    - "DEC-025"
    - "DEC-026"
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "EPIC-004"
    - "EPIC-005"
    - "EPIC-006"
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
    - "specs-refiniment/003-context-guard-product-goal/release-slicing.md"
    - "specs-refiniment/003-context-guard-product-goal/requirements-readiness.md"
    - "specs-refiniment/003-context-guard-product-goal/research.md"
    - "specs-refiniment/003-context-guard-product-goal/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-delivery-spec-synthesis"
    - "delivery-spec"
    - "review"
---

# delivery-spec.md

## Feature Summary
- Context Guard is a local MVP for developers using Claude Code and Codex. Its delivery goal is to reduce avoidable provider-reported cache tokens before productive work while preserving complete required/safety instructions, local evidence, privacy, recovery, and developer control.
- The accepted package contains 4 goals, 9 capabilities, 6 epics, 12 feature outcomes, 24 MVP stories, 48 story acceptance criteria, 48 scenarios, 18 cross-functional tasks, and 6 evidence-driven release slices.
- This delivery specification turns those accepted outcomes into 12 delivery requirement clusters, 9 end-to-end workflows, and complete story/acceptance traceability.
- Current status is planning only: policy, adapters, receipts, runner, pilots, and qualification evidence are not claimed as implemented.
- Audience: Engineering, QA, Security/Privacy, Product, Delivery, and BA preparing architecture, sizing, test design, and implementation handoff.

## Actors and Stakeholders
- Developer initiates guarded work, explicitly invokes skills, inspects/deletes local receipts, bypasses optimization, and restores baseline behavior.
- Repository maintainer authors and validates repository relevance rules under DEC-024.
- Engineering implements deterministic policy/inventory behavior, provider controls, state coordination, receipts, measurement adapters, instrumentation, and recovery.
- QA owns frozen fixtures, oracles, hard gates, invalidation, paired evidence, and qualification signoff. Security/Privacy owns receipt threat review and prohibited-content proof.
- Product owns the 30% target, net-value interpretation, provider decisions, and claim language. Delivery owns slice progression, evidence-package readiness, and combined rollout governance.
- Claude Code and Codex are external versioned hosts. Their supported controls, actual state, and usage events are authoritative integration boundaries.

## Scope and Boundaries
- In scope: provider/version/surface preflight; authoritative inventory/fingerprints; layered policy v2; deterministic relevance; supported startup profile request and actual-state verification; fresh sessions; fallback/bypass/rollback; local receipt lifecycle; quality runner; provider-specific measurement; net-value gate; evidence package; per-provider and combined decisions.
- Claude delivery boundary: version-qualified non-plugin startup `skillOverrides`, with `user-invocable-only` only for exact irrelevant outcomes.
- Codex delivery boundary: version-qualified CLI absolute-path `skills.config` and qualified app-server user-level state before `thread/start`, followed by restoration.
- Customer MVP requires both providers to qualify independently. A one-provider pilot is an internal evidence slice, not a customer release.
- Out of scope: semantic/model relevance classification, skill rewriting/summarization, compact skill index as product, mid-session interception, Claude plugins, repository-local Codex filtering, unqualified IDE/desktop behavior, enterprise administration, centralized telemetry, billed-cost claims, and universal effectiveness claims.
- Architecture, API shape, package layout, concrete storage technology, estimates, capacity, and dates are deliberately deferred to architecture/SDD and team planning.

## Workflows and Failure Paths
- Delivery path: preflight -> inventory -> policy validation -> classification -> lease/snapshot -> supported provider action -> actual-state verification -> fresh session -> task/fixture -> quality/privacy/recovery gates -> provider measurement -> receipt -> restore -> bounded decision.
- Baseline and guarded attempts must share provider/model/version, declared task, repository fingerprint, fixture manifest, and quality oracles.
- Unsupported, stale, duplicate, conflicting, ambiguous, uncorrelated, or unmeasurable inputs use full load or invalidate evidence; zero is never substituted for missing provider data.
- Contention does not wait or mutate: it uses full load. Abandoned state requires ownership/liveness evidence. Restoration is idempotent compare-and-swap and preserves user edits.
- Quality, instruction, privacy, receipt, correlation, recovery, or performance failure prevents savings evaluation/claim for the affected evidence.
- Invalid attempts remain with reason codes and are excluded; valid negative/extreme results remain in aggregation; providers are never pooled.

## Requirements and Business Rules
- DSR-101 through DSR-602 are the delivery-level requirement clusters and map every MVP story to an actor, acceptance set, dependency, and release slice.
- BR-101 through BR-112 define product, comparison, privacy, reversibility, and claim constraints. BR-201 through BR-212 define authoritative identity, inputs, precedence, lifetime, actions, fallback, and receipts.
- DEC-024 is the policy contract: version-2 layered YAML, exact identity for irrelevance, whole same-ID replacement, disable semantics, validation diagnostics, compatibility, and explicit atomic migration.
- Only exact explicit `irrelevant` may reduce visibility. Required, safety-critical, explicit invocation, conflict, and uncertainty retain complete authoritative content.
- Actual state must match requested state before model work. Quality gates must pass before token evaluation. Net-value limits cannot be overridden by savings.
- Combined MVP status may pass only when both providers independently satisfy every quality, privacy, recovery, measurement, statistical, and performance gate.

## Data, Integrations, and Non-Functional Requirements
- **Provider adapter capability contract:** preflight version/surface; read authoritative inventory/state; request supported startup action; verify actual state; start or coordinate a fresh session boundary; restore safely; expose or correlate provider-native usage evidence. Concrete APIs remain an architecture decision.
- **Policy operator contract:** `init` never overwrites; `validate` returns nonzero and identifies file/dotted field/stable code/remediation; `doctor` reports effective sources/version/conflicts without raw content; explicit migration validates, backs up, and atomically replaces.
- **Receipt operator contract:** atomic per-attempt write; inspect targeted sanitized evidence; explicitly delete a target; retain 30 days by default; prune completed unreferenced records only; single-writer locking; quarantine corrupt data.
- Allowed receipt data includes schema/version, run/pair IDs, timestamps, provider/client/model versions, task/repository/policy/inventory fingerprints, identities/digests, reason codes, classification, requested/actual actions, fallback, quality/measurement refs, and restoration status.
- Prohibited data includes prompts, responses, source, credentials, secrets, environment values, and full skill bodies.
- Claude uses deduplicated cache-creation plus cache-read tokens. Codex uses exact cached-input events or validated cumulative deltas. Results remain provider-specific.
- NFRs: deterministic replay; full-load fail safety; provider isolation; local-only core operation; access equivalent to 0700 directories/0600 files; atomicity; non-destructive recovery; Python 3.10+ qualification; local p95 <=750 ms, maximum <=2 seconds, zero happy-path prompts, at most one unsafe-recovery prompt.

## Dependencies, Risks, and Constraints
- Accepted order: Slice 1 relevance/receipt foundation; Slice 2 Claude guarded vertical; Slice 3 shared quality runner; Slice 4 Claude feasibility; Slice 5 Codex vertical/feasibility; Slice 6 net-value and combined decision.
- Hard dependencies: DSR-102 needs authoritative inventory; provider verticals need relevance plus receipt foundation; measurement needs provider vertical plus quality gate; rollout needs both provider packages plus net-value and CONS-401.
- EVID-401 represents build and qualification outputs and remains unfulfilled until executed. CONS-401 reconciles stale historical authority before evidence handoff.
- Major risks: provider drift, required-instruction loss, profile corruption, receipt leakage, counter misattribution, benchmark variance, causal overclaim, negative net value, and overgeneralization.
- Required controls: capability/version gates, exact identity, conservative precedence, actual-state verification, full load, lease/snapshot/CAS, minimized receipts, hard quality gates, correlated alternating pairs, no outlier deletion, provider-separated reporting, and bounded claims.
- Engineering capacity, named assignees, estimates, and dates are not provided. Owner: Delivery + Engineering. Impact: no delivery schedule can be committed. Resolution/next step: architecture review and team estimation after this spec is approved.

## Decisions, Assumptions, and Open Questions
- Accepted authority: DEC-002 through DEC-006, DEC-009 through DEC-014, and DEC-016 through DEC-026. DEC-001, DEC-007, DEC-008, and DEC-015 are superseded.
- **Accepted DEC-026:** DSR-101 through DSR-602, WF-DS01 through WF-DS09, and the traceability/gate model in this delivery spec are the cross-functional implementation-planning baseline; architecture, estimates, and live qualification remain downstream evidence.
- Assumption DS-A01: role ownership is sufficient for handoff until Delivery assigns named people. Owner: Delivery. Impact: work is attributable by discipline but not person. Resolution/next step: assign during estimation.
- Execution question DS-OQ01: pinned provider controls and usage schemas must still pass preflight at implementation time. Owner: Engineering + QA. Impact: affected surface may be full-load/unmeasurable. Resolution/next step: contract-test in Slices 2, 4, and 5.
- Architecture question DS-OQ02: package boundaries, internal APIs, concurrency primitive, and concrete receipt store are not selected. Owner: Engineering. Impact: sizing cannot be final. Resolution/next step: architecture workflow followed by SDD; choices must satisfy this spec.
- Evidence question DS-OQ03: causal skill contribution and 30% outcome require live pairs. Owner: Product + Engineering + QA. Impact: rollout may pass, revise, or reject. Resolution/next step: T-018 and DSR-501/DSR-502.
- Compatibility question DS-OQ04: Codex IDE/desktop parity remains post-MVP. Owner: Engineering. Impact: unqualified surfaces remain full-load/unclaimed. Resolution/next step: T-017 after Codex CLI vertical.

## Success Measures
- Provider effectiveness: five valid pairs for each of three fixtures/provider; median reduction >=30%, nearest-rank Q1 >=0%, every fixture median >=0%; providers separate.
- Quality: zero hard failures, complete required/safety instruction preservation, explicit skill-invocation oracle, and no token access until QG-301 through QG-309 pass.
- Safety/control: unsupported/ambiguous/mismatched state uses full load; bypass, contention fallback, crash recovery, CAS restoration, and user-edit preservation pass.
- Privacy/evidence: atomic schema-valid receipts reproduce decisions and measurements without prohibited content; inspect/delete/retention/pruning/quarantine behave as specified.
- Net value: local p95 <=750 ms, no qualifying run >2 seconds, zero happy-path prompts, at most one unsafe-recovery prompt.
- Governance: every provider decision includes versions, repository, model, fixtures, failures, statistics, causal bounds, privacy/quality/recovery/performance results; combined MVP only when both providers qualify.

## Source Coverage
- `specs-refiniment/003-context-guard-product-goal/business-context.md`: full actors, current/desired behavior, 9 workflows, 24 business rules, and 16 end-to-end ACs.
- `specs-refiniment/003-context-guard-product-goal/user-stories.md`: 24 stories, 48 story ACs, 48 scenarios, dependencies, and readiness.
- `specs-refiniment/003-context-guard-product-goal/backlog.md`: feature/story/task decomposition and Definition of Ready.
- `specs-refiniment/003-context-guard-product-goal/release-slicing.md`: accepted six-slice plan and readiness verdict.
- `specs-refiniment/003-context-guard-product-goal/goal-capability-map.md`: goals, capabilities, epics, roles, and outcome links.
- `specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md`: zero current planning blockers, EVID-401, and CONS-401.
- `specs-refiniment/003-context-guard-product-goal/decision-log.md`: authority and supersession through DEC-025.
- `specs-refiniment/003-context-guard-product-goal/qa.md`: fixtures, hard gates, invalidation, and regression scope.
- `specs-refiniment/003-context-guard-product-goal/qa-strategy.md`: adapters, pairing, measurement, aggregation, privacy replay, and evidence constraints.
- `specs-refiniment/003-context-guard-product-goal/research.md`: provider surfaces, version evidence, limitations, and compatibility questions.
- `specs-refiniment/003-context-guard-product-goal/prfaq.md` and `specs-refiniment/003-context-guard-product-goal/discovery.md`: customer, value, MVP, business requirements, launch posture, and risks.
- `specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md` and `specs-refiniment/003-context-guard-product-goal/requirements-readiness.md`: historical gaps and gate evolution.
- `specs-refiniment/003-context-guard-product-goal/change-impact.md`: DEC-024/POL-401/S-103 owner-impact evidence.
- `specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon`: lifecycle authority. The full-flow context pack and deferred evidence ranges were reviewed before synthesis.

## Requirement Detail
| Requirement ID | Actor/System | Requirement | Source | Priority | Acceptance Ref |
| --- | --- | --- | --- | --- | --- |
| DSR-101 | Developer; provider adapter | Preflight provider/version/surface and produce stable authoritative skill identities/digests or explicit unsupported/uncertain result before mutation. | S-101; S-102; F-101 | P0 / Slice 1 | AC-S101-1/2; AC-S102-1/2 |
| DSR-102 | Maintainer; relevance engine | Validate DEC-024 policy v2 and deterministically classify every skill using DEC-009 precedence, exact identity, stable reason codes, and full content except exact irrelevant. | S-103; S-104; F-102 | P0 / Slice 1 | AC-S103-1/2; AC-S104-1/2 |
| DSR-201 | Developer; Claude adapter | Apply and verify a supported Claude non-plugin guarded profile before a fresh session; provide bypass, full-load fallback, lease-safe and CAS-safe restoration. | S-201; S-202; F-201 | P0 / Slice 2 | AC-S201-1/2; AC-S202-1/2 |
| DSR-202 | Developer; Codex adapter | Apply and verify supported Codex CLI/app-server pre-thread state; handle contention, abandoned state, user edits, fallback, and idempotent recovery. | S-203; S-204; F-202 | P0 / Slice 5 | AC-S203-1/2; AC-S204-1/2 |
| DSR-301 | QA; Security/Privacy; receipt service | Write one atomic schema-valid minimized receipt for every attempted decision/measurement and prove prohibited content is absent while replay remains possible. | S-301; S-302; F-301 | P0 / Slice 1 | AC-S301-1/2; AC-S302-1/2 |
| DSR-302 | Developer; receipt service | Support targeted inspect/delete, 30-day retention, safe completed-unreferenced pruning, single-writer behavior, and corruption quarantine. | S-303; S-304; F-302 | P0 / Slice 1 | AC-S303-1/2; AC-S304-1/2 |
| DSR-401 | QA; fixture runner | Execute three frozen provider-neutral fixtures in fresh correlated sessions and evaluate machine completion plus instruction-preservation oracles. | S-401; S-402; F-401 | P0 / Slice 3 | AC-S401-1/2; AC-S402-1/2 |
| DSR-402 | QA; evidence gate | Enforce QG-301 through QG-309 before token access; retain/explain invalid attempts and exclude them from aggregation without erasure. | S-403; S-404; F-402 | P0 / Slice 3 | AC-S403-1/2; AC-S404-1/2 |
| DSR-501 | QA; Claude metrics | Extract a deduplicated Claude cache window, run alternating warm-cache pairs, retain valid negatives, aggregate provider statistics/causal bounds, and decide against the 30% gate. | S-501; S-503; S-504 | P0 / Slice 4 | AC-S501-1/2; AC-S503-1/2; AC-S504-1/2 |
| DSR-502 | QA; Codex metrics | Extract exact Codex cached-input events or validated deltas, run the same paired/statistical protocol, and mark missing boundaries unmeasurable. | S-502; S-503; S-504 | P0 / Slice 5 | AC-S502-1/2; AC-S503-1/2; AC-S504-1/2 |
| DSR-601 | Engineering; Product | Measure local overhead/prompts separately from provider time and fail the affected claim/full-load gate on any DEC-018 breach. | S-601; S-602; F-601 | P0 / Slice 6 | AC-S601-1/2; AC-S602-1/2 |
| DSR-602 | Delivery; Product; QA | Assemble bounded replayable evidence, close CONS-401, decide each provider, and permit combined MVP only when both independently pass every gate. | S-603; S-604; F-602 | P0 gate / Slice 6 | AC-S603-1/2; AC-S604-1/2 |

## Workflow Detail
| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Requirement Ref |
| --- | --- | --- | --- | --- | --- | --- |
| WF-DS01 | Guarded startup requested | Developer; adapter | Preflight version/surface/capabilities; read inventory twice; fingerprint identities | Eligible or unsupported state recorded | Unsupported/ambiguous -> no mutation/full load | DSR-101 |
| WF-DS02 | Eligible inventory exists | Maintainer; relevance engine | Load effective policy; validate/migrate explicitly; classify with fixed precedence | Deterministic action plan/reasons | Invalid/conflict/stale -> uncertain/full content | DSR-102 |
| WF-DS03 | Action plan is eligible | Context Guard; provider adapter | Acquire lease; snapshot/digest; request action; verify actual state; start fresh session | Verified Claude or Codex guarded session | Contention/mismatch/user edit -> full load/no overwrite | DSR-201; DSR-202 |
| WF-DS04 | Attempt changes state or ends | Receipt service; developer | Persist minimized receipt atomically; inspect/delete/retain/prune/quarantine; restore with CAS | Auditable evidence and baseline state | Write/privacy/restore failure -> invalidate/disable | DSR-301; DSR-302; DSR-201; DSR-202 |
| WF-DS05 | Qualification begins | QA; runner | Freeze manifest; run baseline/guarded fresh sessions; correlate pair | Comparable attempt pair | Fingerprint/correlation mismatch -> invalid | DSR-401 |
| WF-DS06 | Pair outputs exist | QA | Run machine and instruction oracles; apply QG-301–QG-309 | Token access allowed or denied | Any failure -> retained invalid evidence | DSR-402 |
| WF-DS07 | Valid pair is measurable | QA; metrics adapter | Extract/dedupe/delta provider window; append immutable attempt ledger | Provider-native cache value | Drift/missing boundary -> unmeasurable | DSR-501; DSR-502 |
| WF-DS08 | Valid-pair target reached | QA; Product | Aggregate unrounded reductions, Q1, fixture/provider medians, causal bounds | Provider pass/revise/reject result | Statistical/quality miss -> no qualification | DSR-501; DSR-502 |
| WF-DS09 | Both provider packages available | Engineering; Product; Delivery; QA | Evaluate overhead/prompts; close consistency; assemble evidence; decide each provider and combined MVP | Bounded rollout decision | Any gate failure or one provider fail -> combined no-go | DSR-601; DSR-602 |

## Business Rule Detail
| Rule ID | Rule | Applies To | Source | Failure Behavior | Decision Ref |
| --- | --- | --- | --- | --- | --- |
| BR-101 | Guarded runs prevent only explicitly irrelevant full skill content at supported startup boundaries. | DSR-102/201/202 | prfaq.md | Full load/no credit | DEC-004; DEC-012 |
| BR-102 | Required and safety-critical instructions remain complete and authoritative. | All provider/quality paths | prfaq.md | Hard failure; invalidate/restore | DEC-004; DEC-010 |
| BR-103 | Uncertainty favors full inclusion and correctness. | Classification/control | prfaq.md | No omission/no credit | DEC-009 |
| BR-104 | Providers remain separately measured and decided. | DSR-501/502/602 | prfaq.md | Reject pooled result | DEC-003; DEC-011 |
| BR-105 | Pair validity requires equivalent declared inputs and quality. | DSR-401/402 | prfaq.md | Invalidate pair | DEC-010; DEC-011 |
| BR-106 | Evidence reports native tokens, not inferred billed cost. | DSR-501/502/602 | prfaq.md | Reject claim | DEC-003; DEC-006 |
| BR-107 | Receipts exclude prohibited raw content. | DSR-301/302 | prfaq.md | Invalidate/quarantine/review | DEC-016 |
| BR-108 | Skills/unrelated config stay unchanged and intervention is reversible. | DSR-201/202 | prfaq.md | Full load; release block on loss | DEC-017 |
| BR-109 | Compact skill index is not the product solution. | Scope/design | prfaq.md | Reject scope/design | DEC-004 |
| BR-110 | 30% claim needs named passing provider evidence. | DSR-501/502/602 | prfaq.md | No effectiveness claim | DEC-003; DEC-011 |
| BR-111 | Net-value breach cannot be offset by savings. | DSR-601 | backlog.md | Affected surface fails | DEC-018 |
| BR-112 | Combined MVP requires both providers independently pass. | DSR-602 | backlog.md | Combined revise/reject | DEC-006; DEC-025 |
| BR-201 | Identity uses provider/version/scope/name/canonical locator/metadata/body digests. | DSR-101 | business-context.md | Missing/duplicate/change -> uncertain | DEC-009 |
| BR-202 | Safety-critical wins and keeps complete content. | DSR-102 | business-context.md | Lower rule ignored/receipted | DEC-009 |
| BR-203 | Explicit or mandatory invocation is required unless safety-critical. | DSR-102 | business-context.md | Ambiguity -> uncertain | DEC-009 |
| BR-204 | Exact policy-required match is required unless higher precedence. | DSR-102 | business-context.md | Invalid/conflict -> uncertain | DEC-009; DEC-024 |
| BR-205 | Irrelevant needs exact positive match and no higher precedence. | DSR-102 | business-context.md | Absence never implies irrelevant | DEC-009; DEC-024 |
| BR-206 | Missing/stale/unsupported/conflicting/ambiguous evidence is uncertain. | DSR-101/102 | business-context.md | Full content/zero credit | DEC-009 |
| BR-207 | Fixed precedence resolves outcomes; equal conflict is uncertain. | DSR-102 | business-context.md | No omission | DEC-009 |
| BR-208 | Only irrelevant maps to reduction; failed actual state restores full load. | DSR-201/202 | business-context.md | Invalidate savings | DEC-009; DEC-012 |
| BR-209 | Snapshot is bound to provider/task/repository/policy/inventory/profile fingerprints. | DSR-102/201/202 | business-context.md | Change forces recompute | DEC-009 |
| BR-210 | Raw content, semantic judgment, and prior token totals are not classification inputs. | DSR-102 | business-context.md | Privacy/determinism failure | DEC-009 |
| BR-211 | Receipt includes accepted minimized evidence/action fields. | DSR-301 | business-context.md | Non-reproducible/unmeasurable | DEC-016 |
| BR-212 | Receipt lifecycle/content follows privacy and user-control limits. | DSR-301/302 | business-context.md | Invalidate/quarantine/restore | DEC-016 |

## User Story Traceability
| Requirement | Stories | Feature | Epic | Release Slice | Coverage |
| --- | --- | --- | --- | --- | --- |
| DSR-101 | S-101; S-102 | F-101 | EPIC-001 | Slice 1 | Complete |
| DSR-102 | S-103; S-104 | F-102 | EPIC-001 | Slice 1 | Complete |
| DSR-201 | S-201; S-202 | F-201 | EPIC-002 | Slice 2 | Complete |
| DSR-202 | S-203; S-204 | F-202 | EPIC-002 | Slice 5 | Complete |
| DSR-301 | S-301; S-302 | F-301 | EPIC-003 | Slice 1 | Complete |
| DSR-302 | S-303; S-304 | F-302 | EPIC-003 | Slice 1 | Complete |
| DSR-401 | S-401; S-402 | F-401 | EPIC-004 | Slice 3 | Complete |
| DSR-402 | S-403; S-404 | F-402 | EPIC-004 | Slice 3 | Complete |
| DSR-501 | S-501; S-503; S-504 | F-501; F-502 | EPIC-005 | Slice 4 | Complete |
| DSR-502 | S-502; S-503; S-504 | F-501; F-502 | EPIC-005 | Slice 5 | Complete |
| DSR-601 | S-601; S-602 | F-601 | EPIC-006 | Slice 6 | Complete |
| DSR-602 | S-603; S-604 | F-602 | EPIC-006 | Slice 6 | Complete |

- All 24 MVP stories are covered. S-503/S-504 intentionally apply to both provider measurement requirements without pooling their results.

## Acceptance Traceability
| Requirement | Story Acceptance Coverage | BA Acceptance Coverage | Primary Failure/Boundary Coverage | Status |
| --- | --- | --- | --- | --- |
| DSR-101 | AC-S101-1/2; AC-S102-1/2 | AC-301; AC-302 | Unsupported version; duplicate/stale identity | Defined, execution pending |
| DSR-102 | AC-S103-1/2; AC-S104-1/2 | AC-303; AC-304 | Invalid/future policy; conflict/uncertainty | Defined, execution pending |
| DSR-201 | AC-S201-1/2; AC-S202-1/2 | AC-305; AC-307 | Actual-state mismatch; user edit | Defined, execution pending |
| DSR-202 | AC-S203-1/2; AC-S204-1/2 | AC-306; AC-307 | Unsupported surface; contention/abandonment | Defined, execution pending |
| DSR-301 | AC-S301-1/2; AC-S302-1/2 | AC-308; AC-309 | Interrupted write; prohibited content | Defined, execution pending |
| DSR-302 | AC-S303-1/2; AC-S304-1/2 | AC-309 | Wrong target; referenced/corrupt/concurrent receipt | Defined, execution pending |
| DSR-401 | AC-S401-1/2; AC-S402-1/2 | AC-310; AC-311 | Fingerprint mismatch; missing required instruction | Defined, execution pending |
| DSR-402 | AC-S403-1/2; AC-S404-1/2 | AC-311; AC-312 | Gate failure; short valid-pair count | Defined, execution pending |
| DSR-501 | AC-S501-1/2; AC-S503-1/2; AC-S504-1/2 | AC-313; AC-314 | Duplicate/drifted event; negative result; failed statistic | Defined, execution pending |
| DSR-502 | AC-S502-1/2; AC-S503-1/2; AC-S504-1/2 | AC-313; AC-314 | Missing delta boundary; negative result; failed statistic | Defined, execution pending |
| DSR-601 | AC-S601-1/2; AC-S602-1/2 | AC-315 | p95/max/prompt breach; provider-time contamination | Defined, execution pending |
| DSR-602 | AC-S603-1/2; AC-S604-1/2 | AC-316 | Stale authority; one-provider failure; overclaim | Defined, execution pending |

- Every requirement has positive and adverse acceptance coverage. EVID-401 is the executable proof still required.

## QA and Operational Notes
- Build QA in the accepted sequence: contract/unit tests in Slice 1; provider-control/recovery tests in Slices 2/5; frozen runner and QG enforcement in Slice 3; measurement/aggregation in Slices 4/5; net-value/evidence governance in Slice 6.
- Minimum frozen fixtures: read-only repository analysis, isolated test-only code change, and explicit AI-SDLC skill use. Each uses fixed inputs, fresh sessions, completion and instruction oracles, and correlated baseline/guarded attempts.
- QG-301 through QG-309 are hard gates. QA can invalidate; invalid attempts remain; additional attempts may reach the valid-pair target; valid negative/extreme values remain.
- Operational controls: full-load fallback on unsupported/mismatch/contention; one provider/profile mutation lease; baseline snapshot/digest; ownership/liveness recovery; idempotent CAS restoration; preserve user edits; disable optimization when safe restore is impossible.
- Receipt operations are local and explicit. No remote collector is required. Corrupt receipts are quarantined and cannot support claims.
- Observability is privacy-safe: stable codes, versions, fingerprints, requested/actual state, fallback, gate outcomes, measurement refs, restoration, and timing—never raw session content.
- Release evidence must expose failures and bounds, not only successful medians. Provider/version/schema drift triggers requalification.

## Handoff Risks
| Risk ID | Risk | Owner | Impact | Required Action / Exit Evidence |
| --- | --- | --- | --- | --- |
| HR-001 | Delivery spec approved without architecture boundaries or sizing | Engineering + Delivery | Estimates or ownership may be misleading | Architecture/SDD maps each DSR to components/interfaces; team sizes with named owners |
| HR-002 | Provider controls drift after research | Engineering | Mutation may be unsafe or infeasible | Version/capability contract tests and actual-state fixtures pass before guarded use |
| HR-003 | Policy/identity error permits required-content omission | Engineering + QA | Critical safety/quality failure | DEC-024 negative tests, exact identity, precedence, instruction oracles pass |
| HR-004 | Receipt schema/storage leaks or loses evidence | Security/Privacy + Engineering | Privacy or audit failure | Threat review, allowlist/forbidden fixtures, atomicity, permissions, lifecycle tests pass |
| HR-005 | Recovery overwrites user changes | Engineering | Configuration loss | Lease/snapshot/liveness/CAS/crash/user-edit tests pass |
| HR-006 | Measurement window or correlation is wrong | QA + Engineering | False savings result | Versioned adapter fixtures, dedupe/delta validation, pair correlation and replay pass |
| HR-007 | One repository/provider result becomes a broad claim | Product + Delivery | Misleading launch | Bounded evidence labels, per-provider decisions, combined two-provider gate, CONS-401 closure |
| HR-008 | 30% target misses or local overhead erases value | Product + Engineering + QA | MVP may not justify rollout | Preserve negative results; execute causal analysis; accept/revise/reject without silent scope expansion |

- Delivery-spec verdict: ready for strict QA requirements review and architecture/estimation after DEC-026 disposition. It is not implementation signoff or release evidence.
