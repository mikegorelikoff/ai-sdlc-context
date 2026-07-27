---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "requirements-readiness.md"
  path: "specs-refiniment/003-context-guard-product-goal/requirements-readiness.md"
  workspace: "refinement"
  skill: "ai-sdlc-requirements-readiness-review"
  flow_mode: "full"
  state_file: "specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  status: "review"
  owner: "Product and Delivery"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-201"
    - "AC-210"
    - "BR-101"
    - "BR-106"
    - "BR-112"
    - "BR-201"
    - "BR-209"
    - "BR-212"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "DEC-008"
    - "DEC-009"
    - "DEC-010"
    - "DEC-011"
    - "DEC-012"
    - "DEC-013"
    - "DEP-001"
    - "DEP-002"
    - "NFR-101"
    - "NFR-108"
    - "RISK-001"
    - "RISK-009"
    - "WF-201"
    - "WF-206"
  related_artifacts:
    - "specs-refiniment/003-context-guard-product-goal/business-context.md"
    - "specs-refiniment/003-context-guard-product-goal/decision-log.md"
    - "specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md"
    - "specs-refiniment/003-context-guard-product-goal/discovery.md"
    - "specs-refiniment/003-context-guard-product-goal/prfaq.md"
    - "specs-refiniment/003-context-guard-product-goal/qa-strategy.md"
    - "specs-refiniment/003-context-guard-product-goal/qa.md"
    - "specs-refiniment/003-context-guard-product-goal/research.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-requirements-readiness-review"
    - "requirements-readiness"
    - "review"
    - "conditional-ready"
    - "mapping-ready"
---

# requirements-readiness.md

## Feature Summary
- Confirmed: Context Guard targets developers actively using Claude Code and Codex who incur substantial provider-reported cache tokens before productive work. The MVP promise is at least 30% fewer same-task cache tokens without loss of required instructions or evidence (DEC-002 through DEC-004).
- Confirmed: GAP-001 through GAP-004 are definition-complete. DEC-012 bounds provider-native pre-session controls; DEC-009 defines deterministic relevance; DEC-010 defines three quality fixtures; DEC-011 defines provider-specific measurement and aggregation.
- Current product state: the initiative is sufficiently defined for outcome-level goal/capability mapping, but no startup-profile adapter, runner, validator, governed receipt store, or qualifying pilot has been implemented.
- Evidence: discovery.md; prfaq.md; research.md RF-012 through RF-018; business-context.md BR-201 through BR-212; qa.md; qa-strategy.md; decision-log.md.
- Blockers: DEC-005 through DEC-012 remain proposed; receipt lifecycle and startup-overhead threshold remain undefined; causal contribution and the 30% result remain unproven.

## Actors and Stakeholders
- Developer: primary user, task initiator, receipt reviewer, bypass/rollback operator, and beneficiary of lower cache usage.
- Repository maintainer: owns declarative require/exclude/safety policy and may not rewrite authoritative skill content.
- Product owner: owns customer promise, 30% claim boundary, MVP surface, and disposition of DEC-005, DEC-006, DEC-009 through DEC-012.
- Engineering: owns provider capability preflight, authoritative identity, adapters, schema versioning, safe configuration mutation, and rollback.
- QA: owns fixture validity, hard-gate acceptance, invalidation, provider independence, and measurement reproducibility.
- Security/Privacy: owns receipt schema, storage permissions, retention, cleanup, deletion, and response to leakage.
- Claude Code and Codex are authoritative host actors; unsupported or ambiguous behavior must produce `uncertain` plus full-load fallback.
- Evidence: discovery actors; business-context.md actor/permission matrix; qa.md ownership; DEC-009 through DEC-012.
- Gap: named approvers exist by role, but DEC-005 through DEC-012 have not been accepted by those authorities.

