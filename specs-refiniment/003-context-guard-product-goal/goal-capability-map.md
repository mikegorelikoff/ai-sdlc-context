---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "goal-capability-map.md"
  path: "specs-refiniment/003-context-guard-product-goal/goal-capability-map.md"
  workspace: "refinement"
  skill: "ai-sdlc-goal-capability-and-epic-mapping"
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
    - "BR-104"
    - "BR-107"
    - "BR-110"
    - "BR-111"
    - "BR-112"
    - "BR-201"
    - "BR-202"
    - "BR-205"
    - "BR-210"
    - "BR-211"
    - "BR-212"
    - "CAP-001"
    - "CAP-002"
    - "CAP-003"
    - "CAP-004"
    - "CAP-005"
    - "CAP-006"
    - "CAP-007"
    - "CAP-008"
    - "CAP-009"
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
    - "DEC-014"
    - "DEP-001"
    - "DEP-002"
    - "DEP-003"
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
    - "NFR-102"
    - "RISK-003"
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
    - "specs-refiniment/003-context-guard-product-goal/requirements-readiness.md"
    - "specs-refiniment/003-context-guard-product-goal/research.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-goal-capability-and-epic-mapping"
    - "goal-capability-map"
    - "review"
    - "conditional-ready"
    - "outcome-map"
    - "mapping-only"
---

# goal-capability-map.md

## Feature Summary
- Context Guard is a local MVP for developers actively using Claude Code and Codex. It aims to reduce avoidable provider-reported cache tokens before productive work while preserving complete required and safety-critical instructions, local evidence, and developer control.
- Accepted outcome constraints are DEC-002 through DEC-004: target active AI-agent developers; measure at least 30% fewer normalized cache tokens per provider for the same task/model; prevent only explicitly irrelevant skill content while retaining full required, safety-critical, and uncertain content.
- The map is outcome-level planning only under the 7/10 conditional readiness verdict and proposed DEC-013. It does not authorize backlog decomposition, delivery commitment, architecture selection, implementation, or a savings claim.
- Proposed DEC-009 through DEC-012 define the relevance contract, quality evaluator, measurement protocol, and supported provider boundary; they remain governance gates rather than accepted facts.

## Actors and Stakeholders
- Primary actor: the developer declares the task, starts the guarded session, may explicitly invoke skills, inspects local receipts, bypasses guarded mode, and restores the baseline profile.
- Repository maintainer owns versioned local safety, require, and exclude policy using authoritative host skill identities; they cannot rewrite authoritative skill content or silently weaken mandatory rules.
- Product owns outcome, MVP boundary, net-value thresholds, and claim approval. Delivery owns progression gates. Engineering owns provider adapters, deterministic evaluation, state coordination, and recovery. QA owns fixture validity, hard-gate evaluation, run invalidation, and measurement signoff. Security/Privacy co-owns receipt lifecycle.
- Claude Code and Codex are external host boundaries: they supply authoritative skill inventory/state and supported startup controls. Enterprise buyers, centralized administrators, and cross-developer monitoring operators are outside the MVP.

## Scope and Boundaries
- In scope: local pre-session capability/version preflight; authoritative skill inventory; deterministic per-skill classification; provider-supported startup visibility/configuration; new-session enforcement; actual-state verification; full-load fallback; rollback; sanitized receipts; quality-first paired measurement; and provider-independent result reporting.
- Claude MVP boundary: Claude Code 2.1.218+ non-plugin skills controlled by startup `skillOverrides`; `user-invocable-only` is the conservative action for an explicit `irrelevant` result. Plugin skills and unsupported client surfaces remain full-load/measurement-only.
- Codex MVP boundary: Codex CLI 0.144.1+ absolute-path startup `skills.config`; app-server-backed clients may use verified user-level skill state before `thread/start` with restoration. Repository-local filtering and unqualified IDE/desktop parity are excluded.
- Out of scope: skill-body rewriting or summarization, a customer-facing compact skill index, semantic model classification, remote prompt/source collection, mid-session interception, enterprise policy administration, and combined-provider claims.
- Planning boundary: only goal/capability/epic mapping is approved to proceed. GOV-301, DATA-301, PERF-301, and OPS-301 block downstream committed planning; EVID-301 blocks qualification and release.

