---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "discovery.md"
  path: "specs-refiniment/003-context-guard-product-goal/discovery.md"
  workspace: "refinement"
  skill: "ai-sdlc-working-backwards-discovery"
  flow_mode: "full"
  state_file: "specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  status: "review"
  owner: "Product owner"
  created_at: "2026-07-26"
  updated_at: "2026-07-26"
  trace_ids:
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEP-001"
    - "DEP-002"
    - "DEP-003"
    - "RISK-001"
    - "RISK-002"
    - "RISK-003"
    - "RISK-004"
    - "RISK-005"
    - "RISK-006"
    - "RISK-007"
  related_artifacts:
    - "specs-refiniment/003-context-guard-product-goal/business-context.md"
    - "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-working-backwards-discovery"
    - "discovery"
    - "review"
---

# discovery.md

## Feature Summary
- Confirmed facts: Context Guard is a local developer tool for Claude Code and Codex. Its existing product foundation prevents predictable high-context tool operations and compacts supported high-output commands while preserving complete local evidence.
- Confirmed initiative: extend the MVP to reduce cache tokens consumed before productive work begins by preventing irrelevant skill content from entering startup context while retaining complete required and safety-critical instructions.
- Target customer: developers actively using AI coding agents.
- Product promise: reduce AI-agent cache usage before productive work starts without losing required instructions or evidence (DEC-002).
- Target outcome: at least 30% fewer normalized cache tokens for the same task and model (DEC-003).
- Evidence: `README.md`, `docs/index.md`, existing Stage 1 and Stage 2 requirements, the discovery interview, and local provider usage records.
- Open question/blocker: the provider-compatible mechanism for relevance control is not selected; a compact skill index is explicitly excluded by DEC-004.

## Actors and Stakeholders
- Primary user and beneficiary: a developer who actively uses Claude Code or Codex and bears or cares about token usage.
- System actor: the Claude Code or Codex runtime that assembles startup context, invokes skills, and emits local usage records.
- Product actor: Context Guard, which must measure or consume cache-token evidence and enforce the accepted context boundary locally.
- Configuration owner: the developer or repository maintainer who enables the MVP, selects policy posture, and can roll it back.
- Decision owner: Product owner, responsible for accepting scope, success measures, and residual risk.
- Delivery stakeholders: Engineering owns provider feasibility and relevance-control design; QA owns benchmark repeatability and quality non-regression; Security/Privacy review owns safe treatment of local session metadata.
- Evidence: DEC-002 through DEC-004 and `business-context.md`.
- Open question: no enterprise buyer, approver, or centralized administrator is in the MVP customer definition.

## Scope and Boundaries
- In scope: Claude Code and Codex; developer-local operation; pre-work/startup skill context; normalized cache-token measurement; relevance-based exclusion of irrelevant full skill content; complete loading of selected required skills; same-task benchmarking; explicit quality safeguards; reversible rollout.
- Existing foundation retained: deterministic policy behavior, local artifacts/evidence, no centralized collector, and progressive observe/warn/enforce posture where applicable.
- Out of scope: a compact skill index as the user-facing mechanism; semantic/vector search; centralized employee monitoring; exact provider billing attribution; claims of 30% currency-cost reduction; autonomous deletion or rewriting of skill instructions; weakening safety or mandatory workflow instructions; enterprise governance; unsupported provider runtimes.
- The MVP optimizes startup skill context, not all causes of cache usage. System prompts, conversation history, repository files, tool results, and provider internals remain separate contributors unless explicitly added by later refinement.
- Constraint: provider-controlled startup context may not expose an interception point; feasibility must be proven before solution commitment.

## Workflows and Failure Paths
- WF-D001 Baseline: for a named provider, model, repository state, and task, run the agent without the MVP intervention; capture only usage counters, timing, selected skill identifiers where available, and task-quality outcome.
- WF-D002 Guarded startup: run the same task with the MVP enabled; irrelevant full skill content does not enter startup context, while every selected required or safety-critical skill is loaded in its complete authoritative form.
- WF-D003 Comparison: normalize baseline and guarded runs by provider and model; compare Claude cache-read plus cache-creation tokens or Codex cached-input tokens; report reduction and quality outcome without converting it into provider-billed cost.
- WF-D004 Safe uncertainty: when relevance cannot be determined safely, preserve the required full instruction rather than omit it, record the uncertainty, and report reduced or zero savings for that run.
- WF-D005 Rollback: when quality, instruction compliance, or provider compatibility regresses, disable the intervention and restore baseline startup behavior without changing original skill files.
- Failure paths: missing counters produce an unmeasurable result; changed model/task/repository invalidates direct comparison; provider schema drift blocks measurement; unsafe instruction omission fails the run; unavailable pre-context hooks block runtime prevention and require a different delivery design.

