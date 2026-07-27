---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "user-stories.md"
  path: "specs-refiniment/003-context-guard-product-goal/user-stories.md"
  workspace: "refinement"
  skill: "ai-sdlc-user-story-decomposition"
  flow_mode: "full"
  state_file: "specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  status: "review"
  owner: "Business Analysis and Product"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-201"
    - "AC-210"
    - "BR-101"
    - "BR-108"
    - "BR-110"
    - "BR-111"
    - "BR-112"
    - "BR-201"
    - "BR-206"
    - "BR-208"
    - "BR-209"
    - "BR-211"
    - "BR-212"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
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
    - "DEC-019"
    - "DEC-020"
    - "DEC-022"
    - "DEC-023"
    - "DEC-024"
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
    - "specs-refiniment/003-context-guard-product-goal/requirements-readiness.md"
    - "specs-refiniment/003-context-guard-product-goal/research.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-user-story-decomposition"
    - "user-stories"
    - "review"
    - "story-refinement"
    - "scenario-covered"
    - "policy-resolved"
    - "policy-blocker"
---

# user-stories.md

## Feature Summary
- Context Guard is a local MVP for active Claude Code and Codex developers. It aims to reduce avoidable pre-work cache tokens by at least 30% per provider while preserving complete required and safety instructions, quality, privacy-safe evidence, and developer control.
- DEC-022 accepts the six-epic, 12-feature, 24-story backlog. This artifact expands those stories into testable acceptance logic, primary and negative scenarios, dependencies, risks, and readiness.
- No story or criterion claims that provider adapters, the runner, pilots, or effectiveness already exist.

## Actors and Stakeholders
- Developer: preflights and starts sessions, receives classifications, inspects evidence, bypasses optimization, and restores full-load state.
- Repository maintainer: owns local versioned relevance policy and actionable validation feedback.
- Engineering: owns provider adapters, deterministic evaluation, state leases, storage, recovery, counters, and performance instrumentation.
- QA: owns frozen fixtures, oracles, hard gates, invalidation, pairing, aggregation, and qualification evidence.
- Security/Privacy: owns receipt governance and forbidden-content validation. Product and Delivery own metrics, sequence, claims, and rollout decisions.
- Claude Code and Codex are external, versioned host boundaries rather than product actors.

## Scope and Boundaries
- Stories cover only supported Claude non-plugin startup overrides and supported Codex CLI/app-server pre-thread state, with actual-state verification and restoration.
- The combined customer MVP requires independent qualification of both providers; provider pilots can occur sequentially under DEC-019.
- Excluded: skill rewriting or summarization, semantic model relevance, compact skill index as product, remote content collection, mid-session interception, enterprise administration, Claude plugin optimization, repository-local Codex filtering, and unqualified IDE/desktop parity.
- Architecture, estimates, implementation commitment, release approval, and effectiveness claims remain outside this story-decomposition stage.

## Workflows and Failure Paths
- Primary: preflight, inventory, validate policy, classify, create baseline snapshot/lease, apply supported state, verify actual state, start fresh session, execute fixture, pass quality gates, measure, persist sanitized evidence, and restore.
- Alternate: developer bypasses optimization or explicitly invokes a skill; full authoritative content is available.
- Negative: missing, stale, duplicate, conflicting, unsupported, or ambiguous evidence yields `uncertain`, full load, and no optimization credit.
- Failure/retry: contention uses full load; abandoned leases use ownership/liveness recovery; compare-and-swap restoration preserves user edits; unsafe recovery disables optimization and offers one action.
- Evidence is invalidated by quality, privacy, correlation, counter, schema, performance, recovery, or paired-input failure.

## Requirements and Business Rules
- BR-101 through BR-112 and BR-201 through BR-212 govern the stories. Fixed precedence is safety-critical, mandatory/required, policy-required, exact policy-irrelevant, then uncertain.
- Only explicit irrelevant may reduce visibility. Explicitly invoked, required, safety-critical, uncertain, or otherwise mandatory skills retain complete authoritative content.
- Token size, historic usage, and model-generated semantic judgment cannot decide irrelevance.
- Quality precedes savings. Negative results and invalid attempts remain visible; valid providers are never pooled.
- DEC-024 resolves POL-401 and makes S-103 contract-ready: version-2 layered YAML, existing user/repository locations, deterministic `skills.rules`, exact identity for `irrelevant`, rule-id layering, actionable diagnostics, v1 compatibility, future-version rejection, and explicit atomic migration.

