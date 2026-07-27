---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "prfaq.md"
  path: "specs-refiniment/003-context-guard-product-goal/prfaq.md"
  workspace: "refinement"
  skill: "ai-sdlc-prfaq-package-synthesis"
  flow_mode: "full"
  state_file: "specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  status: "review"
  owner: "Product owner"
  created_at: "2026-07-26"
  updated_at: "2026-07-26"
  trace_ids:
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
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEP-001"
    - "DEP-002"
    - "DEP-003"
    - "NFR-101"
    - "NFR-102"
    - "NFR-103"
    - "NFR-104"
    - "NFR-105"
    - "NFR-106"
    - "NFR-107"
    - "NFR-108"
    - "RISK-001"
    - "RISK-002"
    - "RISK-003"
    - "RISK-004"
    - "RISK-005"
    - "RISK-006"
    - "RISK-007"
    - "RISK-008"
    - "RISK-009"
    - "WF-101"
    - "WF-102"
    - "WF-103"
    - "WF-104"
    - "WF-105"
  related_artifacts:
    - "specs-refiniment/003-context-guard-product-goal/business-context.md"
    - "specs-refiniment/003-context-guard-product-goal/decision-log.md"
    - "specs-refiniment/003-context-guard-product-goal/discovery.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-prfaq-package-synthesis"
    - "prfaq"
    - "review"
---

# prfaq.md

## Feature Summary
- Initiative: add startup-context control to Context Guard's existing local prevention and reversible-compaction foundation.
- Target customer: developers actively using Claude Code or Codex.
- Customer problem: substantial cache tokens can be consumed before productive work begins, while current local logs reveal usage only after context has already been assembled.
- MVP outcome: prevent irrelevant full skill content from entering startup context, preserve every required and safety-critical instruction in full, and measure the change through controlled provider-specific cache-token comparisons.
- Product promise: reduce AI-agent cache usage before productive work starts without losing required instructions or evidence (DEC-002 and DEC-005).
- Success target: at least 30% fewer normalized cache tokens for the same task, provider, model, and repository state, with equivalent task and instruction-compliance outcomes (DEC-003).
- Status: decision-ready PRFAQ draft for a local pilot, not a public availability or verified cost-savings announcement.
- Critical dependency: Engineering must establish a provider-compatible control point before full skill content enters model context; current tool hooks may occur too late (DEP-001 and RISK-001).

## Actors and Stakeholders
- Developer: primary customer, enables the MVP, runs Claude Code or Codex, receives unchanged required instructions, and reviews local evidence.
- AI coding-agent runtime: assembles startup context, exposes or selects skills, and emits provider-specific local usage counters.
- Context Guard: applies the accepted startup-context boundary, captures sanitized measurement provenance, and provides bypass/rollback without changing authoritative skill files.
- Repository maintainer: owns pilot configuration, repeatable repository tasks, and local rollout posture.
- Product owner: owns customer promise, MVP scope, 30% target, launch claim, and decisions when feasibility or benchmark results require rescoping.
- Engineering: owns Claude Code and Codex feasibility, provider adapters, deterministic inclusion behavior, privacy controls, and rollback.
- QA: owns controlled baseline-versus-guarded comparisons, quality non-regression, repeatability, invalidation rules, and evidence receipts.
- Security/Privacy reviewer: verifies that usage measurement excludes prompts, source, credentials, raw responses, and full skill bodies.
- No enterprise buyer, centralized administrator, or cross-developer monitoring role is included in the MVP.