## Workflows and Failure Paths
- Baseline: preflight provider/version, inventory authoritative skills, preserve the current full-load profile, start a fresh session, run a frozen task, validate quality, and record the normalized provider measurement window.
- Guarded path: resolve the same declared inputs, classify every skill using fixed precedence, apply only supported provider actions, verify actual state, start a fresh session, execute the same fixture, pass hard quality gates, and then compare cache-token measurements.
- Classification precedence: identity/control failure to safe `uncertain`; then `safety-critical`; explicit or host/repository mandatory `required`; policy-required; exact policy-irrelevant; default `uncertain`. Only `irrelevant` may reduce visibility.
- Failure paths: ambiguity, stale inputs, capability mismatch, action failure, missing receipt fields, quality regression, task/model/repository mismatch, or measurement-schema drift invalidate savings and restore the baseline/full-load state.
- Operational gaps remain capability work: concurrent sessions, stale locks, crashes, user edits during guarded mode, rollback conflict, and idempotent recovery require an explicit contract before implementation-ready stories.

## Requirements and Business Rules
- BR-101 through BR-112 establish local operation, irrelevant-skill exclusion, full required-instruction preservation, controlled comparison, provider-specific 30% measurement, privacy, conservative fallback, rollback, claim accuracy, provider isolation, bounded startup overhead, and evidence scope.
- BR-201 through BR-212 and AC-201 through AC-210 define authoritative identity, allowed inputs, fixed precedence, deterministic lifetime, requested/actual actions, full-load fallback, reproducible sanitized receipts, and prohibited content.
- Any missing, duplicate, stale, conflicting, unsupported, or ambiguous identity/control evidence must yield `uncertain`; uncertainty earns no optimization credit.
- Token size, historical token usage, or model-generated semantic judgment may prioritize measurement but cannot classify a skill as irrelevant.
- Quality is evaluated before savings. Any missing required instruction, policy violation, task failure, unauthorized modification, privacy leak, or failed recovery is a hard failure and invalidates the pair and effectiveness claim.

## Data, Integrations, and Non-Functional Requirements
- Provider integrations are versioned adapters for Claude Code startup settings and Codex CLI/app-server startup state. Each adapter must preflight capabilities, verify actual state before model work, and support non-destructive restoration.
- A local receipt must include schema/provider/client versions, run and pair identifiers, task/repository/policy/inventory fingerprints, stable skill identity, metadata/body digests, reason codes, classification, requested and actual actions, fallback reason, measurement-window identifiers, quality result, and timestamp.
- Receipts must exclude raw prompts, responses, source content, credentials, full skill bodies, and secret values. Raw content is not a relevance input and must not be centralized.
- Determinism, fail-safe full inclusion, local-only operation, provider isolation, reproducibility, schema-version checks, and no material startup/interruption regression are required non-functional outcomes.
- DATA-301 leaves receipt path, permissions/ownership, retention, cleanup/deletion, corruption recovery, and concurrent access unresolved. PERF-301 leaves numeric startup-duration and interruption thresholds unresolved.

## Dependencies, Risks, and Constraints
- DEP-001: provider behavior and configuration surfaces are external, version-dependent contracts. DEP-002: local logs are schema-dependent and privacy-sensitive. DEP-003: the first controlled pilot uses this repository and three frozen fixtures.
- Principal risks: attributing cache usage to skills without causal evidence; removing required instructions; provider schema or surface drift; corrupting user configuration; leaking local content; overstating a one-repository result; and optimization overhead erasing value.
- Mitigations mapped into capabilities include per-provider preflight, authoritative digests, deterministic precedence, full-load fallback, actual-state verification, local sanitized receipts, hard quality gates, paired fresh sessions, versioned counter extraction, rollback, and provider-independent claims.
- Constraint: current authoring may run on Python 3.9.6, but the qualifying runner requires Python 3.10+ and installed provider versions must be re-preflighted.
- Unresolved delivery blockers: GOV-301 decision disposition, DATA-301 receipt lifecycle, PERF-301 thresholds, OPS-301 coordination/recovery, EVID-301 execution evidence, and CONS-301 upstream consistency cleanup.

