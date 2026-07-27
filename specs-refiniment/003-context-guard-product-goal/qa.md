---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "qa.md"
  path: "specs-refiniment/003-context-guard-product-goal/qa.md"
  workspace: "refinement"
  skill: "ai-sdlc-qa"
  flow_mode: "full"
  state_file: "specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/003-context-guard-product-goal/decision-log.md"
  status: "review"
  owner: "Product and QA"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-301"
    - "AC-316"
    - "BR-101"
    - "BR-112"
    - "BR-201"
    - "BR-212"
    - "DEC-018"
    - "DEC-024"
    - "DEC-026"
  related_artifacts:
    - "specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md"
    - "specs-refiniment/003-context-guard-product-goal/backlog.md"
    - "specs-refiniment/003-context-guard-product-goal/business-context.md"
    - "specs-refiniment/003-context-guard-product-goal/change-impact.md"
    - "specs-refiniment/003-context-guard-product-goal/decision-log.md"
    - "specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md"
    - "specs-refiniment/003-context-guard-product-goal/delivery-spec.md"
    - "specs-refiniment/003-context-guard-product-goal/discovery.md"
    - "specs-refiniment/003-context-guard-product-goal/goal-capability-map.md"
    - "specs-refiniment/003-context-guard-product-goal/prfaq.md"
    - "specs-refiniment/003-context-guard-product-goal/qa-strategy.md"
    - "specs-refiniment/003-context-guard-product-goal/release-slicing.md"
    - "specs-refiniment/003-context-guard-product-goal/requirements-readiness.md"
    - "specs-refiniment/003-context-guard-product-goal/research.md"
    - "specs-refiniment/003-context-guard-product-goal/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-qa"
    - "qa"
    - "review"
    - "gap-003"
    - "quality-evaluator"
---

# qa.md

## Feature Summary
- QA boundary: validate Context Guard's deterministic relevance, supported provider controls, local receipt lifecycle, recovery, quality-first measurement, net-value gates, and bounded rollout for Claude Code and Codex.
- The plan covers DSR-101 through DSR-602, all 24 MVP stories, 48 story acceptance criteria, 48 adverse/primary scenarios, and six release slices.
- Current signoff is **plan ready, execution pending**. No provider qualification, 30% result, or release pass is claimed.

## Actors and Stakeholders
- QA owns fixtures, oracles, hard gates, invalidation, valid-pair accounting, and evidence signoff.
- Engineering supplies deterministic components, provider fixtures, recovery controls, metrics adapters, and focused automated validation.
- Security/Privacy signs receipt minimization, permissions, lifecycle, and forbidden-content coverage.
- Product/Delivery sign provider results, net value, scope bounds, and combined rollout. Developers/maintainers exercise guarded startup, policy diagnostics, receipts, bypass, and restore.

## Scope and Boundaries
- In scope: policy/inventory/classification; Claude and Codex supported surfaces; actual-state verification; lease/snapshot/CAS recovery; receipts; three frozen fixtures; QG-301–QG-309; provider windows; paired statistics; overhead/prompts; evidence package.
- Out of scope: unqualified IDE/desktop, Claude plugins, repository-local Codex filtering, enterprise/central telemetry, semantic classification, billed-cost claims, and generalized effectiveness.
- Claude and Codex are tested and signed independently; combined MVP requires both.

## Workflows and Failure Paths
- Test the complete WF-DS01–WF-DS09 chain and each transition independently.
- Every primary path has an adverse twin: unsupported version, duplicate identity, invalid policy, uncertain classification, state mismatch, contention, crash, user edit, receipt interruption/leak, fixture mismatch, gate failure, event drift, negative result, performance breach, and one-provider failure.
- Safe outcome is full load, invalid/unmeasurable evidence, preserved diagnostics, and no unsupported claim.

## Requirements and Business Rules
- Coverage authority: DSR-101–DSR-602; BR-101–BR-112 and BR-201–BR-212; AC-S101-1 through AC-S604-2; BA AC-301–AC-316.
- Only exact irrelevant may reduce visibility. Quality precedes tokens. Missing evidence is never zero. Negative valid results remain. Providers never pool. Net-value and privacy failures are hard gates.
- QA may invalidate attempts; invalid attempts stay auditable and additional attempts may reach the valid-pair target.

## Data, Integrations, and Non-Functional Requirements
- Test inputs: pinned provider/client/model versions; authoritative inventories/digests; policy v1/v2/future/invalid fixtures; repository/task/inventory fingerprints; sanitized usage-event fixtures; receipt lifecycle fixtures; three frozen tasks.
- Privacy scans prohibit prompt/response/source/credentials/secrets/environment/full-skill content.
- Validate local permission equivalents, atomicity, 30-day retention, target delete, safe pruning, quarantine, single writer, determinism, provider isolation, and restoration.
- Performance gate: p95 <=750 ms, max <=2 s, zero happy-path prompts, at most one unsafe-recovery prompt, excluding provider time.