## Scope and Boundaries
- MVP includes: Claude Code and Codex evaluated independently; this repository as the first pilot; local cache-token measurement; relevance-based exclusion of irrelevant full skill content before startup context entry; complete loading of required and safety-critical skills; controlled same-task comparison; quality guardrails; privacy-safe evidence; bypass and rollback.
- Existing product boundary retained: local deterministic behavior, no required network service or model call for core control, no centralized collector, preserved evidence, and non-destructive configuration.
- MVP excludes: compact skill index as the user-facing solution; provider-billed cost attribution; public 30% currency-savings claim; semantic/vector retrieval; centralized telemetry; enterprise enforcement; rewriting or deleting authoritative skills; optimizing all system prompts, conversation history, repository context, or tool output as part of this increment.
- The 30% target is a pilot acceptance gate, not a guaranteed outcome for every task or repository.
- Uncertain relevance favors instruction preservation over token reduction.
- No public launch occurs until provider feasibility, privacy, quality equivalence, and measurement repeatability are demonstrated.

## Workflows and Failure Paths
- WF-101 Measurement-only baseline: bind a named task to provider, model, repository state, and quality checks; run without intervention; capture sanitized cache counters and outcome evidence.
- WF-102 Guarded run: execute the same controlled task with startup-context control enabled; exclude irrelevant full skill content; preserve complete selected required and safety-critical instructions; capture equivalent counters and outcomes.
- WF-103 Comparison: validate control equivalence, calculate provider-specific cache-token reduction, and reject comparisons whose task, model, repository state, or quality differs materially.
- WF-104 Safe uncertainty: when relevance cannot be determined safely, include the potentially required full skill, record the reason, and accept lower or zero savings.
- WF-105 Rollback: when quality, compliance, privacy, compatibility, or startup performance fails, disable the intervention and restore baseline behavior without changing original skills.
- Failure path: if no supported pre-context or install-time control exists, Engineering stops delivery commitment and returns OQ-001 for product rescoping.
- Failure path: missing or changed provider counters make the run unmeasurable; the product reports no result rather than estimating.
- Failure path: any omitted required instruction or failed quality check invalidates the token-saving result regardless of its percentage.

## Requirements and Business Rules
- BR-101: The MVP must prevent irrelevant full skill content from entering startup context for guarded runs.
- BR-102: Every skill classified as required or safety-critical must be loaded from its complete authoritative source without lossy rewriting.
- BR-103: When relevance is uncertain, correctness and instruction compliance take precedence over token reduction.
- BR-104: Claude Code and Codex measurements must be evaluated separately using their native cache-token fields.
- BR-105: A comparison is valid only for the same declared task, provider, model, and materially equivalent repository state and quality outcome.
- BR-106: The MVP must calculate token reduction from raw baseline and guarded counters and must not silently convert tokens into billed cost.
- BR-107: Measurement artifacts must exclude prompts, source content, credentials, raw responses, and full skill bodies.
- BR-108: Original skill files and unrelated provider configuration must remain unchanged; the intervention must be reversible.
- BR-109: A compact skill index must not be presented as the accepted customer solution (DEC-004).
- BR-110: A 30% effectiveness claim may be made only for a named provider/model/task sample whose controlled comparison and quality gates pass.

## Data, Integrations, and Non-Functional Requirements
- Measurement data: Claude `cache_read_input_tokens` and `cache_creation_input_tokens`; Codex `cached_input_tokens`; provider/model/version; task ID; repository-state marker; baseline/guarded mode; timestamps; quality outcome; startup duration; included/excluded skill identifiers when observable.
- Formula: `(baseline_cache_tokens - guarded_cache_tokens) / baseline_cache_tokens * 100`, valid only when baseline is greater than zero and comparison controls pass.
- Integrations: Claude Code and Codex startup or install-time skill-loading surfaces; provider-local usage records; Context Guard CLI/reporting; repository-local benchmark fixtures.
- NFR-101 Safety: required and safety-critical instruction compliance must not regress.
- NFR-102 Privacy: core control and measurement remain local; sanitized receipts contain no user prompt, source, credential, raw response, or full skill body.
- NFR-103 Determinism: identical declared inputs and relevance decisions produce the same inclusion outcome.
- NFR-104 Reversibility: disabling the intervention restores baseline behavior and original skills remain intact.
- NFR-105 Compatibility: provider adapters isolate schema and caching differences; cross-provider counters are not aggregated as equivalent.
- NFR-106 Auditability: every claim traces to raw numeric counters, comparison controls, and quality evidence.
- NFR-107 Performance: startup overhead is measured; Product and Engineering set the acceptance threshold before delivery readiness (OQ-003).
- NFR-108 Fail-safety: unsupported schemas, missing counters, or uncertain relevance yield an explicit unmeasurable or full-load result, not silent omission.