## Scope and Boundaries
- In scope: local Claude Code and Codex startup-context control; non-plugin Claude skills; version-qualified Codex CLI/app-server surfaces; deterministic provider/task relevance; provider-specific cache measurement; three frozen pilot fixtures; local sanitized receipts; full-load fallback; bypass and rollback.
- Out of scope: compact skill index as customer solution; semantic/vector classification; mutation or summarization of authoritative skills; centralized telemetry; billed-cost claims; unsupported runtimes; Claude plugin-skill optimization; repository-local Codex filtering; universal effectiveness claims.
- Planning boundary: goal/capability mapping may express outcomes, risk spikes, and decision gates. It must not imply that adapters or the 30% result already exist.
- Delivery boundary: backlog decomposition, user stories, delivery specification, architecture commitment, implementation, and release slicing remain blocked until critical proposed decisions are disposed and receipt governance plus the startup-overhead threshold are defined.
- Evidence: discovery scope; prfaq.md; DEC-004; DEC-009 through DEC-012; research.md RF-018.

## Workflows and Failure Paths
- Defined flow: freeze task/repository/provider/profile inputs; run measurement-only baseline; derive deterministic relevance decisions; apply a provider-native guarded profile before a fresh session/thread; verify actual state; run the same fixture; evaluate all hard quality gates; only then calculate provider-specific cache reduction; restore baseline state.
- Defined exception flow: missing identity, ambiguous policy, unsupported capability, failed action, schema drift, privacy hit, quality mismatch, timeout, or rollback failure invalidates the run/pair. Uncertainty always restores full-load behavior and earns no savings.
- Claude boundary: pre-session `skillOverrides` for non-plugin skills. Codex boundary: startup absolute-path overrides or verified user-level app-server state before `thread/start`.
- Test flow: PILOT-01 read-only analysis, PILOT-02 isolated test-only change, and PILOT-03 explicit required-skill use, each repeated in five valid warm-cache pairs per provider under DEC-011.
- Evidence: WF-D001 through WF-D005; WF-201 through WF-206; QA-301 through QA-312; QG-301 through QG-309; qa-strategy.md.
- Execution gap: workflow contracts are observable and testable, but the profile manager, runner, validators, receipt replay, and live provider runs do not yet exist.

## Requirements and Business Rules
- BR-101 through BR-112 tie the customer outcome to exclusion precision, full required-skill preservation, controlled comparison, privacy, rollback, claim accuracy, provider independence, performance, and evidence scope.
- BR-201 through BR-212 and AC-201 through AC-210 make relevance deterministic: authoritative identity, bounded non-content inputs, fixed precedence, per-session lifetime, `uncertain` fallback, exact irrelevant rules, action verification, and sanitized receipts.
- QA-301 through QA-312 and QG-301 through QG-309 make task quality, instruction preservation, reproducibility, recovery, and provider independence observable.
- DEC-011 defines the exact primary/diagnostic windows, provider adapters, pairing, repetitions, aggregation, variance guard, invalidation, and independent 30% gates.
- Evidence: prfaq.md business requirements; business-context.md catalogs; qa.md; qa-strategy.md; DEC-009 through DEC-012.
- Remaining requirement gaps: receipt storage/permissions/retention/deletion; numeric startup-overhead and interruption thresholds; provider-profile concurrency/locking semantics; and policy-authoring usability. These must be resolved before delivery specification or backlog commitment.

## Data, Integrations, and Non-Functional Requirements
- Data contract: sanitized receipts contain schema/adapter/provider/client/model versions, task/repository/policy/profile/inventory digests, session and boundary IDs, native numeric counters, action/classification reason codes, primer/order timing, quality outcomes, invalidation reason, and unrounded results.
- Prohibited data: prompts, source text, credentials, environment values, raw responses, and full skill bodies. Core operation remains local with no centralized collector.
- Integrations: Claude Code startup settings and local usage records; Codex CLI startup configuration, app-server skills APIs, exact usage events or validated rollout deltas; Context Guard CLI/policy/reporting; disposable worktrees and pytest.
- NFR coverage: safety, privacy, determinism, reversibility, compatibility, auditability, fail-safety, reproducibility, and performance measurement are specified.
- Evidence: NFR-101 through NFR-108; BR-106 through BR-112; BR-209 through BR-212; qa-strategy receipt and environment sections; research RF-009 through RF-018.
- Blocking gaps: filesystem location, mode/ownership, retention, cleanup and deletion rules are missing; provider schema adapters are designed but not implemented; Python 3.10+ qualifying environment is unavailable in the current Python 3.9.6 authoring runtime.

