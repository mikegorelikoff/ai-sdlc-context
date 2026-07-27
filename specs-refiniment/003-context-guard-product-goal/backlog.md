---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "backlog.md"
  path: "specs-refiniment/003-context-guard-product-goal/backlog.md"
  workspace: "refinement"
  skill: "ai-sdlc-backlog-decomposition-and-task-planning"
  flow_mode: "full"
  state_file: "specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  status: "review"
  owner: "Product and Delivery"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "BR-101"
    - "BR-112"
    - "BR-201"
    - "BR-211"
    - "BR-212"
    - "CAP-001"
    - "CAP-002"
    - "CAP-009"
    - "DEC-001"
    - "DEC-002"
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
    - "DEC-021"
    - "DEC-022"
    - "DEC-023"
    - "DEC-024"
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "EPIC-004"
    - "EPIC-005"
    - "EPIC-006"
    - "GOAL-001"
    - "GOAL-002"
    - "GOAL-003"
    - "GOAL-004"
    - "RISK-003"
  related_artifacts:
    - "specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md"
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
    - "ai-sdlc-backlog-decomposition-and-task-planning"
    - "backlog"
    - "review"
    - "decomposition-ready"
    - "mvp-backlog"
    - "policy-resolved"
    - "proposed-decision"
---

# backlog.md

## Feature Summary
- Context Guard is an MVP for developers who actively use Claude Code and Codex. It reduces avoidable provider-reported cache tokens before productive work without losing required or safety-critical instructions, local evidence, or developer control.
- This backlog decomposes six accepted epics into 12 feature outcomes, 24 actor-centered stories, 24 acceptance summaries, and explicit technical, QA, operations, privacy, analytics, and product tasks.
- DEC-019 controls sequence; DEC-021 authorizes this decomposition with zero planning blockers. The backlog represents intended work, not implemented capability or proven savings.

## Actors and Stakeholders
- Developer: declares work, starts guarded sessions, explicitly invokes skills, inspects receipts, bypasses optimization, and restores full-load behavior.
- Repository maintainer: authors versioned local relevance policy without rewriting authoritative skills or weakening mandatory and safety rules.
- Product and Delivery: own value, scope, sequencing, rollout, and claims.
- Engineering: owns provider preflight, deterministic evaluation, profile coordination, receipts, measurement adapters, and recovery.
- QA: owns fixtures, hard quality gates, run invalidation, paired evidence, and qualification signoff. Security/Privacy co-owns receipt governance.
- Claude Code and Codex are external versioned host boundaries. Enterprise administration and cross-developer monitoring are outside MVP.

## Scope and Boundaries
- In scope: local pre-session preflight, authoritative inventory, deterministic per-skill relevance, validated policy, supported provider startup controls, actual-state verification, fallback/bypass/rollback, governed local receipts, quality-first paired measurement, net-value evaluation, and provider-bounded rollout decisions.
- Claude scope: version-qualified non-plugin skills and startup `skillOverrides`. Codex scope: version-qualified CLI absolute-path `skills.config` and verified app-server user-level state before `thread/start`.
- Out of scope: skill rewriting or summarization, semantic model classification, compact skill index as the product, remote content collection, mid-session interception, enterprise policy administration, Claude plugin optimization, repository-local Codex filtering, and unqualified IDE/desktop compatibility.
- Claude may qualify first, but the customer-facing MVP requires independent Claude Code and Codex qualification.

## Workflows and Failure Paths
- Baseline and guarded runs share frozen task/model/repository inputs, fresh sessions, quality evaluation, provider-normalized measurement, and restoration.
- Guarded startup performs capability/version preflight, inventory, policy validation, deterministic classification, supported profile mutation, actual-state verification, execution, hard quality gates, measurement, receipt persistence, and restore.
- Missing, stale, conflicting, duplicate, unsupported, or ambiguous evidence becomes `uncertain`; full content remains visible and no savings credit is earned.
- Contention uses full-load fallback. Abandoned state is detected by ownership and liveness. Restoration is idempotent compare-and-swap and never overwrites user edits. Unsafe automatic recovery leaves optimization disabled and exposes one recovery action.
- Any quality, privacy, correlation, counter, receipt, performance, or recovery failure invalidates the affected evidence and claim.