## Decisions, Assumptions, and Open Questions
- Accepted authority: DEC-002 defines the target user and promise; DEC-003 defines the provider-specific 30% target and pilot; DEC-004 requires complete required/safety content and excludes a compact skill index.
- Proposed dependencies: DEC-005 positioning, DEC-006 rollout, DEC-007 original hold, DEC-009 relevance contract, DEC-010 quality evaluator, DEC-011 measurement contract, DEC-012 provider boundary, DEC-013 mapping-only readiness, and DEC-014 adoption of this four-goal, nine-capability, six-epic planning model. DEC-001 and DEC-008 require explicit reconciliation or supersession.
- This map assumes no unrecorded product approval. Proposed decisions are mapped as gated capabilities and epics, not converted to accepted requirements.
- OQ-001: Engineering must verify Codex IDE/desktop pre-thread skill-state parity. OQ-002: Product and Engineering must isolate the causal cache-token contribution. OQ-003: Product must decide later whether Claude plugin skills or Codex repository-local configuration justify a compatibility slice.
- Open-item control: every blocker has an owner, impact, and resolution/next step in this artifact. Product/Delivery/Engineering/QA disposition proposed decisions; Security/Privacy and Engineering close receipt governance; Product/Engineering set net-value thresholds; Engineering defines coordination/recovery; Engineering/QA execute qualification.

## Success Measures
- Primary outcome: for each provider independently, median guarded normalized cache tokens are at least 30% lower than paired baseline for the same frozen task/model after five valid warm-cache pairs per fixture, with no outlier deletion and the DEC-011 variance gate satisfied.
- Quality gate: all three provider-neutral fixtures pass machine completion and instruction-preservation oracles; zero hard-gate failures; explicit AI-SDLC skill use loads the complete authoritative instructions.
- Safety/control gate: unsupported, ambiguous, stale, or failed control states use full-load fallback; rollback restores the baseline without changing unrelated configuration; developers can inspect, bypass, and restore locally.
- Privacy/evidence gate: receipts reproduce decisions from declared fingerprints and reason codes while containing none of the prohibited prompt, response, source, credential, secret, or full-skill content.
- Net-value gate: startup duration and developer interruption do not materially worsen. Numeric thresholds and failure disposition must be set through PERF-301 before release slicing.
- Claim gate: results remain provider-specific, version-pinned, and limited to the qualified repository/fixtures until broader evidence exists.

## Source Coverage
- `specs-refiniment/003-context-guard-product-goal/discovery.md`: customer problem, MVP, accepted outcome constraints, risks, metrics, and non-goals.
- `specs-refiniment/003-context-guard-product-goal/prfaq.md`: working-backwards narrative, BR-101 through BR-112, rollout intent, launch risks, and business requirements.
- `specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md`: original four delivery gaps, definition-complete updates, contradictions, and residual delivery blockers.
- `specs-refiniment/003-context-guard-product-goal/requirements-readiness.md`: 7/10 conditional verdict, mapping boundary, GOV/DATA/PERF/OPS/EVID/CONS gaps, and required follow-up.
- `specs-refiniment/003-context-guard-product-goal/business-context.md`: actors, permissions, WF-201 through WF-206, BR-201 through BR-212, and AC-201 through AC-210.
- `specs-refiniment/003-context-guard-product-goal/research.md`: RF-001 through RF-018 provider feasibility, control surfaces, limitations, and open questions.
- `specs-refiniment/003-context-guard-product-goal/qa.md`: three fixtures, hard gates, invalidation rules, regression targets, and execution status.
- `specs-refiniment/003-context-guard-product-goal/qa-strategy.md`: adapters, paired protocol, measurement windows, receipt fields, aggregation, and strategy risks.
- `specs-refiniment/003-context-guard-product-goal/decision-log.md`: DEC-001 through DEC-013 status and authority.
- `specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon` and both refinement indexes provide lifecycle/routing evidence. The full-flow 24,000-token context pack identified 277 deferred ranges; their merged evidence ranges were read before synthesis.