## Data, Integrations, and Non-Functional Requirements
- Local receipts use an application-owned user-only location equivalent to 0700/0600, atomic writes, schema/version validation, 30-day retention, inspect/delete, completed-unreferenced pruning, corruption quarantine, and single-writer semantics.
- Allowed receipt evidence is limited to versions, identifiers, fingerprints, digests, reason codes, classifications, requested/actual actions, fallback reasons, quality/measurement references, and timestamps. Prompts, responses, source, credentials, secrets, and full skill bodies are forbidden.
- Provider adapters are capability/version gated and must verify actual state before model work.
- Added local overhead must meet p95 <=750 ms and maximum <=2 s excluding network/model time; happy path has zero extra prompts and unsafe recovery allows at most one actionable prompt.

## Dependencies, Risks, and Constraints
- DEC-019 controls sequence: shared relevance/receipt foundation, Claude vertical, quality runner, Claude pilot, Codex vertical/pilot, then combined gate.
- Qualification depends on installed/version-pinned providers, local usage schemas, Python 3.10+, frozen repository/task/model inputs, and fresh-session warm-cache pairing.
- Risks: provider drift, missing required content, configuration loss, receipt leakage, ambiguous event correlation, counter misattribution, variance, overhead, and overclaiming one-repository results.
- POL-401 is resolved by DEC-024. EVID-401 is represented in stories S-201 through S-604. CONS-401 must close before S-603 delivery handoff.

## Decisions, Assumptions, and Open Questions
- Accepted authority: DEC-002 through DEC-006, DEC-009 through DEC-014, and DEC-016 through DEC-022. DEC-001, DEC-007, DEC-008, and DEC-015 are superseded.
- Assumption: each accepted backlog story remains one actor/outcome story; technical work stays in linked tasks rather than becoming actorless stories.
- Accepted policy decision: DEC-024 supplies the exact S-103 contract and closes POL-401.
- Open evidence questions: Codex exact-event availability, IDE/desktop parity, live eligibility/variance, causal skill contribution, and broader-repository generalization. These affect evidence or later scope, not the current story split.

## Success Measures
- Per provider: five valid pairs for each of three frozen fixtures; median normalized reduction >=30%; nearest-rank Q1 >=0%; every fixture median >=0%; no provider pooling or outlier deletion.
- Quality: zero hard-gate failures, full required/safety instruction preservation, valid completion oracles, and successful bypass/fallback/rollback.
- Evidence: every credited run is preflighted, provider-isolated, reproducible from sanitized receipts, and free of prohibited content.
- Net value: DEC-018 latency and prompt limits pass. Claims remain provider/version/repository/fixture bounded.
- Story readiness is measured by actor, outcome, acceptance criteria, scenarios, dependencies, priority, MVP status, and unresolved-rule visibility.

## Source Coverage
- `specs-refiniment/003-context-guard-product-goal/backlog.md`: accepted 12-feature/24-story decomposition, acceptance summaries, tasks, and readiness notes.
- `specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md`: zero-blocker planning gate, resolved POL-401, and EVID-401/CONS-401 controls.
- `specs-refiniment/003-context-guard-product-goal/goal-capability-map.md`: goals, capabilities, epics, actors, dependencies, and outcome traceability.
- `specs-refiniment/003-context-guard-product-goal/business-context.md`: actors, permissions, workflows, rules, and AC-201 through AC-210.
- `specs-refiniment/003-context-guard-product-goal/qa.md`: fixtures, oracles, hard gates, invalidation, and regression targets.
- `specs-refiniment/003-context-guard-product-goal/qa-strategy.md`: measurement adapters, windows, pairing, aggregation, receipt, and replay rules.
- `specs-refiniment/003-context-guard-product-goal/decision-log.md`: current authority and supersession through DEC-024.
- `specs-refiniment/003-context-guard-product-goal/research.md`: provider surfaces, version evidence, limitations, and open questions.
- `specs-refiniment/003-context-guard-product-goal/prfaq.md`: value, BR-101 through BR-112, rollout, and launch risks.
- `specs-refiniment/003-context-guard-product-goal/discovery.md`: customer problem, MVP, metrics, constraints, and exclusions.
- `specs-refiniment/003-context-guard-product-goal/change-impact.md`: DEC-016 through DEC-020 focused impact evidence.
- `specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md`: original delivery gaps and resolved definition evidence.
- `specs-refiniment/003-context-guard-product-goal/requirements-readiness.md`: earlier readiness dimensions and controlled follow-up.

