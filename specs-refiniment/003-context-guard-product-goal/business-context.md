---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "business-context.md"
  path: "specs-refiniment/003-context-guard-product-goal/business-context.md"
  workspace: "refinement"
  skill: "ai-sdlc-ba"
  flow_mode: "full"
  state_file: "specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  status: "review"
  owner: "Product and Engineering"
  created_at: "2026-07-26"
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
    - "GOAL-001"
    - "GOAL-002"
    - "GOAL-003"
    - "GOAL-004"
    - "WF-301"
    - "WF-302"
    - "WF-303"
    - "WF-304"
    - "WF-305"
    - "WF-306"
    - "WF-307"
    - "WF-308"
    - "WF-309"
  related_artifacts:
    - "specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md"
    - "specs-refiniment/003-context-guard-product-goal/backlog.md"
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
    - "ai-sdlc-ba"
    - "business-context"
    - "review"
    - "relevance-contract"
---

# business-context.md

## Feature Summary
- **Goal:** reduce avoidable provider-reported cache tokens before productive work for developers using Claude Code and Codex, without losing required or safety-critical instructions, evidence, privacy, or control.
- **Problem:** current local logs reveal substantial pre-work cache activity only after consumption and cannot prevent or causally attribute irrelevant full skill content at provider startup.
- Context Guard will add deterministic, provider-bounded startup relevance control, safe full-load fallback, local sanitized receipts, quality-first paired measurement, recovery, and bounded rollout decisions.
- Accepted authority through DEC-025 defines the customer, 30% target, conservative classification, provider surfaces, receipt lifecycle, recovery, performance, policy v2, backlog, stories, and six release slices.
- This business context defines observable behavior and permissions. It does not choose APIs, packages, schemas beyond accepted product contracts, or claim that implementation/effectiveness evidence exists.

## Actors and Stakeholders
- Developer: primary beneficiary and task initiator; starts guarded sessions, invokes skills, inspects/deletes receipts, bypasses optimization, and restores baseline behavior.
- Repository maintainer: authors repository-level relevance rules within the accepted layered policy contract.
- Product: owns customer promise, MVP scope, provider pass/fail interpretation, net-value boundary, and claims.
- Delivery: owns slice progression, evidence-package readiness, and combined rollout governance.
- Engineering: owns policy implementation, provider adapters, inventory, state coordination, receipts, measurement adapters, instrumentation, and recovery.
- QA: owns frozen fixtures, hard quality gates, run invalidation, paired protocol, and qualification signoff. Security/Privacy co-owns receipt governance and leakage prevention.
- Claude Code and Codex are external versioned hosts that expose authoritative skill state, supported startup controls, and provider-native usage evidence.

## Scope and Boundaries
- In scope: local pre-session capability/version checks; authoritative skill inventory and fingerprints; DEC-024 policy validation; deterministic classification; supported startup profile application; actual-state verification; fresh-session execution; full-load fallback; bypass/rollback; local receipt lifecycle; three frozen fixtures; provider-specific paired measurement; net-value evaluation; per-provider and combined decisions.
- Claude boundary: version-qualified non-plugin skills controlled through startup `skillOverrides`; only explicit `irrelevant` may request `user-invocable-only`.
- Codex boundary: version-qualified CLI absolute-path `skills.config` and qualified app-server user-level state verified before `thread/start` and restored afterward.
- Customer MVP requires independent qualification of both providers. Claude-only and Codex-only outputs are internal qualification results.
- Out of scope: skill rewriting/summarization, semantic model classification, compact skill index as the product, mid-session interception, Claude plugins, repository-local Codex filtering, unqualified IDE/desktop behavior, enterprise administration, centralized telemetry, billed-cost claims, and universal/generalized effectiveness claims.
- T-017 IDE/desktop parity and broader repository evidence remain post-MVP unless explicitly brought into scope by a later decision.