## Business Goals
| Goal ID | Goal | Metric | Target | Owner | Source |
| --- | --- | --- | --- | --- | --- |
| GOAL-001 | Reduce avoidable pre-work AI-agent cache consumption for active Claude Code and Codex developers | Provider-normalized guarded versus baseline cache tokens for the same frozen task/model | At least 30% median reduction per provider after quality gates | Product | DEC-002; DEC-003; BR-104 |
| GOAL-002 | Preserve task correctness, required/safety instructions, evidence, and developer control while optimizing context | Hard-gate failures; instruction-oracle results; bypass/rollback success | Zero hard failures and 100% complete required/safety instruction preservation across valid pairs | Product and QA | DEC-004; DEC-010; QG-301 through QG-309 |
| GOAL-003 | Make optimization trustworthy, local, reproducible, and bounded to supported provider surfaces | Qualified adapter/profile runs with reproducible privacy-safe receipts and successful restoration | Every credited run is version-preflighted, receipted, provider-isolated, and recoverable; unsupported states use full load | Engineering, QA, Security/Privacy | DEC-009; DEC-011; DEC-012; AC-201 through AC-210 |
| GOAL-004 | Deliver positive net developer value without overstating evidence | Startup duration; developer interruptions; scope/claim compliance | No material regression; numeric thresholds resolved before release slicing; claims remain provider/version/pilot bounded | Product and Engineering | BR-110; BR-111; PERF-301; RISK-003 |

## Role Matrix
| Actor | Role | Need | Permission Boundary | Source |
| --- | --- | --- | --- | --- |
| Developer | Primary beneficiary and task initiator | Lower avoidable cache usage without losing instructions; inspect and control guarded runs | May declare task, invoke, inspect, bypass, and restore; no forced remote disclosure | DEC-002; DEC-004; business-context.md |
| Repository maintainer | Local policy owner | Express stable safety/require/exclude rules for repository work | May author versioned declarative rules; cannot rewrite skills or weaken mandatory policy | DEC-009; BR-202 through BR-205 |
| Product | Outcome and claim owner | Decide scope, value thresholds, rollout, and defensible claims | Must disposition proposed decisions and cannot treat unvalidated savings as fact | DEC-003; DEC-005; DEC-006; DEC-013 |
| Delivery | Lifecycle gate owner | Advance only when required evidence and decisions are complete | May allow outcome mapping; must block committed backlog/delivery while readiness blockers remain | DEC-007; DEC-013 |
| Engineering | Provider/control owner | Build deterministic adapters, state coordination, receipts, and recovery | Must validate providers independently and cannot infer control from token logs | GAP-001; GAP-002; OPS-301 |
| QA | Quality and measurement authority | Validate fixtures, invalidate bad runs, and sign off evidence | Savings are evaluated only after hard gates; invalid pairs cannot support claims | DEC-010; DEC-011; EVID-301 |
| Security/Privacy | Receipt governance owner | Keep audit evidence useful without retaining sensitive content | Must define local lifecycle and prohibit prompts, responses, source, secrets, and skill bodies | DATA-301; NFR-102 |
| Claude Code / Codex host | External authoritative boundary | Expose versioned inventory, invocation/state, and supported startup controls | Provider-owned context assembly is not assumed mutable; ambiguity falls back to full load | RF-001 through RF-018 |