## Story Detail Matrix
| Story ID | Epic ID | Actor | Story | Value | Priority | MVP | Dependencies | Risks | Open Questions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S-101 | EPIC-001 | Developer | As a developer, I want guarded startup to preflight the provider and client version so that unsupported controls cannot alter my session. | Safe eligibility | P0 / Slice 1 | Yes | DEC-012 | Provider drift | None |
| S-102 | EPIC-001 | Engineering | As Engineering, I want authoritative skill identities and digests so that relevance decisions are reproducible. | Trustworthy inventory | P0 / Slice 1 | Yes | S-101 | Duplicate or unstable identity | Host contract evidence |
| S-103 | EPIC-001 | Repository maintainer | As a maintainer, I want a versioned local policy with actionable validation so that relevance rules are controlled and repairable. | Safe policy ownership | P0 / Slice 1 | Yes | S-102; DEC-024 | Policy implementation defects | None at contract level |
| S-104 | EPIC-001 | Developer | As a developer, I want deterministic per-skill classifications with reason codes so that I can trust why content is retained or omitted. | Explainable conservative relevance | P0 / Slice 1 | Yes | S-103; DEC-009 | Incorrect precedence | None after S-103 |
| S-201 | EPIC-002 | Developer | As a Claude user, I want a verified fresh guarded session so that eligible irrelevant non-plugin skills do not enter startup context. | Claude cache reduction | P0 / Slice 2 | Yes | S-104; S-301 | Claude surface drift | Live qualification |
| S-202 | EPIC-002 | Developer | As a Claude user, I want bypass, fallback, and non-destructive restore so that I retain control when guarded behavior is unsafe. | Safety and recovery | P0 / Slice 2 | Yes | S-201; DEC-017 | Restore conflict | None |
| S-203 | EPIC-002 | Developer | As a Codex user, I want a verified guarded CLI or qualified app-server session so that eligible irrelevant skills do not enter startup context. | Codex cache reduction | P0 / Slice 5 | Yes | S-104; S-301 | Codex schema drift | IDE parity excluded unless qualified |
| S-204 | EPIC-002 | Developer | As a developer, I want contention, abandoned state, and user edits handled safely so that guarded sessions cannot corrupt my profile. | Configuration safety | P0 / Slice 5 | Yes | DEC-017 | Liveness error | None |
| S-301 | EPIC-003 | QA | As QA, I want an atomic schema-valid receipt for every attempted decision and measurement so that evidence can be replayed. | Auditable evidence | P0 / Slice 1 | Yes | DEC-016 | Partial/corrupt writes | None |
| S-302 | EPIC-003 | Security/Privacy | As Security/Privacy, I want receipts proven free of prohibited content so that local evidence does not leak sensitive material. | Privacy | P0 / Slice 1 | Yes | S-301 | Hidden content channel | None |
| S-303 | EPIC-003 | Developer | As a developer, I want to inspect and delete local receipts so that I control retained evidence. | User control | P0 / Slice 1 | Yes | S-301 | Wrong-target deletion | None |
| S-304 | EPIC-003 | Engineering | As Engineering, I want retention, safe pruning, locking, and quarantine so that receipt storage stays reliable and bounded. | Durable bounded storage | P0 / Slice 1 | Yes | S-301; DEC-016 | Race or referenced-data loss | None |
| S-401 | EPIC-004 | QA | As QA, I want to execute three frozen fixtures in fresh paired sessions so that baseline and guarded behavior are comparable. | Comparable evaluation | P0 / Slice 3 | Yes | Provider vertical; S-301 | Environment nondeterminism | Python 3.10+ |
| S-402 | EPIC-004 | QA | As QA, I want machine completion and instruction-preservation oracles so that task or rule loss is detected. | Quality evidence | P0 / Slice 3 | Yes | S-401 | False oracle equivalence | None |
| S-403 | EPIC-004 | QA | As QA, I want hard gates to block token evaluation until both pair members pass so that savings never mask quality failure. | Quality-first measurement | P0 / Slice 3 | Yes | S-402; DEC-010 | Gate bypass | None |
| S-404 | EPIC-004 | QA | As QA, I want invalid runs retained with reason codes but excluded from aggregation so that evidence is honest and diagnosable. | Evidence integrity | P0 / Slice 3 | Yes | S-403; S-301 | Misclassified invalidity | None |
| S-501 | EPIC-005 | QA | As QA, I want a validated Claude cache window so that cache creation plus read tokens are reproducible. | Claude measurement | P0 / Slice 4 | Yes | S-403; S-301 | Duplicate usage events | Live schema |
| S-502 | EPIC-005 | QA | As QA, I want a validated Codex cached-input window so that exact events or cumulative deltas are reproducible. | Codex measurement | P0 / Slice 5 | Yes | S-403; S-301 | Missing exact event | Adapter may return unmeasurable |
| S-503 | EPIC-005 | QA | As QA, I want alternating warm-cache pairs with no outlier deletion so that ordering and selection bias are bounded. | Fair paired evidence | P0 / Slices 4-5 | Yes | S-501 or S-502 | Cache eviction/variance | Eligibility dry run |
| S-504 | EPIC-005 | Product | As Product, I want provider-separated distributions and causal bounds so that I can judge the 30% target without overclaiming. | Defensible value decision | P0 / Slices 4-5 | Yes | S-503; DEC-011 | Causal over-attribution | Live result unknown |
| S-601 | EPIC-006 | Engineering | As Engineering, I want local overhead and prompts measured separately from provider time so that developer cost is accurate. | Net-value evidence | P0 / Slice 6 | Yes | Provider verticals | Instrumentation bias | None |
| S-602 | EPIC-006 | Product | As Product, I want net-value breaches to fail claims and preserve full load so that negative-value optimization is not shipped. | Safe value gate | P0 / Slice 6 | Yes | S-601; DEC-018 | Gate override | None |
| S-603 | EPIC-006 | Delivery | As Delivery, I want a bounded reproducible evidence package so that governance can review quality, privacy, recovery, measurement, and performance. | Auditable rollout | P0 / Slice 6 | Yes | S-404; S-504; S-602; CONS-401 | Stale authority | Cleanup required |
| S-604 | EPIC-006 | Product | As Product, I want explicit per-provider and combined decisions so that rollout and claims match qualified evidence. | Controlled launch | P0 gate / Slice 6 | Yes | S-603 | Combined overclaim | Both providers required |