## Workflows and Failure Paths
- Primary guarded flow: declare task -> preflight provider/version/surface -> inventory authoritative skills -> validate effective policy -> classify every skill -> capture baseline/lease -> apply supported profile -> verify requested versus actual state -> start fresh session -> execute fixture/task -> quality gates -> measurement -> receipt -> restore.
- Baseline comparison flow uses the same task, model, repository state, provider version, fixture manifest, and quality oracles without guarded omission.
- Audit flow lets authorized local users inspect sanitized receipts and reproduce decisions from fingerprints, reason codes, and versioned inputs without raw content.
- Unsupported, stale, conflicting, duplicate, ambiguous, uncorrelated, or unmeasurable conditions use full load or invalidate evidence; they never infer savings.
- Contention uses full-load fallback. Abandoned state uses ownership/liveness evidence. Restoration is idempotent compare-and-swap and preserves user edits.
- Any quality, privacy, recovery, receipt, counter, correlation, or net-value failure invalidates the affected claim while retaining diagnostic evidence and baseline operation.

## Requirements and Business Rules
- Only explicit `irrelevant` may reduce skill visibility. `safety-critical`, `required`, explicit invocation, conflict, and `uncertain` retain complete authoritative content.
- Classification uses authoritative provider identity, accepted policy, declared task/repository signals, and fixed DEC-009 precedence. Token size, historic usage, and semantic model judgment cannot authorize irrelevance.
- Policy version 2 follows DEC-024: built-in/user/repository layering, mode-only environment override, exact skill identity, unique rule IDs, whole-rule replacement/disable semantics, actionable diagnostics, v1 compatibility, future-version rejection, and explicit backed-up atomic migration.
- Actual provider state must be verified before model work. Unsupported or mismatched state uses full load and earns no credit.
- Quality gates precede token evaluation; providers are measured and decided independently; negative valid results remain; invalid attempts are retained and excluded.
- Receipts are local, minimized, access-controlled, versioned, atomic, user-inspectable/deletable, retained for 30 days by default, safely pruned, locked, and quarantined when corrupt.

## Data, Integrations, and Non-Functional Requirements
- Provider inputs: provider/client version, supported surface/capabilities, authoritative skill identities, metadata/body digests, requested/actual startup state, and provider-native usage events.
- Decision inputs: declared task ID and bounded labels, repository identity/state fingerprint, policy/version/digest, inventory digest, explicit invocation/mandatory flags, and stable rule reason codes.
- Receipt output may include schema/version, run/pair IDs, timestamps, versions, fingerprints/digests, classification, reason codes, requested/actual action, fallback reason, quality result, measurement references, and restoration status.
- Prohibited receipt data: prompts, responses, source content, credentials, secrets, environment values, and full skill bodies.
- Claude metric is deduplicated cache-creation plus cache-read tokens. Codex metric is exact cached-input tokens or a validated cumulative delta. Providers are never pooled.
- Determinism, privacy, provider isolation, fail-safe full inclusion, reproducibility, reversibility, and non-destructive configuration are mandatory.
- Local added overhead must have p95 <=750 ms and no qualifying run >2 seconds, excluding provider network/model time; happy path adds zero prompts and unsafe recovery permits at most one actionable prompt.

## Dependencies, Risks, and Constraints
- Hard dependency order is accepted DEC-025: trusted foundation -> Claude vertical -> shared quality runner -> Claude feasibility -> Codex vertical/feasibility -> net-value and combined decision.
- External dependencies: supported Claude/Codex versions and surfaces, stable provider usage schemas, local filesystem controls, Python 3.10+ qualification runtime, and a frozen pilot repository/fixture manifest.
- EVID-401 is implementation and qualification work. It is not evidence already achieved. CONS-401 must reconcile stale historical wording before S-603 delivery handoff.
- Highest risks: provider drift; omitted required instructions; user configuration corruption; receipt leakage; counter misattribution; benchmark variance; causal overclaim; overhead erasing benefit; generalizing one repository.
- Controls: version/capability gates, exact identities, conservative precedence, actual-state verification, full-load fallback, lease/CAS recovery, field allowlists, hard quality gates, alternating paired runs, no outlier deletion, provider-separated decisions, and claim bounds.
- Capacity, dates, and engineering estimates are not business facts. Owner: Delivery + Engineering. Impact: no calendar commitment is authorized. Resolution/next step: size after delivery specification and architecture review.

