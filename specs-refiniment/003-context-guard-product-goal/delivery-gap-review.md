---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "delivery-gap-review.md"
  path: "specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md"
  workspace: "refinement"
  skill: "ai-sdlc-delivery-package-gap-review"
  flow_mode: "full"
  state_file: "specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  status: "review"
  owner: "Delivery lead"
  created_at: "2026-07-26"
  updated_at: "2026-07-26"
  trace_ids:
    - "AC-001"
    - "AC-007"
    - "BR-101"
    - "BR-103"
    - "BR-106"
    - "BR-112"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "DEP-001"
    - "DEP-002"
    - "DEP-003"
    - "NFR-101"
    - "NFR-102"
    - "NFR-108"
    - "RISK-001"
    - "RISK-002"
    - "RISK-004"
    - "RISK-005"
    - "RISK-006"
    - "RISK-007"
  related_artifacts:
    - "specs-refiniment/003-context-guard-product-goal/business-context.md"
    - "specs-refiniment/003-context-guard-product-goal/decision-log.md"
    - "specs-refiniment/003-context-guard-product-goal/discovery.md"
    - "specs-refiniment/003-context-guard-product-goal/prfaq.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-delivery-package-gap-review"
    - "delivery-gap-review"
    - "review"
---

# delivery-gap-review.md

## Feature Summary
- Review target: the full-flow discovery package and PRFAQ/BRD for Context Guard startup-context control.
- Confirmed outcome: a local MVP pilot for active Claude Code and Codex developers, targeting at least 30% fewer normalized cache tokens without loss of required or safety-critical instructions.
- Package strength: customer problem, MVP exclusions, high-level workflows, privacy posture, rollback, provider-specific reporting, and launch risks are explicit.
- Review judgment: the package is not yet safe for story or implementation-spec decomposition because four core behaviors would have to be invented downstream.
- Delivery blockers: supported pre-context control point; relevance-decision contract; executable task/instruction quality evaluator; provider-specific measurement and aggregation window.
- Proposed governance decision: DEC-007 records a no-go for decomposition until GAP-001 through GAP-004 are resolved with evidence.

## Actors and Stakeholders
- Clear actors: developer, AI coding-agent runtime, Context Guard, repository maintainer, Product, Engineering, QA, and Security/Privacy.
- Clear ownership: Product owns scope and claims; Engineering owns provider feasibility and inclusion behavior; QA owns comparisons and non-regression; Security/Privacy owns receipt minimization.
- Actor gap: no named technical decision authority is identified for accepting provider-specific feasibility evidence and choosing the control boundary. Engineering is the work owner, but approval responsibility is ambiguous.
- Actor gap: the benchmark operator is described, but authority to invalidate a run and approve the final statistical method is not explicit; QA should own both.
- Non-MVP actors are clearly excluded: enterprise buyer, centralized administrator, and cross-developer monitoring operator.
- Resolution: requirements readiness should assign an Engineering approver for GAP-001/GAP-002 and confirm QA as the acceptance authority for GAP-003/GAP-004.

## Scope and Boundaries
- Confirmed MVP: Claude Code and Codex evaluated independently; this repository as pilot; local measurement; irrelevant full-skill exclusion before context entry; full required/safety skill preservation; same-task comparison; quality gate; privacy-safe receipt; rollback.
- Confirmed exclusions: compact skill index as customer solution, billing-cost claims, central telemetry, enterprise enforcement, semantic/vector retrieval, skill mutation, and optimization of all context sources.
- Boundary gap: “before startup context entry” is an outcome boundary, not an established provider surface. Delivery cannot yet tell whether this is runtime control, install-time packaging, host-native selection, or infeasible.
- Boundary gap: “irrelevant skill” has no source-of-truth or deterministic classification contract. The package states behavior for uncertainty but not how relevance evidence is obtained.
- Scope tension: the existing Context Guard hooks govern tool operations, while the MVP must act before provider context assembly. Treating this as a direct extension without a feasibility boundary could hide a new product surface.
- Verdict: scope is product-clear but delivery-incomplete until GAP-001 and GAP-002 resolve.

