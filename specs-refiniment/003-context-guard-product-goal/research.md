---
artifact_metadata:
  schema: "ai-sdlc-research-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "research.md"
  path: "/Users/mikegorelikov/ai-sdlc-context/specs-refiniment/003-context-guard-product-goal/research.md"
  workspace: "refinement"
  skill: "ai-sdlc-research"
  flow_mode: "full"
  state_file: "/Users/mikegorelikov/ai-sdlc-context/specs-refiniment/003-context-guard-product-goal/_ai_sdlc/state.toon"
  status: "review"
  updated_at: "2026-07-27"
  trace_ids:
    - "BR-108"
    - "BR-206"
    - "BR-208"
    - "DEC-003"
    - "DEC-004"
    - "DEC-008"
    - "DEC-009"
    - "DEC-010"
    - "DEC-011"
    - "DEP-001"
    - "GAP-001"
    - "GAP-002"
    - "GAP-004"
    - "RISK-001"
    - "RISK-005"
  metatags:
    - "ai-sdlc"
    - "research"
    - "evidence"
    - "traceable"
---

# Research

## Topic

Provider-supported pre-inference skill visibility controls for Claude Code and Codex

## Questions

- id: RQ-001; question: Does Claude Code expose a supported control point that can prevent irrelevant skill content before it enters model context?; trace_targets: GAP-001/DEP-001/RISK-001
- id: RQ-002; question: Does Codex expose a supported control point that can prevent irrelevant skill content before it enters model context?; trace_targets: GAP-001/DEP-001/RISK-001
- id: RQ-003; question: What can Context Guard control without modifying authoritative skill bodies or introducing its own compact skill index?; trace_targets: GAP-001/GAP-002/DEC-004
- id: RQ-004; question: Which installed client versions and diagnostic surfaces can verify visibility before a paid model inference?; trace_targets: GAP-001/GAP-004/RISK-001
- id: RQ-005; question: Which Claude Code surfaces can apply per-skill visibility before session-start context is built while preserving explicit invocation?; trace_targets: GAP-001/DEC-009/BR-206/BR-208
- id: RQ-006; question: Which Codex configuration layers and client surfaces actually affect the model-visible skill list before thread start?; trace_targets: GAP-001/DEC-009/BR-206/BR-208

## Sources

- id: SRC-001; title: Extend Claude with skills; locator: https://code.claude.com/docs/en/slash-commands; type: official-documentation; accessed_at: 2026-07-27; credibility: Primary Claude Code product documentation.; notes: Documents progressive loading;  invocation controls;  listing behavior;  and the full-skill lifecycle.
- id: SRC-002; title: Claude Code hooks reference; locator: https://code.claude.com/docs/en/hooks; type: official-documentation; accessed_at: 2026-07-27; credibility: Primary Claude Code hook contract.; notes: Documents Skill PreToolUse;  UserPromptExpansion;  InstructionsLoaded;  and their timing.
- id: SRC-003; title: Codex skill-creator reference implementation; locator: https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md; type: official-source-code; accessed_at: 2026-07-27; credibility: OpenAI-owned Codex repository and bundled skill guidance.; notes: Defines intended Codex progressive disclosure for metadata;  skill bodies;  and resources.
- id: SRC-004; title: Codex app-server protocol documentation; locator: https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md; type: official-source-code; accessed_at: 2026-07-27; credibility: OpenAI-owned current app-server protocol documentation.; notes: Documents skills/list;  skills/config/write user-level configuration;  explicit skill injection;  thread startup;  and usage events.
- id: SRC-005; title: Current Context Guard provider adapters; locator: context_guard/adapters/claude_code.py and context_guard/adapters/codex.py; type: internal-source-code; accessed_at: 2026-07-27; credibility: Direct inspection of the repository implementation under refinement.; notes: Read with events.py;  engine.py;  and cli.py to establish the existing lifecycle/tool boundary.
- id: SRC-006; title: Context Guard product-goal discovery evidence; locator: specs-refiniment/003-context-guard-product-goal/discovery.md; type: internal-evidence; accessed_at: 2026-07-27; credibility: Sanitized observations from local Claude Code and Codex session logs.; notes: Shows pre-work cache-token activity but does not attribute it solely to skill content.
- id: SRC-007; title: Anthropic prompt caching; locator: https://platform.claude.com/docs/en/build-with-claude/prompt-caching; type: official-documentation; accessed_at: 2026-07-27; credibility: Primary Anthropic API usage-field contract.; notes: Defines cache creation;  cache read;  and uncached input token semantics.
- id: SRC-008; title: Claude Code settings; locator: https://code.claude.com/docs/en/settings; type: official-documentation; accessed_at: 2026-07-27; credibility: Primary Claude Code settings contract.; notes: Documents skillOverrides values;  settings-local persistence;  plugin limitation;  and the v2.1.129 minimum.
- id: SRC-009; title: Codex project-local skill filtering limitation; locator: https://github.com/openai/codex/issues/20210; type: vendor-issue; accessed_at: 2026-07-27; credibility: OpenAI repository issue with a reproducible current configuration-layer limitation; corroborated locally.; notes: Reports that project-local skills.config entries do not affect the model-visible list while user/global configuration does.
- id: SRC-010; title: Version-pinned local client diagnostics; locator: Local commands: claude --version/--help; codex --version/--help; codex debug prompt-input; type: local-diagnostic; accessed_at: 2026-07-27; credibility: Direct execution against the installed clients without a model inference.; notes: Claude Code 2.1.218 exposes settings;  setting-source;  full-skill-disable;  print;  and IDE flags. Codex CLI 0.144.1 exposes command-line configuration;  app-server;  and model-visible prompt rendering.
- id: SRC-011; title: Disposable Codex skill-visibility capability fixture; locator: Ephemeral nested repository executed locally and removed after sanitized counts were captured; type: local-test-evidence; accessed_at: 2026-07-27; credibility: Controlled no-inference A/B test against Codex CLI 0.144.1.; notes: Baseline listed the probe skill once; project-local skills.config still listed it once; explicit command-line skills.config listed it zero times. Separate tests showed selected global entries and skills.include_instructions affect prompt construction.
- id: SRC-012; title: Sanitized local provider usage samples; locator: Local Claude project JSONL and Codex rollout JSONL under the user home directory; type: internal-observation; accessed_at: 2026-07-27; credibility: Direct schema and counter inspection without retaining prompts;  source content;  credentials;  or raw responses.; notes: Supports the provider-specific measurement adapter contract in DEC-011.