## Acceptance Criteria Matrix
| AC ID | Story ID | Given | When | Then | Rule Covered |
| --- | --- | --- | --- | --- | --- |
| AC-S101-1 | S-101 | A configured client | Preflight runs | Provider, version, surface, and supported controls are recorded | DEC-012 |
| AC-S101-2 | S-101 | Unsupported or ambiguous capability | Guarded startup is requested | No mutation occurs; full load and reason receipt result | BR-108 |
| AC-S102-1 | S-102 | A supported host | Inventory is read twice unchanged | Stable identities and metadata/body digests match | BR-201 |
| AC-S102-2 | S-102 | Missing, duplicate, or stale identity | Inventory resolves | Result is unsupported/uncertain and earns no credit | BR-206 |
| AC-S103-1 | S-103 | A policy at the built-in, user, or repository layer | Maintainer validates version 2 | Unique `skills.rules` fields, exact identity, paths, precedence, and actionable file/field/code/remediation diagnostics follow DEC-024 | DEC-024; POL-401 |
| AC-S103-2 | S-103 | A v1, conflicting, duplicate-id, disabled, or future-version policy | Validation or migration runs | v1 loads as empty relevance without rewrite; same-id layering and disable rules apply; duplicates/future versions fail; explicit migration backs up and atomically replaces | DEC-024; POL-401 |
| AC-S104-1 | S-104 | Same task, inventory, and policy fingerprints | Classification repeats | Per-skill outcome and reason codes are identical | BR-209 |
| AC-S104-2 | S-104 | Safety, required, explicit invocation, conflict, or uncertainty | Decision evaluates | Complete authoritative content remains available; only exact irrelevant may reduce visibility | DEC-009 |
| AC-S201-1 | S-201 | Supported Claude non-plugin inventory | Guarded profile applies | Only explicit irrelevant skills request `user-invocable-only` and actual state matches | DEC-012 |
| AC-S201-2 | S-201 | Requested/actual Claude mismatch | Verification runs before model work | Session uses full load, failure is receipted, and no savings credit is allowed | BR-208 |
| AC-S202-1 | S-202 | Baseline snapshot and digest | Bypass or normal restore runs | Baseline returns idempotently without unrelated changes | DEC-017 |
| AC-S202-2 | S-202 | User edits after snapshot | Restore runs | Compare-and-swap refuses overwrite, disables optimization, and offers at most one recovery action | DEC-017 |
| AC-S203-1 | S-203 | Supported Codex CLI/app-server | Guarded startup applies | Absolute-path or pre-thread state is verified before model work | DEC-012 |
| AC-S203-2 | S-203 | Unsupported client/surface or state mismatch | Guarded startup runs | Full load is preserved and scope/failure is receipted | BR-108 |
| AC-S204-1 | S-204 | Existing provider/profile lease | Another guarded run starts | Second run does not mutate and uses full load | DEC-017 |
| AC-S204-2 | S-204 | Abandoned lease with ownership/liveness evidence | Recovery runs | Restore is idempotent; user edits are not overwritten | DEC-017 |
| AC-S301-1 | S-301 | Any guarded attempt | Decision or measurement terminates | One atomic, schema-valid receipt captures allowed outcome evidence | DEC-016 |
| AC-S301-2 | S-301 | Write interruption or invalid schema | Receipt commit is attempted | Partial data is not accepted; failure is safe and diagnosable | DEC-016 |
| AC-S302-1 | S-302 | Generated receipt corpus | Forbidden-content scan runs | No prompt, response, source, credential, secret, or full skill body is present | BR-212 |
| AC-S302-2 | S-302 | Sanitized receipts | Replay runs | Decisions and report references reproduce without raw content | BR-211 |
| AC-S303-1 | S-303 | Existing local receipts | Inspect command targets a run | Only permitted metadata is displayed locally | DEC-016 |
| AC-S303-2 | S-303 | Explicit receipt target | Delete command succeeds | Target is removed, unrelated receipts remain, and no remote copy exists | DEC-016 |
| AC-S304-1 | S-304 | Aged completed unreferenced and referenced receipts | Maintenance runs | 30-day policy prunes only eligible unreferenced data | DEC-016 |
| AC-S304-2 | S-304 | Corrupt receipt or concurrent writer | Access occurs | Corrupt data is quarantined and single-writer behavior prevents race corruption | DEC-016 |
| AC-S401-1 | S-401 | Frozen repo/task/model/fixture manifest | Runner executes | All three fixtures use fresh sessions and correlated baseline/guarded attempts | DEC-010 |
| AC-S401-2 | S-401 | Input or environment fingerprint mismatch | Pair begins | Pair is invalidated before aggregation and mismatch is retained | DEC-011 |
| AC-S402-1 | S-402 | Fixture outputs | Machine oracles run | Completion and instruction-preservation results are explicit | QG-301 through QG-307 |
| AC-S402-2 | S-402 | Explicit AI-SDLC skill fixture | Oracle evaluates | Complete authoritative skill instructions are loaded and followed | DEC-010 |
| AC-S403-1 | S-403 | Both pair members pass QG-301 through QG-309 | Token evaluation is requested | Measurement access is allowed | DEC-010 |
| AC-S403-2 | S-403 | Any hard-gate failure | Token evaluation is requested | Access is denied; pair and claim are invalid | QG-301 through QG-309 |
| AC-S404-1 | S-404 | Mismatch, privacy leak, recovery failure, or ambiguous correlation | QA invalidates | Attempt and reason remain; result cannot enter valid-pair aggregation | DEC-010 |
| AC-S404-2 | S-404 | Invalid attempts reduce count | Pilot continues | Additional attempts run until required valid pairs or explicit stop; invalids are not erased | DEC-011 |
| AC-S501-1 | S-501 | Version-pinned Claude events and correlation | Adapter extracts primary window | Deduplicated cache creation plus cache read total is reproducible | DEC-011 |
| AC-S501-2 | S-501 | Duplicate/drifted/uncorrelated Claude events | Adapter evaluates | Run is unmeasurable or invalid, never inferred | DEC-011 |
| AC-S502-1 | S-502 | Exact Codex event or validated cumulative totals | Adapter extracts | Per-completion cached-input value/delta is reproducible | DEC-011 |
| AC-S502-2 | S-502 | No valid event or delta boundary | Adapter evaluates | Run is unmeasurable; zero is not substituted | DEC-011 |
| AC-S503-1 | S-503 | Eligible provider/fixture | Pair scheduler runs | Five valid alternating warm-cache pairs complete per fixture/provider | DEC-011 |
| AC-S503-2 | S-503 | Negative or extreme valid result | Ledger and aggregation run | Result remains; no outlier deletion occurs | DEC-011 |
| AC-S504-1 | S-504 | Valid pair ledger | Aggregation runs | Unrounded reductions, nearest-rank quartiles, fixture medians, and provider median are reported | DEC-011 |
| AC-S504-2 | S-504 | Provider result | Gate evaluates | Pass requires median >=30%, Q1 >=0%, every fixture median >=0%, and quality pass | DEC-003; DEC-011 |
| AC-S601-1 | S-601 | Qualifying guarded runs | Timing and prompt instrumentation runs | Local time excludes provider network/model time and emits p95/max/prompt counts | DEC-018 |
| AC-S601-2 | S-601 | Happy and recovery paths | Interaction is observed | Happy path adds zero prompts; unsafe recovery adds at most one actionable prompt | DEC-018 |
| AC-S602-1 | S-602 | p95 >750 ms, any run >2 s, or prompt breach | Net-value gate runs | Affected surface fails claim and full load remains available | DEC-018 |
| AC-S602-2 | S-602 | Thresholds pass | Gate runs | Net-value may pass but does not override quality/privacy/evidence failures | BR-110; BR-111 |
| AC-S603-1 | S-603 | Completed qualification outputs | Evidence package generates | Quality, privacy, recovery, measurement, performance, versions, scope, failures, and replay refs are present | DEC-006 |
| AC-S603-2 | S-603 | Stale contradiction or missing authority | Handoff review runs | Package is not ready until CONS-401 is closed or explicitly reconciled | CONS-401 |
| AC-S604-1 | S-604 | Complete provider package | Product/Delivery decide | Claude and Codex each receive accepted, revised, or rejected status with rationale | DEC-006 |
| AC-S604-2 | S-604 | Combined MVP is considered | Gate runs | Combined claim passes only when both providers independently meet all gates | DEC-003 |