## Decisions, Assumptions, and Open Questions
- Accepted authority: DEC-002 through DEC-006, DEC-009 through DEC-014, and DEC-016 through DEC-025. DEC-001, DEC-007, DEC-008, and DEC-015 are superseded.
- Assumption BA-A01: role owners remain team/discipline roles until named assignees are supplied. Owner: Delivery. Impact: accountability is clear by role but not person. Resolution/next step: assign during delivery planning.
- Assumption BA-A02: the first qualification repository and three frozen fixture types remain suitable for feasibility, not general-market proof. Owner: Product + QA. Impact: claims remain repository/fixture bounded. Resolution/next step: select broader evidence only after MVP feasibility.
- Qualification question BA-OQ01: whether each pinned provider surface and counter window remains supported at execution time. Owner: Engineering + QA. Impact: a surface may become full-load/unmeasurable. Resolution/next step: preflight and contract-test in its slice.
- Evidence question BA-OQ02: whether skill context is large enough causally to achieve 30% per provider. Owner: Product + Engineering + QA. Impact: rollout may be revised or rejected. Resolution/next step: execute T-018 and S-503/S-504 without expanding scope silently.
- Compatibility question BA-OQ03: Codex IDE/desktop parity. Owner: Engineering. Impact: post-MVP only. Resolution/next step: T-017 after the Codex CLI vertical.

## Success Measures
- GOAL-001: for each provider independently, median guarded normalized cache tokens are at least 30% lower than paired baseline after five valid pairs for each of three fixtures, with nearest-rank Q1 >=0% and every fixture median >=0%.
- GOAL-002: zero hard failures and complete required/safety instruction preservation across valid pairs; bypass, fallback, restoration, and recovery succeed.
- GOAL-003: every credited run is version-preflighted, provider-isolated, receipted, reproducible, privacy-safe, and recoverable; unsupported state uses full load.
- GOAL-004: local p95/max/prompt limits pass and every claim remains provider/version/model/repository/fixture bounded.
- Planning quality: every MVP story maps to actors, rules, acceptance criteria, dependencies, a release slice, and an evidence owner.
- Passing these measures during implementation is required for rollout; this BA artifact records targets, not achieved results.

## Source Coverage
- `specs-refiniment/003-context-guard-product-goal/discovery.md`: customer, observed problem, MVP, metrics, constraints, and exclusions.
- `specs-refiniment/003-context-guard-product-goal/prfaq.md`: working-backwards value, BR-101 through BR-112, rollout, and launch risks.
- `specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md`: original delivery gaps and definition evidence.
- `specs-refiniment/003-context-guard-product-goal/requirements-readiness.md`: readiness history and controlled follow-up.
- `specs-refiniment/003-context-guard-product-goal/goal-capability-map.md`: goals, capabilities, epics, actors, and dependencies.
- `specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md`: zero current planning blockers, EVID-401, and CONS-401.
- `specs-refiniment/003-context-guard-product-goal/backlog.md`: 12 features, 24 stories, 18 tasks, and readiness.
- `specs-refiniment/003-context-guard-product-goal/user-stories.md`: 48 acceptance criteria, 48 scenarios, and story dependencies.
- `specs-refiniment/003-context-guard-product-goal/release-slicing.md`: accepted six-slice plan and 8.5/10 readiness verdict.
- `specs-refiniment/003-context-guard-product-goal/qa.md`: fixtures, hard gates, invalidation, and regression scope.
- `specs-refiniment/003-context-guard-product-goal/qa-strategy.md`: measurement windows, pairing, aggregation, and privacy replay.
- `specs-refiniment/003-context-guard-product-goal/research.md`: provider surfaces, limitations, version evidence, and compatibility questions.
- `specs-refiniment/003-context-guard-product-goal/change-impact.md`: DEC-024/POL-401/S-103 owner-impact evidence.
- `specs-refiniment/003-context-guard-product-goal/decision-log.md`: current authority and supersession through accepted DEC-025.
- `specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon`: lifecycle authority. The full-flow 24,000-token context pack and its deferred evidence ranges were reviewed before synthesis.