## Dependencies, Risks, and Constraints
- Resolved for definition: DEP-001 provider boundary, DEP-002 benchmark evaluator, GAP-002 relevance contract, and GAP-004 measurement contract.
- External dependencies: version-pinned Claude/Codex behavior, provider cache/counter availability, supported Python 3.10+, stable task/repository fixtures, and safe local configuration access.
- Critical risks: required instruction omission, rollback failure, privacy leakage, mismatched pair inputs, and unsupported provider action. Each has a hard invalidation or full-load response in QA.
- High residual risks: skill metadata may not materially cause cache use; provider/client schemas may drift; warm-cache behavior may vary; startup overhead may erase value; and one repository cannot support broad claims.
- Constraints: no compact index, no semantic model classifier, no mutation of authoritative skills, no centralized monitoring, no billed-cost claim, no cross-provider pooling, and no optimization claim for unsupported surfaces.
- Evidence: discovery risks; prfaq launch risks; research limitations; qa.md risk coverage; qa-strategy.md strategy risks.
- Planning treatment: carry adapter qualification, causal-contribution proof, receipt governance, and latency budget as explicit capability gates; do not present them as completed evidence.

## Decisions, Assumptions, and Open Questions
- Accepted: DEC-002 customer/promise, DEC-003 provider-specific 30% target, and DEC-004 required-instruction preservation plus compact-index exclusion.
- Proposed and materially relied upon: DEC-005 positioning; DEC-006 two-phase pilot; DEC-007 original planning hold; DEC-009 relevance contract; DEC-010 quality evaluator; DEC-011 measurement contract; DEC-012 provider boundary. DEC-001 and DEC-008 also remain proposed and need status reconciliation.
- Readiness does not convert proposals into approval. Product, Engineering, QA, Delivery, and Security/Privacy must dispose the decisions they own before committed backlog or delivery specification.
- Remaining assumptions: provider settings behave as documented for pinned Claude surfaces; app-server-backed Codex clients honor pre-thread state; cache priming produces eligible pairs; skill visibility is a material token contributor.
- Open questions: exact receipt lifecycle; acceptable startup duration/interruption thresholds; profile mutation concurrency/locking; Codex IDE/desktop parity; broader repositories after the pilot.
- Evidence: decision-log.md DEC-001 through DEC-012; research.md open questions; delivery-gap-review residual gaps.
- Required new decision: DEC-013 records this 7/10 conditional readiness verdict without accepting the underlying proposed product/technical decisions.

## Success Measures
- Primary: each provider independently achieves a median reduction of at least 30.0% across 15 valid paired runs, with nearest-rank Q1 at least 0.0% and every five-run fixture median at least 0.0%.
- Quality: every included baseline and guarded run passes QG-301 through QG-309; any hard failure invalidates the pair and cannot be averaged away.
- Safety/reversibility: required, safety-critical, and uncertain skills remain fully available; only explicit irrelevant outcomes are reduced; forced failure restores baseline/full-load configuration.
- Privacy/reproducibility: receipts contain required digests, counters, boundaries, actions, and reason codes with zero prohibited content; reports replay from sanitized receipts.
- Scope of claim: provider-reported cache-token reduction for the pinned repository, tasks, clients, and models; never billed cost or universal effectiveness.
- Secondary: startup duration and developer interruption must not erase value, but numeric thresholds are still missing and block committed delivery acceptance.
- Evidence: DEC-003; DEC-010; DEC-011; qa.md signoff gates; qa-strategy.md pairing/aggregation rules.
- Status: all measures are definition-complete; none has qualifying execution evidence yet.

