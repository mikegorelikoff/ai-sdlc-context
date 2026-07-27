---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "decision-log.md"
  path: "specs/003-context-guard-product-goal/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs/003-context-guard-product-goal/decision-log.md"
  status: "draft"
  owner: "Engineering"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "decision-log"
    - "draft"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-07-27 | accepted | Engineering | Implement the first vertical as a backward-compatible policy-v2 extension in policy_config.py | Existing loader is the narrowest reversible subsystem and DEC-024 fixes semantics | new module; replace v1; extend loader; accepted: extend loader | requirements.md; design.md; tasks.md; context_guard/policy_config.py | DEC-024; DEC-027; AC-001–AC-006; TC-001–TC-006 |
| DEC-002 | 2026-07-27 | accepted | Engineering | Use an explicit Claude settings path, per-profile persistent lease/private baseline state, atomic skillOverrides-only mutation, and applied-digest CAS restoration; never launch a provider session automatically | DEC-012 and DEC-017 require pre-session native control, non-destructive recovery, user-edit preservation, and a fresh session; explicit paths keep mutation bounded | mutate user settings implicitly; generate untracked launch-only settings; explicit bounded settings mutation with recovery (selected) | requirements.md; design.md; tasks.md; context_guard/claude_profile.py; context_guard/cli.py | DSR-201; AC-021–AC-027; TC-021–TC-027 |
| DEC-003 | 2026-07-27 | accepted | Engineering and QA | Implement Slice 3 as a provider-neutral evaluator over versioned sanitized manifests and attempt evidence; define QG-301 through QG-309 as explicit deterministic gates, persist append-only private outcomes, and expose measurement authorization without executing providers or reading token values | DEC-010, DSR-401/402, AC-S401 through AC-S404 require frozen fixtures, machine/instruction oracles, invalid retention, and tokens gated behind quality; exact QG labels lacked an executable schema | execute arbitrary fixture commands; embed provider execution; sanitized evidence evaluator with external execution boundary (selected) | requirements.md; design.md; test-cases.md; tasks.md; context_guard/quality.py; context_guard/cli.py | DSR-401; DSR-402; AC-028–AC-036; TC-028–TC-036 |
| DEC-004 | 2026-07-27 | accepted | Engineering and QA | Implement Slice 4 as an explicit-path, read-only Claude JSONL adapter over assistant message usage; correlate by declared session, deduplicate identical request/message rows, reject inconsistent duplicates or drift, require prior quality authorization, retain signed pair reductions without outlier deletion, and compute exact median plus nearest-rank Q1 gates without launching Claude | DSR-501; DEC-011; AC-S501-1/2; local supported Claude 2.1.218 JSONL key-shape inspection confirmed duplicated identical usage rows keyed by requestId/message.id | automatic HOME scan; inferred time window; explicit correlated files and identifiers (selected) | requirements.md; design.md; test-cases.md; tasks.md; context_guard/claude_measurement.py; context_guard/cli.py | AC-037–AC-045; TC-037–TC-045; T015–T016 |
| DEC-005 | 2026-07-27 | accepted | Engineering and QA | Align Slice 5 with the current official Codex contract: inventory user-authored skills from HOME/.agents/skills, control visibility through exact absolute-path [[skills.config]] entries in an explicit HOME/.codex config profile with lease/snapshot/CAS recovery, and measure cached_input_tokens from explicit exact turn.completed JSONL events or validated monotonic token_count cumulative boundaries | Fresh Codex manual; official build-skills and codex-exec JSONL sections; local config/session key-shape inspection; change-impact CHG-001 on FR-012 | retain stale HOME/.codex/skills root; command-line-only overrides; explicit reversible config profile plus read-only event adapter (selected) | requirements.md; design.md; test-cases.md; tasks.md; context_guard/inventory.py; context_guard/codex_profile.py; context_guard/codex_measurement.py | FR-012; DSR-202; DSR-502; AC-046–AC-063; TC-046–TC-063; T017–T020 |