## Dependencies, Risks, and Constraints
- DEP-001 Critical: a supported point must exist before full skill content enters startup context. Existing Context Guard tool-operation hooks may execute too late.
- DEP-002 High: Product and QA must define repeatable pilot tasks and objective task-completion/instruction-compliance checks.
- DEP-003 Medium: additional representative repositories are required before generalizing effectiveness beyond this pilot.
- RISK-001: provider interception is infeasible; mitigation is an explicit feasibility spike and product rescoping rather than an unsupported runtime promise.
- RISK-002: relevance control omits required instructions; mitigation is complete authoritative loading, full-load on uncertainty, quality gates, and immediate rollback.
- RISK-003: the pilot misses 30%; mitigation is causal analysis and claim/scope revision through a new product decision.
- RISK-004: skill content is not the dominant startup source; mitigation is falsifiable contribution analysis and no silent expansion to unrelated context sources.
- RISK-005: provider schemas or cache semantics change; mitigation is versioned adapters and comparison invalidation.
- RISK-006: run variance creates misleading savings; mitigation is repeated controlled runs and published invalidation rules.
- RISK-007: local session records expose sensitive content; mitigation is field projection, privacy tests, and local-only receipts.
- Constraints: no compact skill index as the customer solution, no central telemetry, no exact billing claim, and no modification of authoritative skills.

## Decisions, Assumptions, and Open Questions
- Accepted DEC-002: active Claude Code and Codex developers are the MVP customer; the promise is pre-work cache reduction without losing instructions or evidence.
- Accepted DEC-003: success is at least 30% fewer normalized cache tokens for the same task/model, using this repository as the initial pilot.
- Accepted DEC-004: irrelevant full skill content must be prevented, complete required/safety instructions preserved, and a compact skill index excluded as the customer solution.
- Proposed DEC-005: use a measurable cache-token and instruction-preservation headline instead of an unverified cost-savings headline. Owner: Product. Impact: high launch accuracy. Resolution/next step: approve or revise during PRFAQ readiness review.
- Proposed DEC-006: use a measurement-only phase followed by a guarded local experiment; make no broader effectiveness claim until provider-specific gates pass. Owner: Product and QA. Impact: high evidence credibility. Resolution/next step: approve before release slicing.
- Assumption A-101: current local counters remain sufficiently stable for the pilot; they do not establish billed cost.
- Hypothesis H-101: unnecessary skill content materially contributes to startup cache usage; this remains falsifiable.
- OQ-001: which supported mechanism controls inclusion before context assembly? Owner: Engineering. Impact: critical feasibility. Resolution/next step: complete a provider-surface feasibility investigation before delivery commitment; rescope if no supported boundary exists.
- OQ-002: what observable evaluator proves equivalent task and instruction outcomes? Owner: Product and QA. Impact: high validity. Resolution/next step: define during QA strategy and test-case synthesis before readiness review.
- OQ-003: what startup-overhead threshold is acceptable? Owner: Product and Engineering. Impact: medium usability. Resolution/next step: measure baseline and set the threshold before readiness review.
- OQ-004: which repositories extend the evidence beyond this pilot? Owner: Product. Impact: medium generalizability. Resolution/next step: select after feasibility is proven and before a public effectiveness claim.