## Current Behavior
- Context Guard currently provides local CLI/hook policy behavior for supported file reads, searches, commands, lifecycle events, and compact output; it does not yet implement the accepted skill-relevance engine or guarded provider profiles.
- Existing provider behavior uses host-owned skill discovery and progressive disclosure. Context Guard cannot assume a generic mutable startup-context hook.
- Local Claude and Codex logs expose large provider-specific input/cache counters after activity, but do not isolate skill metadata or bodies as the cause and do not prove billed cost.
- No current end-to-end receipt links declared task, authoritative skill inventory, requested/actual provider action, quality outcome, cache window, and restoration result under the accepted contracts.
- Product requirements, stories, policy semantics, release slices, and gates are now accepted as planning authority, while adapters, runner, pilots, and evidence remain to be implemented.
- Therefore the current safe operational behavior is full load; no 30% savings or provider qualification is claimed.

## Desired Behavior
- A developer starts a guarded session for a declared task without an extra happy-path prompt. Context Guard preflights the provider/version/surface and refuses unsafe mutation.
- The system inventories authoritative skills, validates effective policy v2, and produces deterministic `safety-critical`, `required`, `irrelevant`, or `uncertain` outcomes with stable reason codes.
- Only an exact `irrelevant` outcome requests the supported visibility reduction. Required, safety-critical, explicit, conflicting, or uncertain skills retain complete authoritative content.
- Before model work, requested and actual provider state match; otherwise the system restores or preserves full load and writes a sanitized failure receipt.
- A fresh session executes the declared task. Quality/privacy/recovery gates run before cache measurements can influence any decision.
- Baseline and guarded runs produce correlated, provider-specific evidence. Product receives honest pass/revise/reject results, including negative outcomes.
- After the run, baseline state is restored without overwriting unrelated user edits. The developer can inspect/delete local receipts and bypass optimization at any time.
- The customer MVP is eligible only when both Claude Code and Codex independently satisfy quality, privacy, recovery, measurement, and net-value gates.

## Actor and Permission Matrix
| Actor | Role | Permissions | Restrictions | Source |
| --- | --- | --- | --- | --- |
| Developer | Primary user | Declare task; start/bypass guarded mode; explicitly invoke skills; inspect/delete own receipts; request restore | Cannot be forced to disclose raw prompts/source or accept unsafe mutation | DEC-002; DEC-004; S-101; S-201; S-203; S-303 |
| Repository maintainer | Policy author | Create/validate repository policy rules and bounded task/repository selectors | Cannot rewrite skills, weaken mandatory/safety rules, or overwrite existing policy via init | DEC-024; S-103 |
| Product | Outcome/claim owner | Set scope and targets; accept/revise/reject provider and combined rollout | Cannot pool providers, claim billed cost, or override failed gates | DEC-003; DEC-006; S-504; S-604 |
| Delivery | Lifecycle owner | Advance slices and accept evidence-package readiness | Cannot advance combined claim without both provider packages and CONS-401 | DEC-025; S-603 |
| Engineering | Technical control owner | Implement preflight, inventory, adapters, leases, receipts, metrics, instrumentation, recovery | Must preserve full load on ambiguity and user edits; no semantic classifier | DEC-009; DEC-012; DEC-017 |
| QA | Quality/evidence authority | Own fixtures/oracles; invalidate attempts; approve valid pairs and qualification evidence | Cannot expose token evaluation before hard gates or delete valid negative results | DEC-010; DEC-011; S-401–S-404 |
| Security/Privacy | Receipt governance | Review schema, forbidden-content fixtures, permissions, retention, and deletion | Cannot authorize raw prompts/source/secrets/full skill bodies in receipts | DEC-016; BR-212 |
| Claude Code/Codex | External host boundary | Expose versioned inventory/state, supported controls, and usage evidence | Unverified/unsupported behavior cannot authorize omission or measurement | DEC-012; research.md |
| Context Guard | Local evaluator/coordinator | Normalize accepted inputs; request/verify supported actions; receipt and restore | No remote raw-content dependency, skill rewriting, inferred counters, or silent omission | DEC-004; BR-108; BR-206 |