## Requirements and Business Rules
- FR-D001: The MVP must support cache-usage comparison for Claude Code and Codex using provider-specific local counters.
- FR-D002: The MVP must prevent irrelevant full skill content from entering startup context for guarded runs.
- FR-D003: The MVP must load the complete authoritative content of every skill determined to be required for the task, including safety-critical instructions.
- FR-D004: The MVP must produce a same-task, same-model baseline-versus-guarded result with cache-token reduction and quality status.
- FR-D005: The MVP must provide a reversible bypass or rollback when relevance is uncertain or quality regresses.
- BR-D001: Cache-token measurements from different providers or models must not be combined as if they were directly equivalent.
- BR-D002: Token reduction is invalid when task, model, provider version, repository state, or quality outcome differs materially between compared runs.
- BR-D003: Required and safety-critical instructions take precedence over token reduction.
- BR-D004: The product must report measured token changes separately from estimated or billed currency cost.
- BR-D005: The MVP must not present a compact skill index as the accepted user-facing solution (DEC-004).

## Data, Integrations, and Non-Functional Requirements
- Required measurements: Claude `cache_read_input_tokens` and `cache_creation_input_tokens`; Codex `cached_input_tokens`; provider/model identifier; run timestamp; repository revision or state marker; task ID; guarded/baseline mode; quality result; selected skill identifiers where observable.
- Current evidence sources: Claude project session JSONL and stats cache under `~/.claude`; Codex rollout JSONL under `~/.codex/sessions`.
- Data minimization: benchmark records should exclude prompts, source content, credentials, raw assistant output, and full skill content; retain only counters and provenance necessary to reproduce the comparison.
- Integration dependencies: provider startup/context assembly surfaces, skill-selection or skill-loading surfaces, stable local usage schemas, and Context Guard CLI/reporting.
- NFR-D001 Safety: required and safety-critical instruction compliance must not regress.
- NFR-D002 Privacy: core measurement and control must remain local and require no centralized collection.
- NFR-D003 Determinism: the same declared inputs and relevance decision must yield the same inclusion outcome.
- NFR-D004 Reversibility: original skill artifacts remain unchanged and baseline behavior can be restored.
- NFR-D005 Performance: startup overhead must be measured and must not erase the productivity benefit; the numeric limit is TBD.
- NFR-D006 Compatibility: Claude Code and Codex results are evaluated independently because schemas and caching semantics differ.

## Dependencies, Risks, and Constraints
- Dependency: Claude Code and Codex must expose enough local usage data to measure normalized cache tokens; current logs demonstrate counters but not stable contractual schemas.
- Dependency: the delivery design needs a supported point before full skill content enters context. Existing Context Guard tool hooks may occur too late.
- Dependency: a benchmark harness must replay materially equivalent tasks while controlling provider, model, repository state, and quality evaluation.
- Risk: startup context is large, but skill content may be only one contributor; attributing all savings to skills would be misleading.
- Risk: relevance filtering may omit instructions necessary for correctness, lifecycle compliance, or safety.
- Risk: a 30% target may be unreachable for tasks whose required skills dominate startup context.
- Risk: provider caching and pricing semantics may change independently of token counters.
- Constraint: no compact skill index, no exact billing-cost claim, no central telemetry, and no modification of authoritative skills.
- Constraint: benchmark repositories beyond this pilot remain TBA, and the broader quality suite remains TBD.