## Success Measures
- SM-101 Primary: at least 30% fewer normalized cache tokens on valid same-task comparisons. Claude uses cache-read plus cache-creation tokens; Codex uses cached-input tokens. Results remain provider/model-specific.
- SM-102 Quality: the guarded run completes the same task and passes every required and safety-critical instruction check; failure invalidates SM-101.
- SM-103 Evidence: each result identifies task, provider, model, repository state, baseline and guarded counters, calculation, quality outcome, and invalidation status.
- SM-104 Privacy: receipts contain none of the prohibited session-content categories defined by BR-107.
- SM-105 Reversibility: disabling the MVP restores baseline behavior without modifying authoritative skills or unrelated provider configuration.
- SM-106 Repeatability: repeated controlled runs produce a distribution stable enough for QA to support or reject the 30% claim; exact repetition count and variance limit are set in QA strategy.
- SM-107 Performance: startup overhead remains within the threshold established through OQ-003.
- Claim boundary: passing measures demonstrate local cache-token reduction for the named sample, not verified currency-cost reduction or universal effectiveness.

## Source Coverage
- `specs-refiniment/003-context-guard-product-goal/discovery.md`: validated customer, problem evidence, MVP, alternatives, value proposition, workflows, requirements, measures, risks, launch posture, and source limitations.
- `specs-refiniment/003-context-guard-product-goal/business-context.md`: overarching Context Guard goal, actors, existing workflows, rules, and prior acceptance logic.
- `specs-refiniment/003-context-guard-product-goal/decision-log.md`: DEC-001 through DEC-006, including accepted customer/MVP/metric constraints and proposed PRFAQ positioning/launch decisions.
- `specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon`: lifecycle authority and completed discovery predecessor.
- `README.md`, `docs/index.md`, `specs/001-context-guard/requirements.md`, and `specs/002-compact-runtime/requirements.md`: consumed indirectly through the fully traced discovery package for existing product boundaries.
- Sanitized local provider-usage evidence under `~/.claude` and `~/.codex`: consumed through discovery; it confirms large startup/cache counters but does not isolate skill causation or billed cost.
- No external market evidence, customer cohort study, willingness-to-pay data, or provider contract was supplied; the package therefore describes a developer-local pilot rather than a market-wide launch.

## Press Release
### Draft — pilot announcement, not public availability

### Context Guard targets AI-agent cache waste before coding work begins

Developers using Claude Code and Codex can spend substantial cache tokens before productive work starts. Context Guard is preparing a local MVP pilot designed to keep irrelevant full skill content out of startup context while preserving every required and safety-critical instruction in its original, complete form.

Today, developers can inspect provider-local usage records after context has already been consumed, rely on probabilistic instructions, or build provider-specific wrappers. None provides a deterministic, reversible boundary that both reduces startup skill context and proves required instructions were preserved.

The Context Guard pilot will compare the same controlled task with and without startup-context control. It will report provider-specific cache-token counters, quality outcomes, and the exact comparison conditions locally. The MVP target is at least 30% fewer normalized cache tokens, but a result counts only when the guarded run completes the same task and passes every required instruction check.

Context Guard keeps the core experience local: no centralized session collector, no prompt or source capture in benchmark receipts, no rewriting of authoritative skill files, and a safe return to full loading whenever relevance is uncertain.

The first pilot will run in the Context Guard repository on Claude Code and Codex. Broader availability depends on proving that each provider exposes a supported control point before startup context is assembled, demonstrating repeatable savings, preserving task quality and safety instructions, and meeting privacy and startup-performance gates. The pilot measures cache tokens; it does not claim a verified percentage reduction in provider bills.

## Customer FAQ
### What problem does this solve?
AI coding-agent sessions can consume substantial cache tokens before useful work begins. Local logs reveal that consumption afterward but do not prevent irrelevant full skill content from entering startup context.

### Who is the MVP for?
Developers actively using Claude Code or Codex. The first evidence comes from a local pilot in this repository; enterprise administration and generalized market claims are outside MVP.

### What changes for a developer?
For a guarded run, irrelevant full skill content stays out of startup context while every skill determined to be required or safety-critical is loaded completely. The developer receives a local comparison of baseline and guarded cache tokens plus the quality result.