## Scenario Coverage Matrix
| Scenario ID | Story ID | Type | Trigger | Expected Outcome | AC Ref |
| --- | --- | --- | --- | --- | --- |
| SC-S101-P | S-101 | Primary | Supported client starts | Capability/version receipt permits guarded evaluation | AC-S101-1 |
| SC-S101-N | S-101 | Boundary | Unknown version starts | Full load; no mutation or credit | AC-S101-2 |
| SC-S102-P | S-102 | Primary | Stable host inventory read | Stable identities/digests returned | AC-S102-1 |
| SC-S102-N | S-102 | Negative | Duplicate or missing identity | Unsupported/uncertain | AC-S102-2 |
| SC-S103-P | S-103 | Primary | Valid accepted policy | Validation succeeds | AC-S103-1 |
| SC-S103-N | S-103 | Negative | Invalid/conflicting/old policy | Actionable error or accepted migration; no silent weakening | AC-S103-1; AC-S103-2 |
| SC-S104-P | S-104 | Primary | Exact irrelevant rule | Deterministic irrelevant with reason | AC-S104-1 |
| SC-S104-N | S-104 | Boundary | Conflict or uncertainty | Full content retained | AC-S104-2 |
| SC-S201-P | S-201 | Primary | Supported Claude profile | Eligible override verified before fresh session | AC-S201-1 |
| SC-S201-N | S-201 | Failure/retry | Claude state mismatch | Full-load fallback and receipt | AC-S201-2 |
| SC-S202-P | S-202 | Alternate | Developer bypasses | Baseline restored | AC-S202-1 |
| SC-S202-N | S-202 | Failure/retry | User edits baseline | CAS preserves edit and offers recovery | AC-S202-2 |
| SC-S203-P | S-203 | Primary | Supported Codex surface | State verified before thread/session | AC-S203-1 |
| SC-S203-N | S-203 | Boundary | Unqualified IDE/surface | Full load and scoped reason | AC-S203-2 |
| SC-S204-P | S-204 | Negative | Concurrent lease | Second run uses full load | AC-S204-1 |
| SC-S204-R | S-204 | Failure/retry | Process dies with lease | Liveness recovery restores safely | AC-S204-2 |
| SC-S301-P | S-301 | Primary | Guarded attempt ends | Atomic valid receipt exists | AC-S301-1 |
| SC-S301-N | S-301 | Failure/retry | Write interrupted | Partial receipt rejected | AC-S301-2 |
| SC-S302-P | S-302 | Primary | Privacy scan/replay | Clean and reproducible evidence | AC-S302-1; AC-S302-2 |
| SC-S302-N | S-302 | Negative | Forbidden field detected | Evidence invalidated | AC-S302-1 |
| SC-S303-P | S-303 | Primary | User inspects run | Allowed local metadata shown | AC-S303-1 |
| SC-S303-A | S-303 | Alternate | User deletes target | Only target removed | AC-S303-2 |
| SC-S304-P | S-304 | Primary | Retention maintenance | Eligible old receipts pruned | AC-S304-1 |
| SC-S304-N | S-304 | Boundary | Receipt referenced/active/corrupt | Retained or quarantined appropriately | AC-S304-1; AC-S304-2 |
| SC-S401-P | S-401 | Primary | Frozen suite runs | Three correlated fresh-session fixtures execute | AC-S401-1 |
| SC-S401-N | S-401 | Negative | Fingerprint mismatch | Pair invalidated | AC-S401-2 |
| SC-S402-P | S-402 | Primary | Valid fixture output | Oracles pass explicitly | AC-S402-1 |
| SC-S402-N | S-402 | Negative | Required instruction missing | Hard failure | AC-S402-2 |
| SC-S403-P | S-403 | Primary | Both members pass gates | Tokens become evaluable | AC-S403-1 |
| SC-S403-N | S-403 | Negative | Any gate fails | Token evaluation blocked | AC-S403-2 |
| SC-S404-P | S-404 | Negative | QA detects invalidity | Attempt retained/excluded with reason | AC-S404-1 |
| SC-S404-R | S-404 | Failure/retry | Valid pair count short | Additional attempt allowed; invalid remains | AC-S404-2 |
| SC-S501-P | S-501 | Primary | Valid Claude events | Deduplicated cache sum emitted | AC-S501-1 |
| SC-S501-N | S-501 | Boundary | Event drift/duplication | Unmeasurable or invalid | AC-S501-2 |
| SC-S502-P | S-502 | Primary | Valid Codex event/delta | Cached input emitted | AC-S502-1 |
| SC-S502-N | S-502 | Boundary | Missing boundary | Unmeasurable, not zero | AC-S502-2 |
| SC-S503-P | S-503 | Primary | Eligible fixture/provider | Five alternating valid pairs complete | AC-S503-1 |
| SC-S503-N | S-503 | Negative | Valid negative/extreme result | Result retained | AC-S503-2 |
| SC-S504-P | S-504 | Primary | Valid ledger aggregated | Full provider-separated distribution reported | AC-S504-1 |
| SC-S504-N | S-504 | Boundary | One statistical gate fails | Provider target fails | AC-S504-2 |
| SC-S601-P | S-601 | Primary | Guarded runs instrumented | Local p95/max/prompts reproducible | AC-S601-1 |
| SC-S601-N | S-601 | Boundary | Network/model latency present | Excluded from local overhead | AC-S601-1 |
| SC-S602-P | S-602 | Primary | All net-value limits pass | Net-value gate may pass | AC-S602-2 |
| SC-S602-N | S-602 | Negative | Any limit breached | Claim fails and full load remains | AC-S602-1 |
| SC-S603-P | S-603 | Primary | Complete evidence available | Bounded replayable package generated | AC-S603-1 |
| SC-S603-N | S-603 | Negative | CONS-401 or evidence gap remains | Handoff not ready | AC-S603-2 |
| SC-S604-P | S-604 | Primary | Both providers qualify | Combined MVP may be accepted | AC-S604-1; AC-S604-2 |
| SC-S604-N | S-604 | Alternate | One provider fails or evidence is weak | Provider/combined rollout revised or rejected | AC-S604-1; AC-S604-2 |