## Workflow Detail
| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Source |
| --- | --- | --- | --- | --- | --- | --- |
| WF-301 | Developer requests guarded startup | Developer; Context Guard | Preflight provider/version/surface; record eligibility | Supported execution may continue | Unsupported/ambiguous -> full load, no mutation, receipt | S-101; DEC-012 |
| WF-302 | Eligible startup continues | Context Guard; host | Inventory authoritative skills; validate policy; classify with precedence | Every skill has deterministic outcome/reason | Missing/duplicate/stale/conflict -> uncertain/full content | S-102–S-104; DEC-009; DEC-024 |
| WF-303 | Guarded profile is prepared | Context Guard; provider adapter | Acquire lease; snapshot/digest; request profile; verify actual state; start fresh session | Verified guarded session | Contention/mismatch -> full load; user edit -> no overwrite | S-201–S-204; DEC-017 |
| WF-304 | Guarded attempt finishes | Context Guard; QA | Atomically write minimized receipt; scan privacy; retain/quarantine/prune as allowed | Reproducible local evidence | Write/schema/privacy failure -> invalid evidence/full load | S-301–S-304; DEC-016 |
| WF-305 | Qualification pair executes | QA; Engineering | Run frozen baseline/guarded attempts; evaluate completion/instruction oracles and QG-301–QG-309 | Pair becomes valid or invalid with reason | Any gate/mismatch -> token access denied, attempt retained | S-401–S-404; DEC-010 |
| WF-306 | Valid pair reaches measurement | QA; provider adapter | Extract provider window; correlate/dedupe/delta; append ledger | Reproducible per-attempt cache value | Missing/drifted boundary -> unmeasurable, never zero | S-501/S-502; DEC-011 |
| WF-307 | Required valid pairs complete | QA; Product | Aggregate without outlier deletion; report medians/Q1/fixture results and causal bounds | Provider pass/revise/reject recommendation | Any statistical/quality gate miss -> provider does not qualify | S-503/S-504; DEC-011 |
| WF-308 | Session ends or failure occurs | Context Guard; Developer | Restore with CAS; verify baseline; preserve user edits; offer one recovery action only if necessary | Baseline/full-load state restored | Unsafe restore -> optimization disabled and evidence preserved | S-202/S-204; DEC-017/DEC-018 |
| WF-309 | Both provider packages exist | Product; Delivery; QA | Evaluate net value; reconcile CONS-401; assemble bounded package; decide each provider and combined MVP | Accepted/revised/rejected decisions with rationale | One provider fails -> combined MVP cannot pass | S-601–S-604; DEC-025 |