## Requirements and Business Rules
- BR-101 through BR-112 and BR-201 through BR-212 are authoritative. Only an explicit `irrelevant` result may reduce visibility; required, safety-critical, uncertain, explicitly invoked, or otherwise mandatory skills retain complete authoritative content.
- Classification uses authoritative identity and fixed precedence; token size, historic usage, and model-generated semantic judgment cannot determine irrelevance.
- DEC-024 resolves POL-401: S-103 implements version-2 layered YAML using the existing user and repository policy paths, a deterministic `skills.rules` contract, exact identity for `irrelevant`, rule-id overrides, actionable diagnostics, v1 compatibility, future-version rejection, and explicit atomic migration.
- Quality is evaluated before savings. Providers are measured and claimed independently; invalid or negative results are retained and providers are never pooled.

## Data, Integrations, and Non-Functional Requirements
- Receipts are local and unsynchronized by default in an application-owned location with user-only access equivalent to 0700 directories and 0600 files, atomic per-run writes, explicit schema/version, 30-day retention, inspect/delete operations, completed-unreferenced pruning, corruption quarantine, and single-writer semantics.
- Receipts may contain versions, identifiers, fingerprints, digests, reason codes, classifications, requested/actual actions, fallback reasons, quality/measurement references, and timestamps. They must not contain raw prompts, responses, source, credentials, secrets, or full skill bodies.
- Added local overhead must have p95 at or below 750 ms and no qualifying run above 2 seconds, excluding provider network/model time. The happy path has zero extra prompts; unsafe recovery permits at most one actionable prompt.
- Integrations must be version/capability gated, verify actual state, preserve provider isolation, and fail safely to full load.

## Dependencies, Risks, and Constraints
- DEC-019 dependency order is mandatory: Gate 0 decisions; Slice 1 EPIC-001 plus minimum EPIC-003; Slice 2 Claude EPIC-002; Slice 3 EPIC-004; Slice 4 Claude EPIC-005; Slice 5 Codex EPIC-002/005; Slice 6 EPIC-006.
- External dependencies are provider behavior/configuration, local usage schemas, installed client versions, and the first repository pilot. Qualification requires Python 3.10+.
- Major risks are provider drift, required-instruction loss, configuration corruption, receipt leakage, counter misattribution, benchmark variance, overhead erasing value, and claims beyond one repository.
- EVID-401 is represented as build and qualification work. CONS-401 remains an owned documentation/authority cleanup before delivery handoff. POL-401 is resolved by DEC-024.

## Decisions, Assumptions, and Open Questions
- Accepted planning authority is DEC-002 through DEC-006, DEC-009 through DEC-014, and DEC-016 through DEC-024. DEC-001, DEC-007, DEC-008, and DEC-015 are superseded.
- Decomposition assumption: feature and story splits preserve accepted epic outcomes and DEC-019 order; they do not select an implementation architecture.
- Open work, not silent assumptions: Codex IDE/desktop parity, causal skill contribution, live adapter/runner/pilot evidence, and cleanup of stale upstream wording. Policy schema/location/migration are accepted in DEC-024.
- Accepted DEC-022 and DEC-023 establish the 12-feature/24-story decomposition and scenario set; DEC-024 closes the policy readiness exception.

## Success Measures
- GOAL-001: at least 30% median reduction in normalized guarded cache tokens independently per provider after five valid pairs for each of three fixtures, with Q1 and per-fixture medians at least zero.
- GOAL-002: zero hard failures and complete required/safety instruction preservation across valid pairs; bypass, fallback, and rollback succeed.
- GOAL-003: every credited run is version-preflighted, provider-isolated, receipted, reproducible, privacy-safe, and recoverable; unsupported states use full load.
- GOAL-004: DEC-018 latency and interruption limits pass and all claims remain provider/version/repository/fixture bounded.
- These are acceptance targets for planned work. No effectiveness result is claimed at this stage.