## Workflows and Failure Paths
- Confirmed workflows: measurement-only baseline, guarded run, controlled comparison, full-load on relevance uncertainty, and rollback.
- Confirmed failures: missing counters, provider schema drift, quality regression, privacy leakage, excessive startup overhead, and absent pre-context control.
- Workflow gap: guarded startup begins with “exclude irrelevant full skill content,” but the preceding trigger, decision inputs, evaluator, and authoritative inclusion output are unspecified.
- Workflow gap: equivalence between baseline and guarded task outcomes is required, but the task runner, completion oracle, instruction checks, and manual-versus-automated review boundary are unspecified.
- Workflow gap: comparison invalidation names changed task/model/repository state but does not define repeat count, aggregation method, warm/cold cache handling, session boundary, or outlier treatment.
- Workflow gap: rollback is outcome-defined but lacks operational trigger ownership, persisted configuration state, and recovery confirmation.
- Story decomposition would invent these core steps; GAP-001 through GAP-004 remain blockers.

## Requirements and Business Rules
- Strong requirements: BR-101 through BR-112 cover exclusion, required-skill preservation, controlled comparison, 30% target, invalidation on quality regression, privacy, uncertainty fallback, rollback, claim accuracy, provider isolation, startup overhead, and evidence scope.
- Missing rule: what evidence makes a skill required, irrelevant, safety-critical, or uncertain, and which precedence applies when sources disagree.
- Missing rule: whether relevance is determined per task, turn, repository, session, provider, or installation.
- Missing rule: how mandatory skill trigger rules imposed by the host or repository override optimization.
- Missing rule: how “complete authoritative skill” identity and version are proven in a guarded run.
- Missing rule: the minimum benchmark repetition and acceptable variation supporting the 30% gate.
- Missing rule: the exact Codex and Claude counter window, including cumulative versus per-call values and duplicate-event treatment.
- Existing BA acceptance criteria AC-001 through AC-007 describe Stage 1/Stage 2 behavior, not the new startup-control MVP; downstream artifacts must use PRFAQ requirements and add explicit startup-control acceptance IDs.

## Data, Integrations, and Non-Functional Requirements
- Confirmed data categories: provider/model/version, task ID, repository state, mode, timestamps, cache counters, startup duration, quality outcome, and skill identifiers when observable.
- Confirmed privacy boundary: no prompts, source, credentials, raw responses, or full skill bodies in receipts.
- Data-source gap: local JSONL fields are evidence, not a stable provider contract. No schema version, fallback, receipt schema, or provenance hash is defined.
- Measurement gap: Claude uses cache-read plus cache-creation and Codex uses cached-input, but the package does not define which event(s) constitute a run or whether counters are cumulative, incremental, duplicated, or reset between sessions.
- Codex tension: the observed first event had substantial uncached input and zero cached input; a cached-input-only metric may not measure the first startup payload described by the customer problem.
- Integrity gap: evidence that an irrelevant full skill was absent from model context is required by BR-101, but the observable source and privacy-safe proof mechanism are unspecified.
- Retention gap: local receipt location, retention, cleanup, access permissions, and deletion behavior are absent.
- Non-functional coverage is otherwise strong: safety, privacy, determinism, reversibility, compatibility, auditability, performance measurement, and fail-safety are stated.

## Dependencies, Risks, and Constraints
- DEP-001 is correctly identified as critical: a supported pre-context inclusion boundary must exist.
- DEP-002 is correctly identified as high: repeatable pilot tasks and objective quality/instruction checks are required.
- DEP-003 is appropriately deferred: additional repositories are needed before general claims, not before the first pilot.
- RISK-001, RISK-002, RISK-004, and RISK-006 directly threaten feasibility, safety, causal validity, and repeatability.
- Dependency gap: provider documentation or executable evidence for Claude Code and Codex control surfaces is absent; local usage logs prove measurement fields, not intervention authority.
- Dependency gap: no declared source exists for skill inventory, trigger metadata, safety classification, or authoritative version identity.
- Constraint tension: rejecting a compact skill index removes one possible decision surface but does not identify an alternative; downstream design must not silently reintroduce it under another name.
- Constraint: no implementation commitment should be made until GAP-001 is resolved independently for both providers.