## Capability Map
| Capability ID | Capability | Goal Ref | Actors | Dependencies |
| --- | --- | --- | --- | --- |
| CAP-001 | Provider capability, version, and authoritative skill-inventory preflight | GOAL-003 | Engineering; host | DEC-012; RF-012 through RF-018; EVID-301 |
| CAP-002 | Deterministic skill relevance evaluation with fixed precedence and safe uncertainty | GOAL-002; GOAL-003 | Developer; maintainer; Engineering | DEC-009; BR-201 through BR-210; GOV-301 |
| CAP-003 | Provider-specific guarded startup profile application and actual-state verification | GOAL-001; GOAL-003 | Developer; Engineering; host | CAP-001; CAP-002; DEC-012; EVID-301 |
| CAP-004 | Developer transparency, bypass, full-load fallback, rollback, and session-state recovery | GOAL-002; GOAL-004 | Developer; Engineering | CAP-003; BR-107; OPS-301 |
| CAP-005 | Local privacy-safe decision and measurement receipts with governed lifecycle | GOAL-003 | Developer; QA; Security/Privacy; Engineering | BR-211; BR-212; DATA-301 |
| CAP-006 | Frozen task fixtures, instruction oracles, hard quality gates, and invalidation | GOAL-002 | QA; Engineering | DEC-010; CAP-003; EVID-301 |
| CAP-007 | Provider-normalized paired measurement, aggregation, and causal contribution analysis | GOAL-001; GOAL-004 | Product; QA; Engineering | DEC-003; DEC-011; CAP-005; CAP-006; EVID-301 |
| CAP-008 | Net-value, evidence-scope, governance, and claim gate | GOAL-004 | Product; Delivery; QA | CAP-006; CAP-007; GOV-301; PERF-301 |
| CAP-009 | Versioned local relevance-policy authoring and validation | GOAL-002; GOAL-003 | Repository maintainer; Engineering | CAP-001; CAP-002; DEC-009; policy usability evidence |

## Epic Map
| Epic ID | Epic | Capability Ref | Outcome | Priority | Risks |
| --- | --- | --- | --- | --- | --- |
| EPIC-001 | Trustworthy provider-aware relevance decisions | CAP-001; CAP-002; CAP-009 | A declared task and authoritative inventory produce deterministic, explainable, conservative per-skill decisions | MVP P0 | Provider drift; policy errors; proposed DEC-009/DEC-012 |
| EPIC-002 | Safe guarded session control and recovery | CAP-003; CAP-004 | Developers can start a verified guarded session and always retain full-load fallback, bypass, and non-destructive restoration | MVP P0 | Configuration corruption; concurrent sessions; OPS-301 |
| EPIC-003 | Privacy-safe local evidence | CAP-005 | Every decision and measurement is locally auditable without retaining prohibited content | MVP P0 | Receipt leakage/corruption; DATA-301 |
| EPIC-004 | Quality-qualified behavior | CAP-006 | Guarded runs prove task completion and complete required-instruction preservation before any savings are considered | MVP P0 | False equivalence; nondeterminism; missing runner evidence |
| EPIC-005 | Provider-specific cache-value validation | CAP-007 | Claude Code and Codex independently produce valid paired evidence for or against the 30% goal and isolate causal contribution | MVP P0 | Counter drift; variance; EVID-301; over-attribution |
| EPIC-006 | Net-value and defensible rollout governance | CAP-008 | Product and Delivery can accept, revise, or reject rollout and claims from explicit quality, privacy, performance, and evidence gates | MVP P0 gate | GOV-301; PERF-301; one-repository overclaim |

## Outcome Traceability
| Goal ID | Capability IDs | Epic IDs | Coverage | Notes |
| --- | --- | --- | --- | --- |
| GOAL-001 | CAP-003; CAP-007 | EPIC-002; EPIC-005 | Partially covered | Mechanism and protocol are defined; provider adapters, runner, and live paired evidence remain EVID-301 work |
| GOAL-002 | CAP-002; CAP-004; CAP-006; CAP-009 | EPIC-001; EPIC-002; EPIC-004 | Partially covered | Rules and quality gates are defined; governance acceptance, recovery contract, and executed fixtures remain open |
| GOAL-003 | CAP-001; CAP-002; CAP-003; CAP-005; CAP-009 | EPIC-001; EPIC-002; EPIC-003 | Blocked by decision | Provider boundary and relevance contract are proposed; DATA-301, OPS-301, and qualification evidence block delivery |
| GOAL-004 | CAP-004; CAP-007; CAP-008 | EPIC-002; EPIC-005; EPIC-006 | Blocked by decision | PERF-301 numeric thresholds and GOV-301 disposition are required before release slicing or claims |

- All goals link to at least one capability and epic; all capabilities link to a goal and one outcome-oriented epic.
- The map intentionally contains no generic miscellaneous epic and no architecture or implementation tasks.
- Backlog gap review is the next lifecycle stage, but it must treat GOV-301, DATA-301, PERF-301, and OPS-301 as planning blockers and EVID-301 as qualification work. This mapping artifact does not waive the DEC-013 no-go boundary.
