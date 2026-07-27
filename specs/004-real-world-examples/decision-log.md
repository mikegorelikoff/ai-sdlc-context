---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-real-world-examples"
  artifact: "decision-log.md"
  path: "specs/004-real-world-examples/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/004-real-world-examples/_ai_sdlc/state.toon"
  decision_log: "specs/004-real-world-examples/decision-log.md"
  status: "draft"
  owner: "TBD"
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
| DEC-001 | 2026-07-27 | accepted | Product owner / Dev | Publish reproducible fixture evidence and opt-in real-local commands, never raw provider logs | User requested real examples; provider logs may contain private prompts and paths | Commit raw samples; fixture-only docs; deterministic fixtures plus explicit local workflow (selected) | requirements.md; design.md; examples/; docs/real-world-examples.md | FR-001..FR-007; AC-001..AC-007; TC-001..TC-008 |
| DEC-002 | 2026-07-27 | accepted | Product owner / Delivery | Release the additive examples package as v0.1.1 with signed Git history, signed tag, wheel, and sdist | User explicitly requested a release after v0.1.0; behavior is backward-compatible and documentation/example focused | No release; v0.2.0 feature release; v0.1.1 patch release (selected) | pyproject.toml; examples/; docs/real-world-examples.md; GitHub Release v0.1.1 | T001; T002; T003; T004; T005; validation receipt |