## Decisions, Assumptions, and Open Questions
- Accepted DEC-002: target active AI-agent developers on Claude Code and Codex; promise pre-work cache reduction without losing instructions or evidence.
- Accepted DEC-003: target at least 30% fewer normalized cache tokens for the same task/model; use this repository as the initial pilot.
- Accepted DEC-004: prevent irrelevant skill content, preserve complete required/safety instructions, and do not use a compact skill index as the user-facing solution.
- Proposed DEC-001 remains the overarching combined prevention-plus-reversible-compaction product goal and requires product-owner status reconciliation with the accepted discovery decisions.
- Assumption A-001: local cache-token counters are sufficiently stable for an MVP benchmark even though they do not prove provider-billed cost.
- Assumption A-002: the pilot can define repeatable tasks in this repository that exercise skill selection before productive work.
- Hypothesis H-001: unnecessary skill content is a material cause of pre-work cache usage. Logs support large startup context and additional cache creation around skill invocation, but do not isolate causal contribution.
- OQ-001: what provider-compatible mechanism can prevent irrelevant full skill content without a compact index? Owner: Engineering. Impact: critical feasibility and scope. Resolution/next step: complete a provider-surface feasibility investigation before delivery commitment; if no pre-context or install-time control exists, return the MVP for product rescoping.
- OQ-002: what exact task-completion and instruction-compliance evaluator constitutes the non-regression gate? Owner: Product and QA. Impact: high; savings cannot be accepted without equivalent quality. Resolution/next step: define the pilot task set and observable checks during QA strategy and test-case synthesis before readiness review.
- OQ-003: what startup-latency budget is acceptable? Owner: Product and Engineering. Impact: medium; excessive overhead can erase user value. Resolution/next step: measure baseline startup latency during the pilot and propose a threshold before delivery readiness.
- OQ-004: which additional repositories and task families represent the target customer after the pilot? Owner: Product. Impact: medium; single-repository evidence cannot support a general effectiveness claim. Resolution/next step: select the broader sample after the pilot demonstrates feasibility and before any public 30% product claim.

## Success Measures
- SM-001 Primary: at least 30% reduction in normalized cache tokens for the same task and model. Claude metric: `cache_read_input_tokens + cache_creation_input_tokens`. Codex metric: `cached_input_tokens`. Results are reported separately by provider and model.
- SM-002 Quality guardrail: guarded runs complete the same task and satisfy all required and safety-critical instruction checks; any failed guardrail invalidates the token-saving result.
- SM-003 Evidence: every reported result identifies provider, model, repository state, task, baseline run, guarded run, raw counters, calculation, and quality outcome.
- SM-004 Privacy: benchmark output contains no prompts, source content, credentials, or full skill bodies.
- SM-005 Reversibility: disabling the intervention restores baseline skill-loading behavior without changing original skill artifacts.
- SM-006 Secondary: startup latency and developer interruptions do not materially worsen; thresholds remain TBD and must be set before readiness review.
- Formula: `reduction_percent = (baseline_cache_tokens - guarded_cache_tokens) / baseline_cache_tokens * 100`, valid only when baseline is greater than zero and comparison controls pass.
- Cost wording: a passing result demonstrates cache-token reduction, not verified currency-cost reduction.

## Source Coverage
- `README.md`: product positioning, commands, existing rollout posture, and local/no-central-service boundary.
- `docs/index.md`: stated customer problem and Stage 1 prevention plus Stage 2 reversible compaction model.
- `specs/001-context-guard/requirements.md`: existing policy actors, rules, privacy constraints, failure behavior, and acceptance criteria.
- `specs/002-compact-runtime/requirements.md`: existing compact-runtime evidence preservation, benchmark controls, parser fallback, and cost-claim constraints.
- `specs-refiniment/003-context-guard-product-goal/business-context.md`: proposed overarching goal, workflows, rules, and known gaps.
- `specs-refiniment/003-context-guard-product-goal/decision-log.md`: DEC-001 through DEC-004.
- User discovery interview on 2026-07-26: target customer, providers, pain, no workaround, MVP intent, metric target, solution exclusion, and confirmations.
- `~/.claude/projects/-Users-mikegorelikov-ai-sdlc-context/6b0fbd8c-7ab1-4d62-be5e-8b57c335af7d.jsonl`: sanitized usage-field inspection showed approximately 27,997 cache-creation and 28,871 cache-read tokens at the first observed assistant usage, before the first logged Skill tool invocation; later skill activity coincided with additional cache creation but does not establish exclusive causation.
- `~/.claude/stats-cache.json`: aggregate cache-token counters are present, while `costUSD` is zero; this supports token measurement but not verified billing-cost attribution.
- `~/.codex/sessions/2026/07/26/rollout-2026-07-26T18-35-22-019f9f11-0c3a-7b73-a366-0526fe8f0354.jsonl`: sanitized token-count inspection showed 22,550 input tokens on the first event and 22,272 cached-input tokens on the second event.
- Source limitation: no prompt, source-code content, credential, or unrelated session payload was consumed as discovery evidence.