## Dependencies, Risks, and Constraints
- Slice order controls test availability. Provider contract/live tests require installed qualified versions and local credentials/configuration supplied by the operator; tests must use sanitized non-production data.
- Python 3.10+ is required for the qualification runner.
- Highest risks: instruction loss, user-config overwrite, receipt leakage, counter misattribution, false oracle equivalence, variance/causal overclaim, and stale authority.
- EVID-401 remains the execution package; CONS-401 must close before delivery signoff.

## Decisions, Assumptions, and Open Questions
- Accepted authority runs through DEC-026.
- QA-A01: automated contract/fixture tests precede live-provider attempts. Owner: QA + Engineering. Impact: unsafe or drifted integrations fail early. Resolution/next step: enforce slice entry gates.
- QA-OQ01: exact installed provider versions and live event eligibility are execution-time facts. Owner: Engineering + QA. Impact: a surface may be unmeasurable. Resolution/next step: preflight and record versions/events.
- QA-OQ02: named people and execution environment are not supplied. Owner: Delivery + QA. Impact: no execution date. Resolution/next step: assign before Slice 1 test execution.

## Success Measures
- 100% DSR/story acceptance traceability and at least one primary plus adverse scenario per requirement cluster.
- Zero QG-301–QG-309 failures among valid pairs; complete required/safety instruction preservation.
- Five valid alternating warm-cache pairs per fixture/provider; median >=30%, Q1 >=0%, every fixture median >=0%, with no outlier deletion.
- Receipt privacy/lifecycle, bypass/fallback/recovery, and DEC-018 performance gates pass.
- Evidence package is replayable, provider/version/repository/fixture bounded, and exposes failures.

## Source Coverage
- `specs-refiniment/003-context-guard-product-goal/delivery-spec.md`: DSR requirements, workflows, rules, traceability, and handoff risks.
- `specs-refiniment/003-context-guard-product-goal/user-stories.md`: 48 ACs and 48 scenarios.
- `specs-refiniment/003-context-guard-product-goal/business-context.md`: actors, behavior, rules, and BA ACs.
- `specs-refiniment/003-context-guard-product-goal/release-slicing.md`: test sequencing and exit gates.
- `specs-refiniment/003-context-guard-product-goal/qa-strategy.md`: provider windows, pairing, aggregation, and privacy replay.
- `specs-refiniment/003-context-guard-product-goal/decision-log.md`: accepted authority through DEC-026.
- `specs-refiniment/003-context-guard-product-goal/backlog.md`: scope, stories, tasks, and readiness.
- `specs-refiniment/003-context-guard-product-goal/backlog-gap-review.md`: planning gaps and evidence controls.
- `specs-refiniment/003-context-guard-product-goal/change-impact.md`: DEC-024 impact evidence.
- `specs-refiniment/003-context-guard-product-goal/delivery-gap-review.md`: historical delivery gaps.
- `specs-refiniment/003-context-guard-product-goal/discovery.md`: customer, metric, and constraints.
- `specs-refiniment/003-context-guard-product-goal/goal-capability-map.md`: goals, capabilities, and epics.
- `specs-refiniment/003-context-guard-product-goal/prfaq.md`: requirements and rollout risks.
- `specs-refiniment/003-context-guard-product-goal/requirements-readiness.md`: readiness history.
- `specs-refiniment/003-context-guard-product-goal/research.md`: provider evidence and limitations.
- `specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon`: lifecycle authority.

## Acceptance Scenarios
| Scenario | Actor | Setup | Action | Expected Result | Evidence | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| QA-101 | Developer/adapter | Supported and unsupported pinned clients | Run preflight/inventory | Stable identities for supported; no mutation/full load for unsupported/duplicate/stale | Contract fixtures + live smoke | Critical provider drift |
| QA-102 | Maintainer | Valid/invalid/v1/v2/future layered policies | Validate/migrate/classify | DEC-024 diagnostics/migration; deterministic outcomes; only exact irrelevant reduces | Unit/property/CLI tests | Critical instruction loss |
| QA-201 | Claude developer | Supported profile, mismatch, contention, crash, user edit | Start/bypass/restore | Verified state or full load; idempotent CAS; unrelated edits preserved | Adapter + recovery tests | Critical config loss |
| QA-202 | Codex developer | CLI/app-server fixtures plus unsupported surface | Start/recover | Pre-thread state verified or full load; lease/recovery safe | Adapter + recovery tests | Critical config loss |
| QA-301 | QA/Security | Normal/interrupted/leaking receipt fixtures | Write/replay/scan | Atomic valid minimized receipt or safe rejection; no forbidden data | Storage/privacy tests | Critical privacy |
| QA-302 | Developer | Active/referenced/aged/corrupt/concurrent receipts | Inspect/delete/maintain | Targeted control; only eligible prune; quarantine/lock safe | Lifecycle tests | High evidence loss |
| QA-401 | QA | Three frozen manifests | Run fresh baseline/guarded attempts and oracles | Comparable correlated attempts; explicit completion/instruction results | Runner automation | Critical false equivalence |
| QA-402 | QA | Passing/failing/mismatched attempts | Apply QG and invalidation | Tokens gated; invalid retained/excluded; retries do not erase | Gate/ledger tests | Critical gate bypass |
| QA-501 | QA | Claude exact/duplicate/drifted events | Extract and aggregate five pairs x fixtures | Dedupe sum or unmeasurable; negatives retained; stats reproducible | Adapter/aggregation + live pilot | High misattribution |
| QA-502 | QA | Codex exact/delta/missing-boundary events | Extract and aggregate five pairs x fixtures | Exact/delta or unmeasurable; no zero substitution; stats reproducible | Adapter/aggregation + live pilot | High misattribution |
| QA-601 | Engineering/Product | Instrumented qualifying runs | Evaluate overhead/prompts | Provider time excluded; any threshold breach fails affected claim | Timing tests + pilot | High negative value |
| QA-602 | Product/Delivery | Complete/incomplete/one-provider packages | Generate review and decide | Bounded evidence; stale gaps block; combined only when both pass | Report validation + human signoff | High overclaim |