## Source Coverage
- `specs-refiniment/003-context-guard-product-goal/discovery.md`: customer/problem evidence, value, MVP, original risks, assumptions, measures, and local-log limitations.
- `specs-refiniment/003-context-guard-product-goal/prfaq.md`: working-backwards narrative, BR-101 through BR-112, NFR-101 through NFR-108, rollout, success measures, and launch risks.
- `specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md`: original gaps plus the 2026-07-27 definition-complete update for GAP-001 through GAP-004.
- `specs-refiniment/003-context-guard-product-goal/business-context.md`: actor/permission model, WF-201 through WF-206, BR-201 through BR-212, AC-201 through AC-210, and conservative fallback.
- `specs-refiniment/003-context-guard-product-goal/research.md`: 6 questions, 12 registered sources, 18 findings, version-pinned provider capability evidence, measurement semantics, limitations, and open questions.
- `specs-refiniment/003-context-guard-product-goal/qa.md`: three frozen fixtures, QA-301 through QA-312, regressions, environments, validators, and QG-301 through QG-309.
- `specs-refiniment/003-context-guard-product-goal/qa-strategy.md`: provider adapters, windows, warm-cache pairing, repetitions, aggregation, receipt fields, and strategy risks.
- `specs-refiniment/003-context-guard-product-goal/decision-log.md`: status and ownership of DEC-001 through DEC-013.
- `specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon` and both refinement indexes: lifecycle and routing authority.
- The full-flow analyzer consumed nine primary inputs at a 24,000-token budget and emitted 164 deferred ranges; every referenced source/section was read before this verdict. Existing product README/specs are traced through discovery and PRFAQ rather than reinterpreted here.
- Open-question control: each unresolved item has an owner in Blocking Gaps, an explicit impact on progression, and a resolution or next step in Required Follow-Up.

## Readiness Score
- Score: **7/10 — ready for discovery alignment and outcome-level goal/capability mapping only**.
- Improvement from DEC-008's 5/10: the provider boundary, relevance behavior, quality evaluator, and measurement/aggregation contract are now explicit, provider-specific, traceable, and testable.
- Cap: critical product/technical/QA decisions remain proposed; receipt governance, startup-overhead thresholds, concurrency semantics, and policy-authoring usability are missing; no adapter, runner, validation receipt, or live result exists.
- Interpretation: goal/capability mapping may proceed if it preserves proposed status and carries evidence/decision gates. Backlog decomposition, user stories, release commitment, delivery specification, architecture selection, implementation SDD, and effectiveness claims remain no-go.
- Evidence: readiness checklist; DEC-009 through DEC-012; research.md; business-context.md; qa.md; qa-strategy.md.

## Dimension Assessment
| Dimension | Evidence | Status | Gap | Owner |
| --- | --- | --- | --- | --- |
| Customer and problem | DEC-002; discovery customer evidence; local usage observations | 8/10 strong | One-user evidence; frequency and willingness to adopt/pay unvalidated | Product |
| Value and business case | DEC-003; PRFAQ; narrow provider-token claim | 7/10 adequate | Skill contribution and 30% result unproven | Product and Engineering |
| Scope and boundaries | DEC-004; DEC-012; explicit unsupported surfaces/non-goals | 8/10 strong | Critical scope decisions remain proposed | Product |
| Scenarios and workflows | WF-D001 through WF-D005; WF-201 through WF-206; QA fixtures | 8/10 strong | Profile concurrency and operational recovery details missing | Engineering |
| Requirements and testability | BR-101 through BR-212; AC-201 through AC-210; QA/QG gates | 8/10 strong | Receipt lifecycle, latency, interruption, and policy-authoring rules missing | Product, Engineering, QA |
| Technical feasibility | Research RF-012 through RF-018; Codex no-inference A/B; DEC-012 | 7/10 adequate | Claude live qualification and Codex app-server/IDE parity unexecuted | Engineering |
| Data and privacy | Prohibited fields; receipt field catalog; QG-306 | 6/10 partial | Storage path, permissions, retention, cleanup, deletion undefined | Security/Privacy and Engineering |
| Risks and constraints | RISK-001 through RISK-009; QA/strategy mitigations | 9/10 strong | Mitigations lack execution evidence | Cross-functional owners |
| Decisions and consistency | DEC-001 through DEC-012; explicit supersession evidence | 5/10 blocked | DEC-005 through DEC-012 proposed; stale upstream statements remain | Product and Delivery |
| Traceability | Metadata/indexes; BR/AC/QA/QG/DEC links | 9/10 strong | Later backlog/delivery artifacts do not exist yet | BA, Delivery, QA |