## Decisions, Assumptions, and Open Questions
- Accepted decisions: DEC-002 target/customer promise; DEC-003 provider-specific 30% token gate and pilot; DEC-004 full required-skill preservation and rejection of a compact skill index as customer solution.
- Proposed decisions: DEC-001 overarching product framing; DEC-005 PRFAQ positioning; DEC-006 two-phase pilot; DEC-007 no-go for decomposition until four blockers resolve.
- Decision gap: DEC-005 and DEC-006 are used throughout the PRFAQ but remain proposed. Owner: Product. Impact: high narrative and launch consistency. Resolution/next step: accept, revise, or reject before requirements readiness can approve the package.
- Assumption gap: A-101 treats local counters as sufficiently stable without a versioned extraction or aggregation contract. Owner: Engineering and QA. Impact: high metric validity. Resolution/next step: resolve through GAP-004 evidence and replace the assumption with provider-specific rules.
- Hypothesis gap: H-101 states skills materially cause startup cache usage, but current logs show correlation rather than isolated attribution. Owner: Product and Engineering. Impact: high business-case validity. Resolution/next step: include contribution isolation in the pilot; return to discovery if the effect is immaterial.
- Open questions OQ-001 through OQ-004 are owned and carry next steps; OQ-001 and OQ-002 remain decomposition blockers, while OQ-003 and OQ-004 can remain open through early planning if explicitly gated before readiness/public claims.

## Success Measures
- Confirmed primary measure: at least 30% fewer normalized cache tokens for valid same-task comparisons, reported separately for Claude Code and Codex.
- Confirmed guardrails: equivalent task/instruction outcomes, sanitized evidence, reversibility, repeatability, and startup performance.
- Measure gap: “same task” lacks a canonical task definition, fixed inputs, completion oracle, and allowed nondeterminism.
- Measure gap: “same model” does not cover provider/model revision, reasoning mode, context-window configuration, or cache-warm state.
- Measure gap: repeatability is required, but sample size, aggregation statistic, variance threshold, confidence rule, and failure threshold are not specified.
- Measure gap: the target is described as pre-work cache reduction, but no exact start/end event defines “before productive work starts.”
- Measure gap: no rule specifies whether each provider must independently reach 30% or whether one provider may fail; the package implies independent gates and should state this explicitly.
- Result: the metric is directionally testable but not yet executable; GAP-003 and GAP-004 block acceptance-test synthesis.

## Source Coverage
- `specs-refiniment/003-context-guard-product-goal/discovery.md`: full-flow customer/problem validation, MVP, requirements, measures, risks, dependencies, and local-log evidence limitations.
- `specs-refiniment/003-context-guard-product-goal/prfaq.md`: pilot narrative, FAQs, business requirements, non-functional requirements, success measures, and launch risks.
- `specs-refiniment/003-context-guard-product-goal/business-context.md`: earlier quick-flow goal framing and existing-product rules; reviewed for contradictions and identified as stale where DEC-003 later resolves the metric.
- `specs-refiniment/003-context-guard-product-goal/decision-log.md`: DEC-001 through DEC-007, including accepted product constraints, proposed launch decisions, and the proposed no-go verdict.
- `specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon`: lifecycle authority for completed discovery and PRFAQ stages.
- The deterministic gap scan consumed all five sources and returned no missing document category, then identified 22 exact deferred evidence ranges due to the full-flow budget.
- All 22 deferred ranges were read before drafting this verdict, covering BA rules/acceptance/gaps, discovery requirements/data/decisions/measures/sources/customer evidence/alternatives/value/scenarios/MVP/operations/risks, and PRFAQ decisions/measures/sources/press-release claims/business requirements/launch risks.
- Upstream implementation evidence (`README.md`, docs, existing Stage 1/Stage 2 requirements) is traced through discovery and PRFAQ; it supports existing product constraints but not the new pre-context control surface.
- Sanitized local usage evidence supports large cache/input counters but does not prove skill causation, intervention authority, or billed cost.
- Missing evidence categories: provider control-surface proof, relevance-classification contract, executable task/quality fixtures, and provider-specific counter aggregation receipts.

