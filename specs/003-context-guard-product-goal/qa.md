---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "qa.md"
  path: "specs/003-context-guard-product-goal/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs/003-context-guard-product-goal/decision-log.md"
  status: "active"
  owner: "QA"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-001"
    - "AC-063"
    - "TC-001"
    - "TC-063"
  related_artifacts:
    - "specs/003-context-guard-product-goal/branch-plan.md"
    - "specs/003-context-guard-product-goal/change-impact.md"
    - "specs/003-context-guard-product-goal/decision-log.md"
    - "specs/003-context-guard-product-goal/design.md"
    - "specs/003-context-guard-product-goal/plan.md"
    - "specs/003-context-guard-product-goal/requirements.md"
    - "specs/003-context-guard-product-goal/tasks.md"
    - "specs/003-context-guard-product-goal/test-cases.md"
    - "specs/003-context-guard-product-goal/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "active"
    - "slice-5"
    - "slice-4"
    - "slice-3"
    - "slice-1"
---

# QA

## Change Summary
Extend the completed policy, inventory, receipt, Claude-profile, quality, and Claude-measurement slices with current-contract Codex user-skill inventory, reversible explicit profile control, exact or cumulative cached-input measurement, and provider-specific qualification.

## Acceptance Scenarios
AC-001–AC-063 map one-to-one to TC-001–TC-063. Slice 5 must prove HOME/.agents/skills discovery, rejection of stale HOME/.codex/skills inventory, exact irrelevant-skill disable entries, explicit HOME/.codex profile placement, persistent leases, byte-exact compare-and-swap restoration, dead-owner recovery, user-edit preservation, sanitized receipts, exact turn.completed extraction, monotonic cumulative deltas, matching quality context, exact paired reductions, complete five-by-three qualification, and the conjunctive Codex 30 percent gate.

## Regression Targets
All existing policy, inventory, receipts, Claude guarded profile, quality runner, Claude measurement, compact runtime, adapters, hooks, and CLI tests remain green. Codex commands never launch a provider, scan HOME, read undeclared files, edit the main config, mutate undeclared profiles, pool providers, delete outliers, or authorize incomplete, stale, reset, or corrupt evidence.

## Risk Notes
P0 risks are stale Codex path assumptions, loss of an existing profile, concurrent profile writers, restoration over user edits, cumulative-counter reset or double counting, session/model drift, quality-context mismatch, raw log or TOML leakage, and mathematically incorrect threshold decisions. Exact roots, dedicated profiles, persistent leases, byte snapshots, compare-and-swap, explicit boundaries, strict context matching, rational arithmetic, full population requirements, minimized evidence, and fault-injection tests mitigate them.

## Validation Commands
PLANNED: focused inventory, Codex profile, Codex measurement, and CLI tests; complete repository suite; git diff --check through the canonical validation plan. Strict docs and all full-flow SDD gates run supplementally. Live Codex paired execution is excluded from deterministic validation.

## Manual Checks
Inspect docs/codex-profile.md, docs/codex-measurement.md, and minimized receipts. Confirm the generated profile contains only sorted exact [[skills.config]] disable entries; the main config is untouched; only an explicit JSONL file or declared cumulative boundaries are consumed; and no raw line, path, prompt, response, source, credential, environment value, full skill body, baseline TOML, or billed-cost inference is persisted or printed.

## Signoff
Slice 5 deterministic signoff requires focused and full tests, profile concurrency and recovery fault injection, exact and cumulative measurement boundaries, statistical threshold tests, privacy checks, strict docs, SDD gates, and current validation evidence. A real 30 percent Codex result requires a later live five-by-three pilot and is not claimed by unit tests.