## Customer and Problem Evidence
- Customer: developers actively using Claude Code and Codex; the MVP does not yet segment by language, company size, repository type, or purchasing role.
- Reported problem: substantial cache tokens are consumed before productive work begins.
- Reported suspected cause: skill content loaded into context before or around task routing.
- Current workaround: none.
- Consequence: the user perceives unnecessary token consumption and wants to reduce it; exact currency impact is not available from local logs.
- Direct evidence: provider-local records show substantial startup/input cache counters. Claude also shows additional cache creation around explicit skill invocations, but the logs do not isolate which bytes or tokens came from skill metadata, full skill instructions, system prompts, or other context.
- Problem statement: active AI-agent developers lack a local, deterministic control that keeps irrelevant full skill content out of startup context while guaranteeing that required instructions remain complete.
- Evidence gap: customer frequency, breadth beyond the current user, and willingness to adopt or pay are unvalidated.

## Current Process and Alternatives
- Current process: the provider assembles initial context, exposes available skills or routing metadata, and loads or receives full skill instructions according to host behavior; the developer begins work after this context cost is already incurred.
- Current observability: developers can inspect local Claude or Codex records after or during a session, but these counters do not prevent initial context usage or attribute it precisely to individual sources.
- Current workaround: none reported by the user.
- Substitute: repository or global agent instructions can ask the model to load skills selectively, but compliance is probabilistic and the routing catalog itself may consume context.
- Substitute: provider dashboards or local usage logs show consumption after the fact but do not enforce a context boundary.
- Substitute: custom wrappers can reduce selected inputs but are provider-specific, difficult to audit, and may lose required instructions or evidence.
- Switching/adoption barrier: the intervention must operate before context entry, preserve provider compatibility, avoid instruction loss, and require little manual task classification.

## Value Proposition and Business Goals
- Value proposition: For developers actively using Claude Code or Codex who see large cache-token usage before productive work begins, Context Guard provides local, deterministic startup-context control that prevents irrelevant full skill content while preserving complete required instructions and evidence, so they can reduce measurable cache usage without sacrificing task quality, unlike passive usage logs, probabilistic agent instructions, or provider-specific ad hoc wrappers.
- Primary user value: lower cache-token usage before useful work and a reproducible explanation of the reduction.
- Trust value: required and safety-critical instructions remain authoritative and complete; uncertain cases favor correctness over savings.
- Operational value: local, reversible behavior with no central collection and no mutation of original skills.
- Primary business objective: demonstrate at least 30% normalized cache-token reduction on a controlled pilot while passing quality guardrails.
- Secondary objective: create an evidence-backed foundation for broader repositories, providers, and context sources.
- Non-goal: claim a 30% reduction in provider-billed currency cost before pricing-aware validation exists.

## Users, Roles, and Scenarios
- Developer scenario: starts a Claude Code or Codex task in a repository with many installed skills; wants required instructions loaded and irrelevant full skills excluded automatically.
- Benchmark operator scenario: runs controlled baseline and guarded versions of the same task, inspects normalized cache counters, and verifies task/instruction outcomes.
- Repository maintainer scenario: enables the MVP for a pilot, reviews evidence, adjusts or disables it, and preserves existing skill files and provider configuration.
- Engineering scenario: validates whether the provider exposes a pre-context or install-time control point and maps cache-counter semantics without exposing session content.
- Negative scenario: relevance is ambiguous; the MVP preserves the full potentially required skill and reports that the run may not meet the savings target.
- Failure scenario: a required instruction is omitted or task quality changes; the benchmark fails regardless of token reduction and the intervention is rolled back.
- Recovery scenario: disable guarded behavior and rerun the same controlled task under baseline loading.
- Permission rule: developers and maintainers control enablement; the MVP does not autonomously rewrite, delete, or publish skills or session data.

## MVP and Priorities
- Must have: support Claude Code and Codex independently; capture normalized cache-token baselines; prevent irrelevant full skill content from startup context; load complete required and safety-critical skills; same-task comparison; 30% target; quality non-regression gate; local-only evidence; reversible disable/rollback.
- Must have: initial pilot on this repository with named, repeatable tasks and controlled provider/model/repository state.
- Should have: identify which skills were included or excluded without storing their full contents in benchmark evidence; report why a result is invalid or unmeasurable; measure startup latency.
- Could have: broaden to additional repositories and task families; provide aggregate local trend reporting; optimize other startup context sources after separate causal validation.
- Won't have now: compact skill index; centralized dashboard; exact billing-cost calculation; enterprise policy control; semantic/vector retrieval; automatic modification of authoritative skill files; optimization of all conversation or system context.
- MVP completion requires product, engineering, and QA agreement on OQ-001 through OQ-003; discovery does not choose the technical architecture.