## Findings

- id: RF-001; statement: In a regular Claude Code session;  skill descriptions are placed in context while full bodies load only when invoked; irrelevant full skill bodies are not normally a startup-context cost.; source_ids: SRC-001; confidence: high; limitations: Preloaded subagent skills are an exception and behavior is version-dependent.; trace_targets: GAP-001/DEP-001
- id: RF-002; statement: Claude Code has supported controls that reduce skill-listing context without rewriting a skill body: disable-model-invocation in owned frontmatter and skillOverrides in settings.; source_ids: SRC-001/SRC-008; confidence: high; limitations: skillOverrides does not apply to plugin skills; frontmatter changes are not an acceptable generated intervention for authoritative third-party skills.; trace_targets: GAP-001/GAP-002
- id: RF-003; statement: Claude hooks that observe or block a Skill call run after the model-visible skill listing is assembled and therefore are not a generic initial-context rewrite boundary.; source_ids: SRC-001/SRC-002; confidence: high; limitations: This is an inference from documented hook timing and scope.; trace_targets: GAP-001/DEP-001/RISK-001
- id: RF-004; statement: Codex uses progressive disclosure: name and description metadata are the routing surface and full SKILL.md content loads after explicit selection or trigger.; source_ids: SRC-003/SRC-004; confidence: high; limitations: End-to-end token traces remain necessary to quantify contribution.; trace_targets: GAP-001/DEP-001
- id: RF-005; statement: Codex app-server supports skills/list plus user-level enable or disable by absolute path or name;  and explicit skill input injects the authoritative full instructions.; source_ids: SRC-004; confidence: high; limitations: The configuration write mutates user-level state and must be paired with rollback; app-server behavior may not map to every client version.; trace_targets: GAP-001/GAP-002/BR-208
- id: RF-006; statement: The current Context Guard implementation is not skill-aware and cannot presently manage provider skill visibility or profile skill loading.; source_ids: SRC-005; confidence: high; limitations: Reflects the current working tree only.; trace_targets: GAP-001/GAP-002/DEC-008
- id: RF-007; statement: Observed pre-work cache-token activity proves a measurement problem but not that full skill bodies caused it; both providers normally expose metadata before invocation rather than every body.; source_ids: SRC-001/SRC-003/SRC-006; confidence: high; limitations: Controlled contribution isolation has not yet run.; trace_targets: GAP-001/GAP-004/RISK-001
- id: RF-008; statement: GAP-001 is feasible only through provider-specific startup configuration;  not a generic runtime hook.; source_ids: SRC-001/SRC-002/SRC-003/SRC-004/SRC-005; confidence: high; limitations: Supported client surfaces and configuration-layer constraints must remain explicit.; trace_targets: GAP-001/GAP-002/DEC-008
- id: RF-009; statement: Claude cache usage for DEC-003 is the sum of cache creation and cache read tokens across unique responses in the declared window;  with local transcript deduplication by request and message identity.; source_ids: SRC-007/SRC-012; confidence: high; limitations: Claude Code transcript schema must be version-preflighted.; trace_targets: GAP-004/DEC-003/DEC-011
- id: RF-010; statement: Codex measurement should prefer exact per-completion cached input; a validated local rollout fallback uses cumulative total deltas and never sums re-emitted last-token snapshots.; source_ids: SRC-004/SRC-012; confidence: medium; limitations: Exact raw completion events are experimental and rollout schemas may drift.; trace_targets: GAP-004/DEC-003/DEC-011
- id: RF-011; statement: The provider pilot requires paired fresh sessions;  standardized cache priming;  alternating order;  hard quality gates before measurement;  and no statistical outlier deletion.; source_ids: SRC-007/SRC-004/SRC-012; confidence: medium; limitations: Pilot defaults require dry-run validation.; trace_targets: GAP-004/DEC-010/DEC-011
- id: RF-012; statement: The installed clients are Claude Code 2.1.218 and Codex CLI 0.144.1; both are new enough to expose the documented or diagnostic configuration surfaces used by this capability matrix.; source_ids: SRC-008/SRC-010; confidence: high; limitations: The matrix must be rerun whenever either client version changes.; trace_targets: GAP-001/GAP-004/RISK-005
- id: RF-013; statement: Claude Code 2.1.218 can apply per-skill visibility from settings before its session skill listing is built. user-invocable-only is the conservative irrelevant-skill action because it removes model visibility while preserving explicit user invocation; name-only is a lower-savings fallback and on preserves normal behavior.; source_ids: SRC-001/SRC-008/SRC-010; confidence: high; limitations: No no-inference prompt renderer exists in the inspected CLI;  so the exact local listing delta still requires the first controlled Claude pilot; plugin skills are excluded.; trace_targets: GAP-001/DEC-009/BR-206/BR-208
- id: RF-014; statement: Claude CLI interactive;  print;  and IDE-connected sessions share startup settings surfaces;  but generated profiles must be passed before session creation; hooks or mid-session settings changes cannot earn startup savings for the active session.; source_ids: SRC-001/SRC-002/SRC-008/SRC-010; confidence: medium; limitations: IDE parity is inferred from the shared Claude Code process and --ide surface rather than a separate IDE-specific skill visibility contract.; trace_targets: GAP-001/BR-208/RISK-001
- id: RF-015; statement: Codex CLI 0.144.1 applies explicit startup skills.config overrides before model prompt construction. In no-inference diagnostics;  disabling each absolute-path duplicate removed one inventory entry and disabling both removed both; a global include-instructions switch removed the complete skills section.; source_ids: SRC-010/SRC-011; confidence: high; limitations: The global switch is too coarse for DEC-009 and is not the recommended MVP action.; trace_targets: GAP-001/DEC-009/BR-208
- id: RF-016; statement: Codex CLI 0.144.1 did not honor a repository-local .codex/config.toml skills.config entry for the disposable probe skill;  while the equivalent command-line startup override removed it from the model-visible prompt.; source_ids: SRC-009/SRC-011; confidence: high; limitations: This result is version-pinned and may change; repository-local filtering must remain capability-tested rather than assumed.; trace_targets: GAP-001/RISK-001/RISK-005
- id: RF-017; statement: Codex app-server and app-server-backed clients have a supported user-level configuration path through skills/config/write and can verify state with skills/list; changes must happen before thread/start and be rolled back after the run.; source_ids: SRC-004; confidence: high; limitations: The local app-server mutation flow was not executed because it would alter user-level configuration; IDE and desktop client versions still require preflight.; trace_targets: GAP-001/BR-108/BR-208
- id: RF-018; statement: GAP-001 is definition-complete for a bounded MVP: support Claude non-plugin skills through startup skillOverrides and Codex CLI/app-server sessions through generated startup or user-level profiles; require a new session;  actual-state verification;  rollback;  and full-load fallback. Repository-local Codex filtering;  Claude plugin skills;  unsupported IDE versions;  and mid-session interception are not supported optimization surfaces.; source_ids: SRC-001/SRC-004/SRC-008/SRC-009/SRC-010/SRC-011; confidence: high; limitations: Execution qualification still requires a controlled Claude listing/token run and Codex app-server/IDE preflight; unsupported surfaces remain measurement-only/full-load.; trace_targets: GAP-001/DEC-009/DEC-011/RISK-001

## Open Questions

- id: OQ-001; question: Do the installed Codex IDE and desktop clients use the same pre-thread user-level skill state as Codex app-server 0.144.1?; owner: Engineering; next_action: Run skills/list before thread/start in each installed client surface and compare the enabled inventory digest without sending a model turn.
- id: OQ-002; question: How many provider-reported cache tokens are attributable to skill metadata versus other startup instructions?; owner: Product and Engineering; next_action: Execute the DEC-011 controlled baseline and guarded pilots after the adapters and runner exist.
- id: OQ-003; question: Should Claude plugin skills and Codex repository-local configuration become a later compatibility slice?; owner: Product; next_action: Keep them out of the bounded MVP unless pilot demand justifies a provider-specific follow-up capability.