## Business Rule Catalog
| Rule ID | Rule | Applies To | Failure Behavior | Source | Decision Ref |
| --- | --- | --- | --- | --- | --- |
| BR-101 | Irrelevant full skill content must be prevented only in guarded runs at a supported boundary. | Startup control | Unsupported boundary uses full load | prfaq.md | DEC-004; DEC-012 |
| BR-102 | Required and safety-critical instructions remain complete and authoritative. | All guarded decisions | Hard failure; invalidate and restore | prfaq.md | DEC-004; DEC-010 |
| BR-103 | Uncertainty favors correctness and full inclusion. | Classification/control | No omission or savings credit | prfaq.md | DEC-009 |
| BR-104 | Claude and Codex measurements and decisions remain separate. | Measurement/claims | Reject pooled result | prfaq.md | DEC-003; DEC-011 |
| BR-105 | Comparisons require equivalent task/model/repository/provider inputs and quality. | Paired pilot | Invalidate pair | prfaq.md | DEC-010; DEC-011 |
| BR-106 | Report raw provider token calculations, not inferred billed cost. | Evidence/claims | Claim rejected | prfaq.md | DEC-003; DEC-006 |
| BR-107 | Raw prompts, source, credentials, responses, secrets, and full skills are prohibited in receipts. | Data/privacy | Invalidate; quarantine/review | prfaq.md | DEC-016 |
| BR-108 | Original skills and unrelated configuration remain unchanged; intervention is reversible. | Provider profiles | Full load; restore; release block on loss | prfaq.md | DEC-017 |
| BR-109 | Compact skill index is not the customer solution. | Product scope | Scope/design rejected | prfaq.md | DEC-004 |
| BR-110 | 30% claims require named, passing provider/model/task evidence. | Claims | No effectiveness claim | prfaq.md | DEC-003; DEC-011 |
| BR-111 | Net-value limits cannot be overridden by token savings. | Performance | Affected surface fails claim | backlog.md | DEC-018 |
| BR-112 | Combined MVP requires independent qualification of both providers. | Rollout | Combined result revised/rejected | backlog.md | DEC-006; DEC-025 |
| BR-201 | Identity uses provider/version/scope/name/canonical locator/metadata and body digests. | Inventory/receipts | Missing/duplicate/change -> uncertain | business-context.md; S-102 | DEC-009 |
| BR-202 | Safety-critical wins and retains complete content. | Classification | Lower rules ignored and receipted | business-context.md | DEC-009 |
| BR-203 | Explicit invocation or mandatory host/repository state becomes required unless safety-critical. | Classification | Ambiguity -> uncertain/full content | business-context.md | DEC-009 |
| BR-204 | Exact policy-required match becomes required unless higher precedence applies. | Policy evaluation | Invalid/conflict -> uncertain | business-context.md | DEC-009; DEC-024 |
| BR-205 | Irrelevant requires exact identity/rule match and absence of higher precedence. | Policy evaluation | No positive match never implies irrelevance | business-context.md | DEC-009; DEC-024 |
| BR-206 | Missing, stale, unsupported, conflicting, or ambiguous evidence becomes uncertain. | All decisions | Full content; zero credit | business-context.md | DEC-009 |
| BR-207 | Precedence is control-safe uncertain, safety-critical, mandatory/explicit required, policy-required, policy-irrelevant, default uncertain. | Evaluator | Equal conflict -> uncertain | business-context.md | DEC-009 |
| BR-208 | Only irrelevant maps to visibility reduction; actual-state failure restores full load. | Provider adapters | Invalidate savings | business-context.md | DEC-009; DEC-012 |
| BR-209 | Snapshot lifetime is bound to provider/version/task/repository/policy/inventory/profile fingerprints. | Reuse | Change forces recompute | business-context.md | DEC-009 |
| BR-210 | Classification inputs exclude raw content, semantic model judgment, and token totals. | Input contract | Privacy/determinism failure | business-context.md | DEC-009 |
| BR-211 | Receipt records the accepted minimized version/fingerprint/action/evidence fields. | Audit | Missing fields -> non-reproducible/unmeasurable | business-context.md | DEC-016 |
| BR-212 | Receipt lifecycle and content follow DEC-016 privacy and control limits. | Storage | Invalidate/quarantine/restore | business-context.md | DEC-016 |