## Functional and Non-Functional Needs
- Functional need: define a provider-specific baseline collector that reads only usage metadata required for comparison.
- Functional need: apply a pre-startup or equivalent inclusion decision before irrelevant full skill instructions enter model context.
- Functional need: preserve and load the full original content for required skills without lossy rewriting.
- Functional need: bind each measurement to task, provider, model, repository state, mode, and quality evidence.
- Functional need: calculate provider-specific cache-token reduction and clearly distinguish invalid comparisons.
- Functional need: expose a safe bypass and restore baseline behavior.
- Non-functional need: deterministic inclusion for declared inputs, local privacy, compatibility with both providers, bounded startup overhead, auditability, and no regression in required/safety instruction compliance.
- Non-functional need: do not rely on provider-billed cost fields; pricing and cache semantics may differ by provider and model.
- Verification need: create explicit test cases for irrelevant skill exclusion, required skill preservation, ambiguous relevance, schema drift, missing usage data, quality regression, and rollback.

## Operations, Launch, and Support
- Launch shape: developer-local pilot in this repository, evaluated separately on Claude Code and Codex before broader release.
- Phase 1 measurement: collect baseline metadata and validate repeatability without changing startup behavior.
- Phase 2 guarded experiment: enable relevance control for named tasks with explicit quality checks and immediate rollback.
- Go criterion: at least 30% cache-token reduction on valid controlled comparisons, no required/safety instruction regression, and reproducible evidence.
- No-go criterion: unavailable pre-context control, invalid comparisons, instruction loss, material task-quality regression, unacceptable startup overhead, or privacy leakage.
- Support owner: Engineering for provider/schema failures; QA for benchmark invalidity; Product for scope and metric decisions.
- Documentation need: explain counters, comparison formula, limitations, privacy boundary, bypass, rollback, and why measured tokens are not billed cost.
- Monitoring: local benchmark receipts and error reasons only; no centralized telemetry in MVP.
- Incident handling: disable intervention, retain sanitized evidence, restore baseline, and require review before re-enablement.

## Discovery Risks and Dependencies
| ID | Risk or Dependency | Likelihood | Impact | Warning Signal | Mitigation / Fallback | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| RISK-001 | Available hooks occur after startup context is already assembled | High | High | Cache counters rise before Context Guard can act | Feasibility spike; evaluate supported install-time or host-native loading control; stop rather than promise runtime prevention | Engineering |
| RISK-002 | Required or safety-critical skill instructions are excluded | Medium | Critical | Task or compliance check differs from baseline | Correctness-first fallback, full-load on uncertainty, quality gate, immediate rollback | Engineering and QA |
| RISK-003 | 30% target is not reached for representative tasks | Medium | High | Valid guarded runs remain below target | Attribute sources, narrow claim, revise MVP only through product decision | Product |
| RISK-004 | Skill content is not the dominant startup-context source | Medium | High | Excluding irrelevant skills produces little reduction | Instrument contribution where possible; treat H-001 as falsifiable; do not broaden scope silently | Product and Engineering |
| RISK-005 | Provider token schemas or cache semantics change | Medium | Medium | Missing fields or discontinuous counters | Version adapters, invalidate incompatible comparisons, retain raw numeric provenance | Engineering |
| RISK-006 | Benchmark variance creates misleading savings | High | High | Repeated identical runs vary materially | Multiple controlled runs, fixed task/model/revision, publish distribution and invalidation rules | QA |
| RISK-007 | Local logs expose sensitive session data | Low | High | Benchmark artifact contains prompts, source, or credentials | Project only required numeric fields; privacy tests; local-only storage | Security/Privacy |
| DEP-001 | Provider-compatible pre-context inclusion control | Unknown | Critical | No documented interception or install-time path | Architecture and provider feasibility investigation before delivery commitment | Engineering |
| DEP-002 | Repeatable quality evaluator and pilot task set | Open | High | Token savings cannot be paired with equivalent outcomes | QA strategy and test-case synthesis; OQ-002 must be resolved | QA and Product |
| DEP-003 | Additional representative repositories | TBA | Medium | Pilot result does not generalize | Treat this repository as pilot only; select broader sample before public effectiveness claims | Product |