## Evidence Reviewed
- `specs-refiniment/003-context-guard-product-goal/discovery.md`: full-flow customer/problem validation, MVP, workflows, measurements, risks, dependencies, and source limitations.
- `specs-refiniment/003-context-guard-product-goal/prfaq.md`: pilot narrative, FAQs, BR-101 through BR-112, NFR-101 through NFR-108, success measures, and launch risks.
- `specs-refiniment/003-context-guard-product-goal/business-context.md`: earlier quick-flow goal framing and existing-product workflows/rules; treated as partially stale where discovery later resolved the metric.
- `specs-refiniment/003-context-guard-product-goal/decision-log.md`: DEC-001 through DEC-007 and their status/ownership.
- `specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon`: discovery and PRFAQ completion authority.
- Sanitized local-log findings as cited by discovery: Claude startup/cache fields and Codex token-count fields. No prompts, source, credentials, or unrelated session payloads were reviewed in this stage.
- Evidence quality: sufficient for product framing and a no-go gap verdict; insufficient for implementation decomposition or acceptance-test design.

## Gap Matrix
| Area | Gap | Evidence | Impact | Severity | Owner | Resolution |
| --- | --- | --- | --- | --- | --- | --- |
| GAP-001 Provider boundary | Definition complete: provider-native startup profiles are available for Claude non-plugin skills and Codex CLI/app-server sessions; no generic runtime hook exists | DEC-012; research.md RF-012 through RF-018; version-pinned Codex prompt diagnostics | The bounded MVP has a buildable control boundary; live Claude and app-server/IDE qualification remain | Definition complete / execution blocked | Engineering with Product | Accept or revise DEC-012, implement preflight/profile/verification/rollback adapters, and qualify supported surfaces |
| GAP-002 Relevance contract | Definition complete: DEC-009 and BR-201 through BR-212 define authoritative identity, inputs, precedence, outputs, lifetime, and full-load fallback | DEC-009; business-context.md | Core inclusion behavior is specified; governance acceptance and implementation remain | Definition complete / governance pending | Engineering with Product | Accept or revise DEC-009, then implement provider adapters without copied skill content |
| GAP-003 Quality evaluator | Definition complete: three frozen fixtures, machine oracles, instruction checks, invalidation authority, and hard gates are specified | DEC-010; qa.md | Acceptance behavior is specified; runner and live evidence remain absent | Definition complete / execution blocked | Product and QA | Accept or revise DEC-010, implement validators, and execute both providers |
| GAP-004 Measurement window | Definition complete: qa-strategy.md specifies the primary/diagnostic windows, Claude deduplication and cache-write/read sum, Codex exact-event or validated cumulative delta, warm-cache paired protocol, five valid pairs per fixture, no outlier deletion, distribution gates, and sanitized receipt | DEC-003; DEC-011; qa-strategy.md; official provider contracts; sanitized local-log observations | The 30% calculation is specified; execution evidence is still absent | Definition complete / execution blocked | Engineering and QA | Implement the versioned adapters and runner, validate receipt replay, and execute the provider-partitioned pilot |
| GAP-005 Decision status | DEC-005 and DEC-006 drive PRFAQ positioning and rollout but remain proposed | PRFAQ decisions and decision-log.md | Downstream scope and launch artifacts may treat unapproved choices as facts | High | Product | Accept, revise, or reject both before readiness approval and release slicing |
| GAP-006 Stale BA context | Quick-flow business context says a product-level target is absent while discovery/PRFAQ accept 30% | business-context.md gaps; DEC-003 | Traceability can surface contradictory product state | High | BA and Product | Refresh BA context in full flow or explicitly supersede the stale gap during its lifecycle stage |
| GAP-007 Receipt governance | Receipt schema, path, permissions, retention, cleanup, and deletion behavior are absent | NFR-102; BR-106; RISK-007 | Privacy and operational stories would invent data lifecycle rules | High | Security/Privacy and Engineering | Define minimal receipt schema and local data lifecycle before delivery spec |
| GAP-008 Provider schema contract | Local JSONL fields are observations, not stable integration contracts | A-101; RISK-005 | Schema drift can silently invalidate metrics | High | Engineering | Version field adapters, provenance, and explicit unmeasurable behavior |
| GAP-009 Root-cause attribution | Skills are a plausible contributor but not isolated as the material source | H-101; RISK-004 | MVP may miss the business outcome even if technically correct | High | Product and Engineering | Add contribution isolation to feasibility/pilot and return to discovery if immaterial |
| GAP-010 Generalizability | Only this repository is selected; task families and broader repositories remain open | DEP-003; OQ-004 | Pilot cannot support broad customer claims | Medium | Product | Keep pilot claim narrow; select broader evidence before public effectiveness messaging |