### Will Context Guard summarize or rewrite my skills?
No. Authoritative skill files remain unchanged, and required skills load in full. DEC-004 also excludes a compact skill index as the customer-facing solution.

### What happens when Context Guard is unsure whether a skill is required?
It favors correctness: the full potentially required skill is included, the uncertainty is recorded, and the run may show lower or no savings.

### Does this guarantee 30% lower cost?
No. The pilot target is 30% fewer normalized cache tokens for controlled same-task runs. Local logs do not currently establish provider-billed currency cost, and results may differ by provider, model, task, and required skill set.

### Why is this better than usage logs or agent instructions?
Usage logs are retrospective, and agent instructions are probabilistic. The MVP aims for a local, deterministic, reversible inclusion boundary with controlled measurement and instruction-preservation evidence.

### What data leaves my machine?
None is required by the MVP. Sanitized receipts retain counters and reproducibility metadata, not prompts, source content, credentials, raw responses, or full skill bodies.

### Can I turn it off?
Yes. Rollback must restore baseline behavior without changing original skills or unrelated provider configuration.

### What limitations remain?
Provider feasibility is not yet proven, skill content may not be the dominant startup source, additional repositories are not yet selected, and the quality/latency thresholds must be finalized before readiness.

## Internal FAQ
### Why invest in this MVP?
It tests a concrete extension of Context Guard's mission: prevent avoidable model-facing context before it is consumed while preserving local evidence and developer control. It also turns an observed cache-usage concern into a falsifiable, provider-specific product claim.

### What is the business objective?
Demonstrate at least 30% normalized cache-token reduction on valid pilot comparisons without degrading task completion or required/safety instruction compliance.

### What must Engineering prove first?
That Claude Code and Codex expose a supported pre-context or install-time control capable of preventing irrelevant full skill content before model context assembly. If not, the initiative returns for product rescoping.

### What exactly is in MVP?
Provider-specific measurement, startup skill inclusion control, complete required-skill preservation, same-task comparison, sanitized receipts, quality gates, local pilot operation, bypass, and rollback.

### What is explicitly not in MVP?
A compact skill index as the customer solution, universal context optimization, exact billing attribution, centralized telemetry, enterprise controls, semantic retrieval, and modification of authoritative skills.

### How is success calculated?
Claude: baseline versus guarded `cache_read_input_tokens + cache_creation_input_tokens`. Codex: baseline versus guarded `cached_input_tokens`. The task, model, provider, repository state, and quality must be materially equivalent.

### Who owns the pilot?
Product owns scope and claims; Engineering owns feasibility and implementation behavior; QA owns the comparison and quality gates; Security/Privacy owns receipt minimization; the repository maintainer owns local enablement and rollback.

### What is the rollout?
Phase 1 is measurement-only baseline collection. Phase 2 is a guarded experiment for named tasks. Broader release requires provider-specific go gates and explicit approval of DEC-005 and DEC-006.

### What blocks launch?
No supported pre-context control, failed quality or safety checks, unrepeatable measurement, privacy leakage, unacceptable startup overhead, or failure to meet the accepted product gate without an approved scope/claim revision.

### How do we support incidents?
Disable guarded behavior, restore baseline loading, preserve sanitized failure evidence, assign the failure to Engineering or QA, and require review before re-enablement.

