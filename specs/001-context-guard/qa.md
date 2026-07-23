---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-context-guard"
  artifact: "qa.md"
  path: "specs/001-context-guard/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/001-context-guard/_ai_sdlc/state.toon"
  decision_log: "specs/001-context-guard/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-07-23"
  updated_at: "2026-07-23"
  trace_ids:
    - "AC-010"
    - "TC-001"
    - "TC-002"
    - "TC-013"
    - "TC-015"
    - "TC-017"
    - "TC-018"
    - "TC-025"
  related_artifacts:
    - "specs/001-context-guard/decision-log.md"
    - "specs/001-context-guard/design.md"
    - "specs/001-context-guard/requirements.md"
    - "specs/001-context-guard/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "review"
---

# QA

## Change Summary
New capability: introduces the `context-guard` local CLI/policy engine package (context_guard/) from scratch, including provider adapters for Claude Code and Codex, deterministic file/command/search policy rules, layered YAML config, JSONL audit logging, and install/validate/test/doctor/report/init CLI subcommands. This is a new, standalone tool; it does not modify any existing application code (repository was empty prior to this change).

## Acceptance Scenarios
- AC-001 through AC-010 (see requirements.md) exercised via the automated suite mapped in test-cases.md; all must pass before this feature is considered acceptance-ready.
- Manual smoke: install into a scratch Claude Code project config and a scratch Codex config, trigger a real oversized-file-read and a real unbounded `docker compose logs` invocation (or fixture-equivalent if Docker is unavailable), and confirm the block message and suggestion appear as expected.
- Manual smoke: flip `mode: enforce` to `mode: observe` in repo policy and confirm previously-blocked operations now allow while still logging the would-block decision.

## Regression Targets
No pre-existing product to regress against (greenfield repo). Regression scope for future changes to this feature: re-run the full pytest suite (unit, adapter/contract, audit, CLI, perf) and re-validate install idempotency (TC-017, TC-018) whenever adapters, policy schema, or CLI subcommands change, since those are the highest-risk-of-silent-breakage surfaces (provider schema coupling and non-destructive install guarantees).

## Risk Notes
- Highest risk: false positives blocking legitimate developer work, eroding trust before the tool proves value — mitigated by shipping `observe` as the default mode (see design.md Risks and Tradeoffs) and by TC-001/TC-002 coverage of the observe-vs-enforce distinction.
- Provider hook schema drift risk is isolated to adapters and covered by fixture-based contract tests (TC-013-TC-015), but real-world drift can only be caught once fixtures are refreshed against actual provider releases (see test-cases.md Open Gaps).
- Latency risk (Python cold-start) could threaten the <100ms median NFR on constrained hardware; TC-025 is the automated guardrail, but the PRFAQ open question about daemon architecture remains unresolved for a future phase.
- Because this is explicitly not a security product, there is a residual risk of teams over-trusting the fail-closed convenience rules as security controls; mitigated by explicit documentation and `doctor`/`report` messaging (design.md Security Considerations).

## Validation Commands
- `python3 -m pytest tests/` — full automated suite (unit, adapters, audit, CLI, excluding perf marker by default).
- `python3 -m pytest tests/ -m perf` — latency benchmark (TC-025).
- `context-guard validate` — policy schema and hook-install validation (AC-008).
- `context-guard test` — fixture-based smoke check of the 5 required high-cost patterns (AC-009).
- `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py specs/001-context-guard` and `validate_spec.py specs/001-context-guard` — SDD structural gates.
- Defer exact command selection for a given change to `$ai-sdlc-validation`.

## Manual Checks
- Manually run `context-guard install claude` and `context-guard install codex` against real local Claude Code / Codex config locations in a disposable test project (not the user's real projects) and visually confirm the generated hook entries look correct and non-destructive.
- Manually trigger one real oversized file read and one real unbounded log command through an actual Claude Code or Codex session (if available) to confirm end-to-end behavior beyond fixture simulation, per the PRFAQ's own worked examples.
- Manually inspect a sample JSONL audit log to confirm no full prompt/file/output/env/secret content is present by default.

## Signoff
Signoff requires: all automated tests in test-cases.md passing, `context-guard validate` and `context-guard test` passing, AC-001 through AC-010 demonstrated, and at least one manual smoke check performed against a real (non-fixture) Claude Code or Codex hook invocation where available. Owner: Dev (implementer); reviewer: user/PM before pilot rollout per PRFAQ Phase 2.