## Regression Targets
- Existing Context Guard file/search/command/hook policy behavior remains unchanged when guarded skill optimization is disabled.
- `context-guard init`, `validate`, and `doctor` retain existing v1 behavior while adding DEC-024 v2 behavior; init never overwrites.
- Authoritative skill files and unrelated provider configuration remain byte/digest stable.
- Full-load baseline remains available for unsupported, bypassed, failed, and restored paths.
- Existing local privacy guarantees and no required network dependency remain.
- Provider results and receipts remain isolated; one run/provider cannot alter another's evidence.

## Risk-Based Coverage
| Risk | Severity | Coverage | Release Response |
| --- | --- | --- | --- |
| Required/safety instruction omitted | Critical | QA-102/401/402; explicit skill oracle; digest checks | Invalidate, restore, block provider |
| User configuration overwritten | Critical | QA-201/202 crash/contention/user-edit/CAS | Disable optimization, block provider |
| Receipt leaks raw content | Critical | QA-301/302 forbidden corpus and lifecycle | Quarantine, invalidate, block release |
| Counter/correlation wrong | High | QA-401/402/501/502 | Unmeasurable/invalid; no claim |
| Provider drift | High | QA-101/201/202/501/502 version contracts | Full load; requalify |
| Variance/causal overclaim | High | five pairs, no outlier deletion, Q1/fixture gates, T-018 | Revise/reject claim |
| Overhead erases value | High | QA-601 | Affected surface fails |
| Stale authority/combined overclaim | High | QA-602; CONS-401 | Block handoff/combined result |

## Test Data and Environment
- Python 3.10+ isolated test environment; frozen repository revision and working-tree fingerprint; fixed task/model/fixture manifests.
- Policy corpus: v1, valid v2 at each layer, same-ID override/disable, duplicate ID, unknown field, exact/non-exact identity, future version, migration failure/interruption.
- Provider fixtures: supported/unsupported versions, stable/duplicate inventories, requested/actual match/mismatch, contention, dead owner, user edit, restore failure.
- Receipt corpus: valid, partial, corrupt, referenced, active, aged unreferenced, concurrent, and planted forbidden-content values.
- Usage fixtures: Claude exact/duplicate/drifted events; Codex exact/cumulative/missing/non-monotonic boundaries; correlated and mismatched run IDs.
- Live pilot uses sanitized local repository tasks and credentials/configuration that are never copied into artifacts.

## Validation Commands
- Planned Slice 1: `python -m pytest` focused policy, CLI, inventory, receipt, privacy, and lifecycle suites -> required pass before provider mutation.
- Planned provider slices: focused adapter/profile/lease/recovery contract tests -> required pass before live smoke.
- Planned Slice 3: qualification runner against all three frozen fixtures and injected failures -> required deterministic pass for gate logic.
- Planned Slices 4/5: provider measurement fixture tests plus live eligibility dry run -> required before valid pairs.
- Planned Slice 6: aggregation/report/privacy/replay/performance suites -> required before evidence package.
- Repository-wide regression command will be selected after implementation dependencies are inspected; no command is marked passed in this planning artifact.

## Manual Checks
- Developer: inspect guarded/full-load reason output, bypass, receipt inspect/delete, and one-action recovery wording on supported local clients.
- Maintainer: validate diagnostics identify file, dotted field, stable code, and remediation without raw skill content.
- QA: review frozen task equivalence, instruction oracle meaning, invalid ledger entries, negative values, and provider-separated report.
- Security/Privacy: inspect permission modes and sanitized receipt corpus; verify no remote copy.
- Product/Delivery: review scope labels, failures, causal bounds, per-provider decisions, and combined gate.
- All manual checks are planned, not passed; owners record versioned evidence during their slice.

## Signoff Criteria
- **QA plan status: ready for QA requirements gap review; execution signoff pending implementation.**
- Slice entry requires predecessor exit evidence and focused automated tests.
- Provider qualification requires complete valid-pair package and zero hard failures; unmeasurable or failed results remain honest outcomes.
- Security/Privacy must sign receipt controls; Engineering must sign recovery/actual-state evidence; QA must sign fixtures/gates/measurement; Product/Delivery must sign bounded claims.
- Release signoff is blocked until EVID-401 execution and CONS-401 cleanup complete. This is expected future work, not a planning gap.