## Source Coverage
- `specs-refiniment/003-context-guard-product-goal/discovery.md`: customer, problem, MVP, metrics, constraints, risks, and exclusions.
- `specs-refiniment/003-context-guard-product-goal/prfaq.md`: value narrative, BR-101 through BR-112, rollout, and launch risks.
- `specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md`: original delivery gaps and definition-complete evidence.
- `specs-refiniment/003-context-guard-product-goal/requirements-readiness.md`: readiness dimensions and controlled follow-up.
- `specs-refiniment/003-context-guard-product-goal/goal-capability-map.md`: four goals, nine capabilities, six epics, actors, dependencies, and outcome links.
- `specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md`: zero-blocker gate, resolved POL-401, and retained EVID-401/CONS-401 notes.
- `specs-refiniment/003-context-guard-product-goal/user-stories.md`: accepted story details, acceptance criteria, scenarios, and DEC-024 readiness.
- `specs-refiniment/003-context-guard-product-goal/business-context.md`: detailed actors, permissions, workflows, rules, and acceptance criteria.
- `specs-refiniment/003-context-guard-product-goal/research.md`: provider surfaces, limitations, version evidence, and open questions.
- `specs-refiniment/003-context-guard-product-goal/qa.md`: fixtures, oracles, hard gates, invalidation, and regression targets.
- `specs-refiniment/003-context-guard-product-goal/qa-strategy.md`: adapters, measurement windows, pairing, aggregation, and privacy replay.
- `specs-refiniment/003-context-guard-product-goal/decision-log.md`: current authority and supersession through DEC-024.
- `specs-refiniment/003-context-guard-product-goal/change-impact.md`: strict DEC-024/POL-401/S-103 impact evidence.

## Epic Backlog
| Epic ID | Outcome | Actors | Priority | Dependencies |
| --- | --- | --- | --- | --- |
| EPIC-001 | Trustworthy provider-aware relevance decisions | Developer; maintainer; Engineering | P0 / Slice 1 | DEC-009; DEC-012; CAP-001; CAP-002; CAP-009 |
| EPIC-002 | Safe guarded session control and recovery | Developer; Engineering; hosts | P0 / Slices 2 and 5 | EPIC-001; EPIC-003; DEC-017 |
| EPIC-003 | Privacy-safe local evidence | Developer; QA; Security/Privacy; Engineering | P0 / Slice 1 foundation | DEC-016; BR-211; BR-212 |
| EPIC-004 | Quality-qualified behavior | QA; Engineering | P0 / Slice 3 | EPIC-002; EPIC-003; DEC-010 |
| EPIC-005 | Provider-specific cache-value validation | Product; QA; Engineering | P0 / Slices 4 and 5 | EPIC-003; EPIC-004; DEC-011 |
| EPIC-006 | Net-value and defensible rollout governance | Product; Delivery; QA; Engineering | P0 gate / Slice 6 | EPIC-004; EPIC-005; DEC-018 |

Feature decomposition:

| Feature ID | Epic ID | Feature Name | Description | User Role | Business Value | Priority | MVP / Post-MVP | Dependencies | Risks | Open Questions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-101 | EPIC-001 | Provider preflight and inventory | Qualify version/capability and enumerate authoritative skills | Developer | Prevent unsafe optimization on unsupported state | P0 | MVP | DEC-012 | Provider drift | None at backlog level |
| F-102 | EPIC-001 | Policy and relevance engine | Validate versioned policy and produce deterministic reasoned classifications | Maintainer | Make omission explicit, conservative, and reproducible | P0 | MVP | F-101; DEC-009; DEC-024 | Policy mistakes | None at contract level |
| F-201 | EPIC-002 | Claude guarded profile | Apply, verify, and restore supported Claude non-plugin overrides | Developer | Reduce eligible Claude startup context safely | P0 | MVP | F-101; F-102; F-301 | Client drift | Live qualification |
| F-202 | EPIC-002 | Codex guarded profile and recovery | Apply verified Codex startup state with lease-safe recovery | Developer | Reduce eligible Codex startup context without corrupting state | P0 | MVP | F-101; F-102; F-301; DEC-017 | App-server drift; user edits | IDE parity post-MVP unless qualified |
| F-301 | EPIC-003 | Receipt creation and privacy | Persist schema-valid sanitized evidence atomically | Developer; QA | Enable local audit and replay without sensitive content | P0 | MVP | DEC-016 | Leakage; partial writes | None |
| F-302 | EPIC-003 | Receipt lifecycle operations | Inspect, delete, retain, prune, lock, and quarantine receipts | Developer | Keep evidence controllable and bounded | P0 | MVP | F-301; DEC-016 | Accidental deletion; contention | None |
| F-401 | EPIC-004 | Frozen fixture runner | Execute three frozen fixtures with fresh-session controls and machine oracles | QA | Establish comparable task correctness | P0 | MVP | F-201 or F-202; F-301 | Nondeterminism | Runner implementation |
| F-402 | EPIC-004 | Quality gates and invalidation | Enforce QG-301 through QG-309 before measurement access | QA | Prevent savings from masking quality regressions | P0 | MVP | F-401 | False equivalence | Evidence execution |
| F-501 | EPIC-005 | Provider measurement adapters | Extract versioned Claude and Codex cache-token windows | QA; Engineering | Produce provider-valid normalized measures | P0 | MVP | F-301; F-402 | Counter/schema drift | Codex event availability |
| F-502 | EPIC-005 | Pairing, aggregation, and causal analysis | Run paired protocol and report distributions and contribution bounds | Product; QA | Determine whether each provider meets the 30% target | P0 | MVP | F-501 | Variance; over-attribution | Live pilot result |
| F-601 | EPIC-006 | Net-value gate | Measure local overhead and interruptions against DEC-018 | Product; Engineering | Ensure optimization is worthwhile | P0 | MVP | F-201; F-202; F-502 | Instrumentation bias | None |
| F-602 | EPIC-006 | Evidence and rollout decision | Produce bounded claim package and accept, revise, or reject rollout | Product; Delivery | Prevent unsupported effectiveness claims | P0 gate | MVP | F-402; F-502; F-601 | One-repository overclaim | Broader evidence post-MVP |