## Story Dependencies and Risks
- S-101 -> S-102 -> S-103 -> S-104 is the relevance foundation. DEC-024 closes POL-401; S-103 is ready for implementation refinement under the accepted contract.
- S-301/S-302 form the minimum receipt foundation before S-201 or S-203. S-303/S-304 complete lifecycle operations.
- Claude path: S-201/S-202 -> S-401 through S-404 -> S-501 -> S-503/S-504. Codex path substitutes S-203/S-204 and S-502.
- S-601/S-602 depend on provider verticals; S-603 depends on quality, evidence, net-value, and CONS-401; S-604 depends on complete provider packages.
- Highest risks: S-104 instruction loss, S-202/S-204 configuration loss, S-302 privacy leakage, S-403 quality-gate bypass, S-501/S-502 counter drift, S-504 causal overclaim, and S-604 combined overclaim.
- Risk controls are encoded in negative/boundary scenarios and full-load or invalidation outcomes.

## Story Readiness
| Story Set | Readiness | Missing Information | Impact / Blocking Scope | Owner / Resolution or Next Action |
| --- | --- | --- | --- | --- | --- |
| S-101, S-102 | Ready for downstream refinement | Live provider evidence remains delivery work | No story-definition blocker | Engineering validates adapter contracts |
| S-103 | Ready for downstream refinement | No missing product rule; implementation evidence remains | No story-definition blocker | Engineering + QA implement and validate DEC-024/T-001 |
| S-104 | Ready with implementation dependency | S-103 implementation | Cannot implement before S-103, but contract and acceptance behavior are defined | Engineering implements S-103 first |
| S-201 through S-204 | Ready for downstream refinement | Live provider qualification | Evidence/release only | Engineering + QA execute qualification |
| S-301 through S-304 | Ready for downstream refinement | Implementation evidence | Evidence/release only | Engineering + Security/Privacy implement and review |
| S-401 through S-404 | Ready for downstream refinement | Runner and executed fixtures | Evidence/release only | QA + Engineering build and execute runner |
| S-501 through S-504 | Ready with evidence dependency | Provider counters, eligibility, variance, causal results | Effectiveness claim only | QA + Engineering + Product execute pilots and evaluate |
| S-601 through S-604 | Ready with gate dependencies | Qualification package and CONS-401 cleanup | Rollout/release only | Product + Delivery + QA close evidence and consistency gates |

- All 24 stories have a concrete actor, value, priority, MVP status, dependencies, at least two testable acceptance criteria, and primary plus negative/boundary coverage.
- Story decomposition is complete and DEC-024 removes the POL-401 release-slicing blocker. Downstream slicing may not treat EVID-401 as completed evidence.
- Accepted DEC-023 adopts the story set; accepted DEC-024 closes the former S-103 readiness exception.