## Contradictions
- CONTR-001 Metric state: `business-context.md` says a product-level success target is not defined, while DEC-003, discovery, and PRFAQ accept a 30% provider-specific cache-token target. Resolution: treat DEC-003 as current authority and refresh/supersede the stale BA statement before final handoff.
- CONTR-002 Startup outcome versus available evidence: resolved for definition by DEC-011. The primary gate measures provider-reported cache tokens through the first task-relevant action; the full-task window and uncached input remain separate diagnostics and do not silently change DEC-003.
- CONTR-003 Determinism versus undefined inputs: the PRFAQ promises deterministic inclusion, but no authoritative relevance inputs or precedence exist. Resolution: GAP-002.
- CONTR-004 Extension versus integration boundary: resolved for definition by DEC-012. The capability is a provider-native pre-session profile applied by Context Guard; existing runtime hooks are not the optimization boundary.
- CONTR-005 Approved scope versus proposed launch: PRFAQ narrative uses DEC-005 and DEC-006 choices that remain proposed. Resolution: Product approval or revision before readiness approval.
- No contradiction exists between the 30% token target and the refusal to claim 30% billed-cost savings; the package consistently separates them.

## Blocking Questions
- BQ-001: Answered for the bounded MVP by research.md RF-012 through RF-018 and proposed DEC-012. Owner: Engineering. Remaining execution step: implement and qualify Claude startup settings plus Codex CLI/app-server profiles, with unsupported surfaces failing to full-load.
- BQ-002: What deterministic evidence and precedence classify each skill as required, irrelevant, safety-critical, or uncertain for a task/session? Owner: Engineering and Product. Impact: critical core behavior and safety. Resolution/next step: approve a relevance decision contract for GAP-002 before story/spec synthesis.
- BQ-003: Which named pilot tasks, completion oracle, and required-instruction checks establish equivalent quality? Owner: Product and QA. Impact: critical acceptance validity. Resolution/next step: define executable fixtures and QA invalidation ownership for GAP-003.
- BQ-004: Answered for definition by qa-strategy.md and DEC-011. Owner: Engineering and QA. Remaining execution step: implement and validate the versioned adapters/receipt, then obtain five valid pairs per fixture and provider.
- BQ-005: Are DEC-005 and DEC-006 accepted as the positioning and pilot-launch decisions? Owner: Product. Impact: high downstream consistency. Resolution/next step: accept, revise, or reject before requirements readiness approval.
- BQ-006: What local receipt lifecycle is permitted? Owner: Security/Privacy and Engineering. Impact: high privacy and operations. Resolution/next step: define schema, location, permissions, retention, cleanup, and deletion before delivery specification.

## Readiness Verdict
- Verdict: NO-GO for user-story decomposition, delivery specification, or implementation SDD.
- Reason: GAP-001 through GAP-004 are blockers under the full-flow gap framework; downstream work would invent the core integration, relevance behavior, quality oracle, and success calculation.
- Ready now: requirements-readiness review may formalize the score and blocker ownership; provider feasibility investigation and QA benchmark definition may proceed as blocker-resolution work.
- Not ready: goal/capability mapping that implies a buildable solution, backlog/story decomposition, release commitment, architecture selection, or implementation tasks.
- Exit criteria: documented provider-specific pre-context control evidence; accepted relevance-decision contract; executable pilot task/quality fixtures; validated provider-specific measurement receipt; Product disposition of DEC-005/DEC-006.
- Residual high gaps after blocker resolution: BA context refresh, receipt lifecycle, provider schema versioning, causal contribution validation, and broader-repository selection.
- Decision status: DEC-007 is proposed and should be accepted by Delivery/Product during requirements readiness; until then this artifact remains `blocked` and is the authoritative gap verdict.

## Blocker Resolution Update — 2026-07-27

- GAP-001 through GAP-004 are now definition-complete through DEC-009, DEC-010, DEC-011, DEC-012, business-context.md, qa.md, qa-strategy.md, and research.md.
- This does not make delivery ready automatically: DEC-005 through DEC-012 remain proposed where noted; provider adapters, receipt lifecycle, runner/validators, and live qualification evidence are not implemented.
- The next lifecycle action is a full requirements-readiness rerun against the refreshed package. That rerun, rather than this historical verdict, decides whether goal/capability mapping may begin.