## Story Backlog
| Story ID | Epic Ref | Feature ID | Actor | Story | Business Value | Priority | MVP | Acceptance Summary | Dependencies | Assumptions / Open Questions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S-101 | EPIC-001 | F-101 | Developer | As a developer, I can preflight the provider and client version before guarded startup. | Avoid unsupported mutations | P0 / Slice 1 | Yes | AC-S101 | DEC-012 | Version support is explicit |
| S-102 | EPIC-001 | F-101 | Engineering | As Engineering, I can enumerate and fingerprint the authoritative skill inventory or return unsupported. | Make decisions reproducible | P0 / Slice 1 | Yes | AC-S102 | S-101 | Host identity contract |
| S-103 | EPIC-001 | F-102 | Repository maintainer | As a maintainer, I can author and validate a versioned local relevance policy with actionable errors. | Control relevance safely | P0 / Slice 1 | Yes | AC-S103 | S-102; DEC-024 | Version-2 contract accepted |
| S-104 | EPIC-001 | F-102 | Developer | As a developer, I receive deterministic per-skill classifications and reason codes with uncertainty retaining full content. | Trust guarded decisions | P0 / Slice 1 | Yes | AC-S104 | S-103; DEC-009 | No semantic classifier |
| S-201 | EPIC-002 | F-201 | Developer | As a Claude user, I can start a fresh guarded session whose requested and actual skill state are verified. | Reduce eligible Claude cache context | P0 / Slice 2 | Yes | AC-S201 | S-104; S-301 | Non-plugin scope only |
| S-202 | EPIC-002 | F-201 | Developer | As a Claude user, I can bypass, fall back, and restore the baseline without unrelated changes. | Preserve control and safety | P0 / Slice 2 | Yes | AC-S202 | S-201; DEC-017 | Live provider qualification |
| S-203 | EPIC-002 | F-202 | Developer | As a Codex user, I can start a fresh guarded CLI or qualified app-server session with verified state. | Reduce eligible Codex cache context | P0 / Slice 5 | Yes | AC-S203 | S-104; S-301 | Supported surfaces only |
| S-204 | EPIC-002 | F-202 | Developer | As a developer, concurrent, abandoned, or user-edited profile state fails safely and offers idempotent recovery. | Prevent configuration loss | P0 / Slice 5 | Yes | AC-S204 | DEC-017 | One provider/profile lease |
| S-301 | EPIC-003 | F-301 | QA | As QA, I receive an atomic schema-valid receipt for every attempted guarded decision and measurement. | Enable audit and replay | P0 / Slice 1 | Yes | AC-S301 | DEC-016 | Minimum receipt precedes provider verticals |
| S-302 | EPIC-003 | F-301 | Security/Privacy | As Security/Privacy, I can prove receipts exclude all prohibited content. | Prevent local evidence leakage | P0 / Slice 1 | Yes | AC-S302 | S-301 | Sanitized fixtures available |
| S-303 | EPIC-003 | F-302 | Developer | As a developer, I can inspect and explicitly delete my local receipts. | Preserve user control | P0 / Slice 1 | Yes | AC-S303 | S-301 | Local only |
| S-304 | EPIC-003 | F-302 | Engineering | As Engineering, I enforce retention, safe pruning, locking, and corruption quarantine. | Keep evidence reliable and bounded | P0 / Slice 1 | Yes | AC-S304 | S-301; DEC-016 | Completed unreferenced runs only |
| S-401 | EPIC-004 | F-401 | QA | As QA, I can run the three frozen fixtures with fixed inputs and fresh sessions. | Make guarded and baseline runs comparable | P0 / Slice 3 | Yes | AC-S401 | Provider vertical; S-301 | Python 3.10+ |
| S-402 | EPIC-004 | F-401 | QA | As QA, I can evaluate machine completion and instruction-preservation oracles. | Detect task or instruction loss | P0 / Slice 3 | Yes | AC-S402 | S-401 | Provider-neutral fixtures |
| S-403 | EPIC-004 | F-402 | QA | As QA, I block token evaluation until both pair members pass every hard gate. | Keep quality ahead of savings | P0 / Slice 3 | Yes | AC-S403 | S-402; DEC-010 | Zero hard-failure tolerance |
| S-404 | EPIC-004 | F-402 | QA | As QA, I can invalidate and explain runs with mismatch, privacy, recovery, or correlation failures. | Exclude misleading evidence | P0 / Slice 3 | Yes | AC-S404 | S-403; receipts | Invalid attempts retained |
| S-501 | EPIC-005 | F-501 | QA | As QA, I can derive Claude cache creation plus read tokens from a validated deduplicated window. | Measure Claude consistently | P0 / Slice 4 | Yes | AC-S501 | S-403; S-301 | Version-pinned adapter |
| S-502 | EPIC-005 | F-501 | QA | As QA, I can derive Codex cached input from exact events or a validated cumulative delta. | Measure Codex consistently | P0 / Slice 5 | Yes | AC-S502 | S-403; S-301 | Missing exact event may be unmeasurable |
| S-503 | EPIC-005 | F-502 | QA | As QA, I can execute alternating warm-cache baseline/guarded pairs without deleting outliers. | Reduce ordering and selection bias | P0 / Slices 4–5 | Yes | AC-S503 | S-501 or S-502 | Five valid pairs per fixture/provider |
| S-504 | EPIC-005 | F-502 | Product | As Product, I receive provider-separated distributions, causal bounds, and a pass/fail result. | Decide against the 30% goal honestly | P0 / Slices 4–5 | Yes | AC-S504 | S-503; DEC-011 | Providers never pooled |
| S-601 | EPIC-006 | F-601 | Engineering | As Engineering, I can measure added local startup overhead and developer prompts separately from provider time. | Quantify developer cost | P0 / Slice 6 | Yes | AC-S601 | Provider verticals | Instrumentation must not include network/model time |
| S-602 | EPIC-006 | F-601 | Product | As Product, I fail the net-value claim and preserve full load when DEC-018 limits are breached. | Avoid negative-value rollout | P0 / Slice 6 | Yes | AC-S602 | S-601; DEC-018 | No override inside qualifying evidence |
| S-603 | EPIC-006 | F-602 | Delivery | As Delivery, I receive a reproducible evidence package with provider, version, repository, fixture, privacy, quality, and performance bounds. | Support defensible governance | P0 / Slice 6 | Yes | AC-S603 | S-404; S-504; S-602 | CONS-401 cleanup required |
| S-604 | EPIC-006 | F-602 | Product | As Product, I can accept, revise, or reject each provider rollout and the combined MVP claim. | Prevent unsupported launch claims | P0 gate / Slice 6 | Yes | AC-S604 | S-603 | Both providers must qualify for combined claim |