## Business Requirements
| ID | Business Requirement | Priority | Business Value | Observable Acceptance Logic | Owner / Source |
| --- | --- | --- | --- | --- | --- |
| BR-101 | Prevent irrelevant full skill content from entering guarded startup context | Must | Reduce avoidable pre-work cache usage | Given a controlled task with an irrelevant skill, when guarded startup runs, then that full skill body is absent from model startup context evidence | Engineering; DEC-004 |
| BR-102 | Preserve complete authoritative required and safety-critical skills | Must | Maintain correctness and trust | Given a task requiring a named skill, when guarded startup runs, then the complete authoritative skill is available and required checks pass | Engineering and QA; DEC-004 |
| BR-103 | Compare baseline and guarded runs under equivalent controls | Must | Produce credible evidence | Given a comparison, then task, provider, model, repository state, counter fields, and quality outcome are recorded and materially equivalent | QA; DEC-003 |
| BR-104 | Achieve at least 30% fewer normalized cache tokens | Must | Validate primary customer value | Given a valid provider-specific pilot comparison, then the accepted formula reports reduction greater than or equal to 30% | Product and QA; DEC-003 |
| BR-105 | Invalidate savings when task or instruction quality regresses | Must | Prevent harmful optimization | Given any failed required check or materially different outcome, then the run cannot pass the effectiveness gate | QA; SM-102 |
| BR-106 | Keep measurement and control local with sanitized receipts | Must | Preserve privacy and adoption trust | Given a generated receipt, then prohibited prompt/source/credential/raw-response/full-skill content is absent | Security/Privacy; BR-107 |
| BR-107 | Provide safe full-load behavior on relevance uncertainty | Must | Avoid missing instructions | Given unresolved relevance, when guarded startup evaluates the skill, then it includes the full skill and records the uncertainty | Engineering; BR-103 |
| BR-108 | Provide non-destructive bypass and rollback | Must | Make pilot adoption reversible | Given an intervention failure, when rollback runs, then baseline behavior returns and original skills/configuration remain unchanged | Engineering; NFR-104 |
| BR-109 | Report token reduction separately from billed cost | Must | Prevent misleading claims | Given a result, then it names raw token fields and does not state verified currency savings | Product; DEC-005 |
| BR-110 | Isolate Claude Code and Codex semantics | Must | Avoid invalid aggregation | Given results from both providers, then each uses its native fields and is reported separately by provider/model | Engineering and QA; BR-104 |
| BR-111 | Measure startup overhead | Should | Ensure net developer value | Given baseline and guarded runs, then startup duration is captured and evaluated against the threshold established through OQ-003 | Engineering and QA |
| BR-112 | Limit broader claims to representative evidence | Should | Protect product credibility | Given only the initial repository pilot, then public materials identify it as a pilot and do not claim universal effectiveness | Product; DEP-003 |

## Launch Risks
| ID | Launch Risk | Likelihood | Impact | Go/No-Go Signal | Mitigation / Resolution | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| RISK-001 | Provider lacks a supported pre-context control | High | Critical | No supported boundary before full skill content enters context | No-go; complete feasibility investigation and rescope rather than relying on a late hook | Engineering |
| RISK-002 | Required or safety-critical instructions are omitted | Medium | Critical | Any failed instruction or task-quality check | No-go; full-load on uncertainty, complete authoritative loading, rollback, root-cause review | Engineering and QA |
| RISK-003 | Valid pilot runs do not reach 30% | Medium | High | Provider-specific distribution remains below target | No-go for current claim; analyze contribution and obtain a new product scope/metric decision | Product |
| RISK-004 | Skill content is not the dominant source | Medium | High | Guarded exclusion yields little change | Keep hypothesis falsifiable; do not silently broaden MVP; return to discovery if needed | Product and Engineering |
| RISK-005 | Provider usage fields drift | Medium | High | Missing or discontinuous cache counters | Invalidate comparison, update versioned adapter, rerun baseline | Engineering |
| RISK-006 | Run variance makes 30% unreliable | High | High | Identical controls yield unstable distribution | Repeat runs, set variance/confidence rules in QA strategy, block claim until repeatable | QA |
| RISK-007 | Sanitized receipt leaks session content | Low | Critical | Prompt, source, credential, raw response, or full skill appears | No-go; privacy tests, local deletion of affected receipt, security review | Security/Privacy |
| RISK-008 | Startup overhead erases benefit | Unknown | Medium | Guarded startup exceeds the OQ-003 threshold | Tune or rescope; no broader rollout until threshold passes | Product and Engineering |
| RISK-009 | Pilot does not generalize | High | Medium | Results exist only for this repository/task set | Label evidence narrowly; select additional repositories before public effectiveness claims | Product |