## Acceptance Criteria
| AC ID | Given | When | Then | Rule Ref | Source |
| --- | --- | --- | --- | --- | --- |
| AC-301 | A supported or unsupported configured client | Preflight runs | Provider/version/surface/capabilities are recorded; unsupported state causes no mutation and full load | BR-108 | AC-S101-1/2 |
| AC-302 | Stable or defective host inventory | Inventory resolves twice | Stable identities/digests match; missing/duplicate/stale identity becomes unsupported/uncertain | BR-201; BR-206 | AC-S102-1/2 |
| AC-303 | Valid, legacy, conflicting, duplicate, disabled, or future policy | Validate/migrate runs | DEC-024 layering, diagnostics, compatibility, and atomic migration behavior is observable | BR-204; BR-205 | AC-S103-1/2 |
| AC-304 | Same or conflicting classification inputs | Evaluation repeats | Outcomes/reasons are deterministic; only exact irrelevant may reduce visibility | BR-202–BR-210 | AC-S104-1/2 |
| AC-305 | Supported Claude profile or state mismatch | Guarded startup runs | Actual state is verified before model work; mismatch uses full load and no credit | BR-208 | AC-S201-1/2 |
| AC-306 | Supported Codex CLI/app-server or unsupported surface | Guarded startup runs | Pre-thread/absolute-path state is verified; unsupported/mismatch uses full load | BR-208 | AC-S203-1/2 |
| AC-307 | Baseline snapshot, contention, abandoned state, or user edit | Restore/recovery runs | Lease/CAS rules preserve user edits and restore idempotently or disable optimization safely | BR-108 | AC-S202-1/2; AC-S204-1/2 |
| AC-308 | Any guarded attempt including interrupted write | Receipt commits | One atomic schema-valid minimized receipt exists or partial data is rejected safely | BR-211; BR-212 | AC-S301-1/2 |
| AC-309 | Receipt corpus and lifecycle targets | Privacy/replay/inspect/delete/maintenance runs | Prohibited content is absent; replay works; only eligible data is displayed/deleted/pruned/quarantined | BR-107; BR-212 | AC-S302 through AC-S304 |
| AC-310 | Frozen task/model/repository manifest | Three-fixture suite runs | Fresh correlated baseline/guarded attempts execute; fingerprint mismatch invalidates | BR-105 | AC-S401-1/2 |
| AC-311 | Fixture outputs including explicit skill use | Machine oracles and hard gates run | Completion/instruction preservation is explicit and token access remains blocked on any failure | BR-102 | AC-S402; AC-S403 |
| AC-312 | Invalid or negative attempt | Ledger processing runs | Invalid stays retained/excluded with reason; valid negative/extreme result stays included | BR-105 | AC-S404; AC-S503-2 |
| AC-313 | Version-pinned Claude or Codex events | Adapter extracts | Claude dedupe sum or Codex exact/delta value is reproducible; ambiguity is unmeasurable, not zero | BR-104; BR-106 | AC-S501; AC-S502 |
| AC-314 | Five valid pairs for each fixture/provider | Aggregation runs | Unrounded reductions, nearest-rank quartiles, fixture medians, provider median, and causal bounds are reported | BR-104; BR-110 | AC-S503; AC-S504 |
| AC-315 | Qualifying guarded runs | Local timing/prompt gate runs | p95/max/prompt results exclude provider time and any breach fails the affected claim | BR-111 | AC-S601; AC-S602 |
| AC-316 | Completed provider packages and current authority | Delivery decision runs | Bounded evidence is complete; each provider has a rationale; combined passes only when both independently pass | BR-112 | AC-S603; AC-S604 |

## Business Context Gaps
- **No blocking business-context gap remains for delivery specification.** Accepted DEC-009 through DEC-025 define classification, provider boundaries, quality, measurement, data lifecycle, recovery, performance, sequencing, stories, and policy behavior.
- BA-G01 execution evidence: adapters, runner, provider counters, paired results, recovery tests, and net-value measurements are not yet produced. Owner: Engineering + QA. Impact: implementation/release claims remain unavailable. Resolution/next step: execute EVID-401 through accepted slices.
- BA-G02 consistency: historical artifacts still contain superseded readiness/proposal language in body text or retained metadata tags. Owner: BA + Product. Impact: delivery package could cite stale authority. Resolution/next step: close CONS-401 before S-603 and delivery handoff.
- BA-G03 estimation inputs: architecture boundaries, team sizing, assignees, capacity, and dates are not supplied. Owner: Delivery + Engineering. Impact: no schedule commitment. Resolution/next step: delivery specification, optional architecture review, and team estimation.
- BA-G04 compatibility: Codex IDE/desktop parity is outside the accepted MVP unless qualified. Owner: Engineering. Impact: those surfaces remain full-load/unclaimed. Resolution/next step: T-017 after the Codex CLI vertical.
- BA-G05 generalization: one repository cannot support a universal savings claim. Owner: Product + QA. Impact: launch language remains bounded. Resolution/next step: choose additional repositories only after the MVP feasibility decision.