## Acceptance Summary
| Story ID | Acceptance Criterion ID | Given | When | Then | Notes |
| --- | --- | --- | --- | --- | --- |
| S-101 | AC-S101 | A configured provider client | Preflight runs | Supported version/capabilities are recorded or guarded mode is disabled | Full-load fallback |
| S-102 | AC-S102 | A supported host | Inventory is read | Stable identities and digests are emitted; ambiguity is unsupported | Authoritative source only |
| S-103 | AC-S103 | A version-1 or version-2 layered YAML policy | Validation or migration runs | DEC-024 paths, `skills.rules`, exact identity, diagnostics, compatibility, and atomic migration behavior are enforced | DEC-024 closes POL-401 |
| S-104 | AC-S104 | Valid inventory, task, and policy | Classification runs repeatedly | Identical reasoned results occur; only explicit irrelevant may reduce visibility | Fixed precedence |
| S-201 | AC-S201 | Supported Claude and explicit irrelevant skills | Guarded startup runs | Only eligible non-plugin overrides are requested and actual state matches before model work | Fresh session |
| S-202 | AC-S202 | Any Claude control failure or bypass | Restoration runs | Baseline is restored without unrelated edits and failure earns no savings | Idempotent |
| S-203 | AC-S203 | Supported Codex CLI/app-server | Guarded startup runs | Absolute-path or verified pre-thread state is applied and receipted | Unsupported surfaces full load |
| S-204 | AC-S204 | Contention, abandoned lease, or changed baseline | Coordination/recovery runs | No unsafe mutation occurs; CAS preserves user edits; at most one recovery action is shown | DEC-017 |
| S-301 | AC-S301 | Any guarded attempt | A decision or measurement completes or fails | One atomic schema-valid local receipt captures allowed fields and outcome | User-only access |
| S-302 | AC-S302 | Generated receipts | Privacy scan and replay run | No prohibited content exists and decisions replay from sanitized evidence | Leak invalidates evidence |
| S-303 | AC-S303 | Existing receipts | User inspects or deletes by supported command | Selected metadata is shown or targeted receipts are removed without hidden remote copy | Explicit control |
| S-304 | AC-S304 | Aged, referenced, corrupt, or concurrent receipts | Lifecycle maintenance runs | 30-day policy, safe prune, single writer, and quarantine rules are honored | Referenced/active data retained |
| S-401 | AC-S401 | Frozen repository, task, model, and cache state | Runner executes | Three fixtures run in fresh paired sessions with correlations and receipts | No production sampling |
| S-402 | AC-S402 | Fixture outputs | Oracles evaluate | Completion and full required-instruction preservation yield machine results | Manual review bounded |
| S-403 | AC-S403 | A baseline/guarded pair | Measurement access is requested | Access is granted only when both members pass QG-301 through QG-309 | Quality first |
| S-404 | AC-S404 | A mismatched, leaked, failed, or ambiguous run | QA invalidates it | Reason is receipted, attempt retained, and it cannot support aggregation | QA authority |
| S-501 | AC-S501 | Version-pinned Claude usage events | Adapter extracts the window | Deduplicated cache creation plus read tokens and correlation are reproducible | Drift is unmeasurable |
| S-502 | AC-S502 | Version-pinned Codex events | Adapter extracts the window | Exact cached-input or validated cumulative delta is reproducible | No inferred substitute |
| S-503 | AC-S503 | Eligible fixtures and adapter | Pilot runs | Five valid alternating warm-cache pairs per fixture/provider complete; negative/outlier results remain | Invalid attempts do not count |
| S-504 | AC-S504 | Valid pair receipts | Aggregation runs | Unrounded reductions, nearest-rank quartiles, fixture medians, provider median, and causal caveat are reported separately | 30%/Q1/fixture gates |
| S-601 | AC-S601 | Qualifying guarded runs | Local timing and prompts are measured | Provider network/model time is excluded and p95/max/prompt counts are reproducible | DEC-018 |
| S-602 | AC-S602 | p95 above 750 ms, any run above 2 s, or prompt breach | Gate evaluates | Claim fails for that surface and full-load operation remains available | No savings override |
| S-603 | AC-S603 | Completed qualification evidence | Package is generated | It includes quality, privacy, recovery, measurement, net-value, versions, scope, failures, and reproducibility references | No universal claim |
| S-604 | AC-S604 | A complete provider package | Product/Delivery decide | Each provider is accepted/revised/rejected explicitly; combined MVP passes only if both independently qualify | Decision logged |