## Blocking Gaps
- GOV-301 — Decision disposition. DEC-005 through DEC-012 materially define positioning, rollout, relevance, quality, measurement, and provider scope but remain proposed. Owners: Product, Delivery, Engineering, QA. Blocks: committed backlog, delivery specification, architecture, and implementation.
- DATA-301 — Receipt lifecycle. Schema content is bounded, but path, filesystem permissions, ownership, retention, cleanup, deletion, corruption handling, and concurrent access are undefined. Owners: Security/Privacy and Engineering. Blocks: delivery specification and implementation.
- PERF-301 — Net-value thresholds. Startup duration and developer-interruption metrics exist without numeric acceptance or failure thresholds. Owners: Product and Engineering. Blocks: delivery acceptance and release slicing.
- OPS-301 — Profile coordination. Safe handling of concurrent sessions, crashed runs, stale locks, user edits during guarded mode, and rollback conflict is not specified. Owner: Engineering. Blocks: implementation-ready stories.
- EVID-301 — Execution qualification. Claude listing/token behavior, Codex app-server/IDE state, provider adapters, fixture runner, validators, and five-pair pilots are unexecuted. Owners: Engineering and QA. Blocks: effectiveness claim and release; it should appear as gated capability work, not block outcome-level mapping.
- CONS-301 — Upstream staleness. Discovery and earlier gap-review prose still contain superseded open questions. Owner: BA/Product. Blocks: final handoff, not goal mapping, because this review states the current authority chain explicitly.

## Required Follow-Up
1. Goal/capability mapping: translate DEC-002 through DEC-004 plus proposed DEC-009 through DEC-012 into outcome goals, actors, capabilities, evidence gates, and epics. Mark proposed boundaries explicitly and include EVID-301 as qualification work rather than assumed functionality.
2. Governance checkpoint before backlog decomposition: Product/Delivery/Engineering/QA accept, revise, reject, or supersede DEC-005 through DEC-012 and reconcile DEC-001, DEC-007, and DEC-008.
3. Receipt governance: Security/Privacy and Engineering define path, mode/ownership, retention, cleanup/deletion, corruption recovery, concurrency, and privacy validation.
4. Net-value decision: Product and Engineering set numeric startup-duration and interruption thresholds plus failure disposition.
5. Operational contract: Engineering defines locking, stale-run detection, crash recovery, user-edit conflicts, and idempotent rollback for provider profiles.
6. Qualification plan: Engineering/QA implement versioned adapters, manifest/runner/validators, privacy replay, and the DEC-011 provider pilots in Python 3.10+.
7. Consistency cleanup: refresh superseded discovery/business/gap statements before delivery handoff and keep broader repositories deferred until the pilot qualifies.
8. Gate progression: do not start backlog decomposition, stories, release slicing, delivery specification, architecture, or implementation until items 2 through 5 are resolved and the backlog gap review confirms zero planning blockers.

## Readiness Verdict
- Verdict: **CONDITIONALLY READY for goal/capability/epic mapping; NO-GO for committed delivery planning or implementation.**
- Why: the customer, outcome, bounded MVP, provider control boundary, deterministic relevance behavior, quality evaluator, and measurement gate are sufficiently explicit to map what capabilities must exist. The package no longer requires solution invention at that level.
- Conditions on mapping: preserve proposed decision status; distinguish definitions from implemented evidence; include full-load fallback, privacy, rollback, provider independence, and qualification gates; do not promise the 30% result.
- No-go boundary: backlog decomposition, user stories, release slicing, delivery specification, architecture commitment, implementation SDD, and launch/effectiveness claims remain blocked by GOV-301, DATA-301, PERF-301, and OPS-301. EVID-301 blocks qualification and release.
- Score authority: 7/10 under proposed DEC-013; this supersedes DEC-008's 5/10 only if DEC-013 is accepted.
- Next lifecycle skill: `ai-sdlc-goal-capability-and-epic-mapping`.
- Validation status: artifact structure and traceability must pass the full-flow scaffold; document-level whitespace and index checks are required. No product pilot was executed by this review.