## Priorities and Dependencies
- Gate 0 is complete through DEC-021. Backlog work starts with Slice 1: F-101, F-102, and the minimum F-301/F-302 receipt foundation.
- Slice 2 delivers the Claude vertical F-201; Slice 3 adds F-401/F-402; Slice 4 adds Claude F-501/F-502 qualification.
- Slice 5 delivers and qualifies the Codex vertical F-202 plus Codex portions of F-501/F-502. Slice 6 completes F-601/F-602 and the combined gate.
- No story may bypass its provider preflight, receipt, quality, or restore dependency. Measurement stories cannot access token results before hard quality gates.
- DEC-024 closes the Slice 1 definition dependency for S-103. EVID-401 is embodied in S-201 through S-604 and related tasks. CONS-401 is required before S-603 delivery handoff.
- Estimation order should follow feature dependencies; release slicing remains a separate downstream decision.

## Cross-Functional Tasks
| Task ID | Owner | Output | Dependencies | Refs |
| --- | --- | --- | --- | --- |
| T-001 | Engineering + QA | Implement and validate the accepted version-2 layered policy, diagnostics, v1 compatibility, and atomic migration | DEC-024 | F-102; S-103; POL-401 resolved |
| T-002 | Engineering | Claude capability/inventory/profile adapter contract tests | T-001 | F-101; F-201; DEC-012 |
| T-003 | Engineering | Codex CLI/app-server capability/inventory/profile adapter contract tests | T-001 | F-101; F-202; DEC-012 |
| T-004 | Engineering | Provider/profile lease, snapshot, CAS restore, and crash-recovery tests | T-002; T-003 | S-202; S-204; DEC-017 |
| T-005 | Security/Privacy | Receipt schema threat review and forbidden-content fixture set | T-001 | F-301; DEC-016 |
| T-006 | Engineering | Atomic storage, access-mode, retention, pruning, quarantine, and delete implementation plan | T-005 | F-301; F-302 |
| T-007 | QA | Frozen repository snapshots, tasks, models, instruction oracles, and validity manifest | Provider vertical | F-401; DEC-010 |
| T-008 | QA + Engineering | Python 3.10+ runner with fresh-session, correlation, invalidation, and replay pipeline | T-007; T-006 | F-401; F-402; EVID-401 |
| T-009 | QA + Engineering | Claude usage-window fixtures and deduplication validator | T-008; T-002 | S-501; DEC-011 |
| T-010 | QA + Engineering | Codex exact-event/cumulative-delta fixtures and drift validator | T-008; T-003 | S-502; DEC-011 |
| T-011 | QA | Pair scheduler, attempt ledger, aggregation formulas, and reproducibility tests | T-009 or T-010 | S-503; S-504 |
| T-012 | Engineering | Local overhead and prompt instrumentation separated from provider time | Provider vertical | F-601; DEC-018 |
| T-013 | Analytics/Product | Provider-separated human and machine evidence report | T-011; T-012 | F-602; GOAL-001; GOAL-004 |
| T-014 | Delivery + Product | Provider and combined rollout decision template with claim bounds | T-013 | S-603; S-604 |
| T-015 | BA + Product | Refresh stale decision/readiness wording and optional research ownership mapping | DEC-021 | CONS-401; S-603 |
| T-016 | QA | End-to-end privacy, quality, recovery, variance, and net-value qualification matrix | T-004 through T-012 | EVID-401; QG-301 through QG-309 |
| T-017 | Engineering | Codex IDE/desktop pre-thread state parity spike | Codex CLI vertical | OQ-001; post-MVP unless qualified |
| T-018 | Product + Engineering | Causal skill-contribution analysis and claim language review | T-011 | F-502; RISK-003 |

## Definition of Ready
| Item ID | Type | Ready? | Missing Info | Blocker? | Next Action |
| --- | --- | --- | --- | --- | --- |
| EPIC-001 / F-101 | Epic/Feature | Ready | None at backlog level | No | Decompose S-101/S-102 in story refinement |
| F-102 / S-103 | Feature/Story | Ready | None at contract level; implementation evidence remains | No | Implement T-001 under accepted DEC-024 |
| EPIC-002 | Epic | Ready | Live adapter evidence | No | Refine Claude then Codex stories in DEC-019 order |
| EPIC-003 | Epic | Ready | Implementation evidence | No | Refine receipt stories with Security/Privacy review |
| EPIC-004 | Epic | Ready | Runner and executed fixture evidence | No | Preserve T-007/T-008 and QA invalidation authority |
| EPIC-005 | Epic | Ready with assumptions | Live provider counters, eligibility, variance, and causal results | No | Implement and qualify adapters/pilots under EVID-401 |
| EPIC-006 | Epic | Ready with assumptions | Qualification evidence and CONS-401 cleanup | No | Complete net-value instrumentation and evidence package |
| Backlog package | Artifact | Ready for user-story decomposition review | Estimates and story-level technical choices intentionally absent | No | Run `ai-sdlc-user-story-decomposition` |

- Every story has an actor, outcome, value, priority, MVP status, acceptance summary, and dependency.
- No implementation estimate is implied. S-103 is contract-ready under DEC-024; effectiveness and rollout remain gated by EVID-401 and downstream reviews.
