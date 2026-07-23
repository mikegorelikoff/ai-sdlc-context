---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-context-guard"
  artifact: "requirements.md"
  path: "specs/001-context-guard/requirements.md"
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
    - "DEC-001"
  related_artifacts:
    - "specs/001-context-guard/decision-log.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "review"
---

# Requirements

## Goal
Provide a local, deterministic hook-based policy engine (Context Guard) that reduces avoidable context growth in Claude Code and Codex agent sessions by blocking or warning on high-cost tool operations (oversized file reads, unbounded command/log output, unscoped repository search) before they enter the model's context, without requiring a proxy, vector database, or centralized data collector.

## Problem Statement
Engineering teams using Claude Code and Codex see high token consumption but cannot identify which developer or agent actions caused it. Common causes include: full reads of large/generated files, unbounded log commands (docker/kubectl logs, git log -p), unscoped repository-wide search (grep -R, find .), repeated large reads within a session, and loading large instruction/skill files for tasks that do not need them. Provider dashboards show totals but not a deterministic, repository-level policy that prevents inefficient actions before they occur. Teams currently rely on developers remembering informal guidance, which is unreliable because model instructions (CLAUDE.md/AGENTS.md) are probabilistic, not enforced.

## Scope
In scope for MVP:
- Local CLI tool (`context-guard`) distributable via pipx/uv, no daemon, no network, no database.
- Provider adapters for Claude Code hooks and Codex hooks that normalize hook JSON on stdin into a common internal event model and return a provider-compatible decision on stdout.
- Deterministic policy engine evaluating file-read, shell-command, and search-command operations against a layered YAML policy (built-in defaults -> user config -> repo config -> env overrides).
- Three enforcement modes: observe, warn, enforce; fail-open by default, with an explicit fail-closed allowlist for a small set of security-adjacent rules.
- Local JSONL audit log of policy decisions (no full prompts, source, output, env values, or secrets by default).
- CLI subcommands: install claude, install codex, validate, test, doctor, report, init.
- Default policy covering: oversized/generated file reads, unbounded log/search shell commands, unscoped repository search.

Out of scope for MVP is covered in "Out of Scope" below.

## Actors
- Developer: runs Claude Code or Codex locally; experiences allow/warn/block decisions and bounded-alternative guidance.
- Claude Code hook runtime: invokes Context Guard as a PreToolUse/PostToolUse/PostToolUseFailure/SessionStart/PreCompact/Stop hook command, passing JSON on stdin and reading a JSON decision on stdout.
- Codex hook runtime: invokes Context Guard as a PreToolUse/PostToolUse/PreCompact/PostCompact/SessionStart/Stop command hook handler.
- Repository/platform maintainer: authors and commits the repo-level `policy.yaml`, chooses the enforcement mode, and reviews the JSONL audit log or `context-guard report` output.
- Context Guard CLI operator: installs, validates, and diagnoses the tool via `context-guard install|validate|test|doctor|report|init`.

## Inputs
- Provider hook JSON payload on stdin: for Claude Code, includes event name (PreToolUse, PostToolUse, PostToolUseFailure, SessionStart, PreCompact, Stop), tool name, tool input (e.g. file path, command string), session id, and cwd. For Codex, includes an analogous payload for PreToolUse, PostToolUse, PreCompact, PostCompact, SessionStart, Stop.
- Layered policy configuration: built-in `defaults/policy.yaml`, optional user-level config (e.g. `~/.config/context-guard/policy.yaml`), optional repo-level config (`.context-guard/policy.yaml` or similar committed path), and environment-variable overrides (e.g. `CONTEXT_GUARD_MODE`).
- Filesystem state needed for evaluation: target file size and path (via `stat`, no file content read), current git repository name/root.
- CLI arguments for `context-guard install|validate|test|doctor|report|init`.

## Outputs
- A provider-compatible JSON decision on stdout: `allow`, `allow-with-warning` (message included), or `block` (with an actionable explanation and, where applicable, one or more bounded-alternative command suggestions).
- One JSONL audit event per evaluated operation appended to a local log file, containing: timestamp, provider, event, operation, matched rule id, decision, estimated_risk, a hash of the command/path (not raw content), and repository name. Raw command text is optionally recorded locally but disabled by default in `enforce`/`warn` modes for organizational deployments.
- CLI outputs: install confirmation and generated hook config diffs (`install`), pass/fail policy + schema validation report (`validate`), fixture-based test run results (`test`), environment/installation diagnostics (`doctor`), a human-readable summary of prevented-context estimates (`report`), and a newly created default policy file (`init`).

## Functional Requirements
- FR-1: The system MUST parse Claude Code hook JSON (PreToolUse, PostToolUse, PostToolUseFailure, SessionStart, PreCompact, Stop) from stdin into a common internal `Event` model.
- FR-2: The system MUST parse Codex hook JSON (PreToolUse, PostToolUse, PreCompact, PostCompact, SessionStart, Stop) from stdin into the same common internal `Event` model.
- FR-3: On a `PreToolUse` file-read event, the system MUST evaluate the target path against deny globs (e.g. `node_modules/**`, `dist/**`, `*.map`, `*.min.js`), file size thresholds (`max_full_read_bytes`, `require_range_above_bytes`), and whether a bounded range was requested, and MUST block full reads that exceed policy without a bounded range.
- FR-4: On a `PreToolUse` shell-command event, the system MUST detect known unbounded patterns (e.g. `docker compose logs`, `kubectl logs`, `git log -p`, `grep -R`, `find .`, `cat <large-lockfile>`) and MUST block commands in the `require_bounds` list that lack a recognized line/time/byte/path boundary flag.
- FR-5: On a `PreToolUse` search-command event, the system MUST require a path scope and/or result limit when `search.require_path_scope` or `search.maximum_results` is configured, and MUST block unscoped repository-root searches that violate this.
- FR-6: A `block` decision MUST include a human-readable explanation and, where a deterministic bounded alternative exists, at least one example corrected command.
- FR-7: The system MUST support three modes per rule group: `observe` (log only, never block), `warn` (allow but attach a warning message), `enforce` (block per policy).
- FR-8: The system MUST resolve policy in this precedence order: built-in defaults -> user config -> repo config -> environment overrides, with later layers overriding earlier ones field-by-field.
- FR-9: The system MUST default cost/token-optimization rules to fail-open (allow) when the tool process errors, cannot parse the event, or cannot load policy, and MUST record the failure in the audit log.
- FR-10: The system MUST support an explicit, separately configured fail-closed rule set (e.g. secrets/protected-path/destructive-command patterns) that blocks on evaluation failure instead of allowing.
- FR-11: The system MUST append one JSONL audit record per evaluated `PreToolUse`/`PostToolUse`/`PostToolUseFailure` event to a local log file, and MUST NOT include full prompts, full file contents, full command stdout, environment-variable values, or secret values in that record by default.
- FR-12: `context-guard install claude` MUST generate or update the Claude Code hook configuration (settings.json hooks block) to invoke Context Guard for the required events without overwriting unrelated existing hook entries.
- FR-13: `context-guard install codex` MUST generate or update Codex's `config.toml`/hook configuration for the required events without overwriting unrelated existing configuration.
- FR-14: `context-guard validate` MUST check policy YAML schema validity and installed hook configuration, returning a non-zero exit code and explicit error list on failure.
- FR-15: `context-guard test` MUST run the fixture-based adapter/policy test suite and report pass/fail per fixture.
- FR-16: `context-guard doctor` MUST report Python version, installation path, policy resolution chain, and detected provider hook configuration status.
- FR-17: `context-guard report` MUST summarize local JSONL audit events into prevented-bytes, prevented-lines, prevented-operation counts, explicitly labeled as an estimate, not a provider-reported token count.
- FR-18: `context-guard init` MUST create a default repo-level `policy.yaml` without overwriting an existing one, and MUST warn (not overwrite) if one is already present.
- FR-19: A `SessionStart` event MUST initialize local per-session state used for detecting repeated large reads within the same session.
- FR-20: A `PreCompact`/`PostCompact` (or nearest available compaction event) MUST record a local checkpoint audit event noting the session's cumulative prevented-context estimate at that point.

## Non-Functional Requirements
- NFR-1 (Latency): Median hook evaluation latency MUST be under 100 ms on a typical developer machine, measured end-to-end from stdin read to stdout write, excluding process startup where a persistent runtime is not used.
- NFR-2 (No network): The tool MUST NOT make outbound network calls during policy evaluation.
- NFR-3 (No external services): The tool MUST run without any database, vector store, or backend service; all state is local files.
- NFR-4 (Portability): The tool MUST run on macOS and Linux developer machines under a supported Python 3 version (3.10+), packaged for pipx/uv installation.
- NFR-5 (Non-destructive install): `context-guard install` MUST be idempotent and MUST NOT remove or corrupt unrelated existing hook/config entries.
- NFR-6 (Auditability): Every blocking or warning decision MUST be reconstructable from the local JSONL audit log (rule id, decision, timestamp) without needing to replay the original session.
- NFR-7 (Fail-safety): A crash or unhandled exception in the policy engine MUST NOT hang the provider's tool-call lifecycle; the process MUST exit deterministically within a bounded timeout and default to the configured fail-open/fail-closed behavior for the affected rule group.
- NFR-8 (Testability): Provider adapters MUST be tested against captured JSON fixtures rather than live provider processes.
- NFR-9 (Privacy default): Default configuration MUST NOT persist secret values, full command output, or full file contents to disk.

## Constraints
- MVP MUST NOT use an LLM or semantic analysis for policy evaluation; all rules are deterministic (size/glob/pattern/flag checks).
- MVP MUST NOT introduce a proxy, API gateway, or centralized data collector.
- MVP MUST NOT auto-rewrite commands; on block, it only suggests bounded alternatives for the agent/developer to issue.
- MVP MUST NOT auto-terminate sessions; it may only warn that compaction/restart is advisable.
- Claude Code and Codex hook schemas are provider-controlled and may change; provider parsing MUST be isolated to `adapters/claude_code.py` and `adapters/codex.py` so schema changes do not require engine changes.
- Codex's current hook implementation supports command hook handlers only (prompt/agent hook handlers may be parsed but are not executed), so the Codex adapter targets command-handler invocation only.
- The MVP is explicitly not a security product; security-adjacent rules (secrets, protected paths, destructive commands) are best-effort convenience blocks and MUST NOT be marketed or relied upon as replacing OS permissions, sandboxing, secret scanning, or endpoint protection.

## Acceptance Criteria
- AC-001: Given a Claude Code `PreToolUse` Read event for a file matching a deny glob (e.g. `dist/bundle.min.js`) without a bounded range, when Context Guard evaluates it in `enforce` mode, then it returns a `block` decision with an explanation and a bounded-range suggestion, and appends one JSONL audit record with `decision: block`.
- AC-002: Given the same event in `observe` mode, when Context Guard evaluates it, then it returns `allow` and appends a JSONL audit record with `decision: block` and an `observe_mode: true`-equivalent marker showing what would have happened, without blocking execution.
- AC-003: Given a shell command `docker compose logs api` (no bound flags), when evaluated in `enforce` mode, then it is blocked with suggested alternatives including `--tail` and `--since` forms; given `docker compose logs --tail 200 api`, then it is allowed.
- AC-004: Given `rg "PaymentService" src/payment` (scoped search with a path), when evaluated, then it is allowed without a warning.
- AC-005: Given `find . -type f` (unscoped, repo root, no result limit) with `search.require_path_scope: true`, when evaluated in `enforce` mode, then it is blocked with an explanation.
- AC-006: Given a policy evaluation that throws an unhandled exception for a token-optimization rule, when Context Guard runs, then it returns `allow` (fail-open) and logs the error to the audit log, and the host provider's tool call proceeds.
- AC-007: Given `context-guard install claude` run twice in a row, when inspecting the resulting Claude Code hook configuration, then it is unchanged after the second run (idempotent) and any pre-existing unrelated hooks remain intact.
- AC-008: Given `context-guard validate` run against a syntactically invalid `policy.yaml`, when executed, then it exits non-zero and prints the specific schema error(s).
- AC-009: Given at least 5 captured fixture events covering the 5 required high-cost patterns (oversized file read, unbounded docker/kubectl logs, `git log -p`, unscoped `find`/`grep -R`, oversized lockfile read), when `context-guard test` runs, then all fixtures pass with the expected decision.
- AC-010: Given 100 sequential fixture evaluations on a representative developer machine, when timed, then the median wall-clock evaluation latency is under 100 ms.

## Out of Scope
- Vector search, embeddings, or semantic relevance scoring of any kind.
- A web dashboard or centralized reporting/control-plane service.
- Centralized employee monitoring or cross-developer data collection.
- Direct provider billing/usage API integration (exact token-cost attribution).
- Automatic command rewriting or automatic session termination.
- Source-code summarization or model routing.
- An API gateway or proxy in front of Claude Code/Codex.
- Exact tokenizer-accurate token counting for every provider.
- Autonomous modification of repository policy files by the tool itself.
- A persistent daemon/long-running background process (may be considered post-MVP for performance).

## Assumptions
- Assumption: Claude Code hook configuration is expressed as commands in `settings.json` under a `hooks` key, matching the currently documented Claude Code hooks feature; the install command should be updated if this schema changes.
- Assumption: Codex hook configuration lives in `config.toml` or a related hook configuration file and currently executes command hook handlers; prompt/agent hook handlers are treated as parsed-but-not-executed per the PRFAQ and are out of scope for the MVP adapter.
- Assumption: "Bounded" for shell commands means the presence of a recognized flag or argument (e.g. `--tail`, `--since`, a path argument narrower than repo root, a `-n`/`-m` result-limit flag); the MVP uses a maintained pattern list per command family rather than full shell-argument semantic parsing.
- Assumption: File size and generated-file detection rely on filesystem `stat` and path/extension/glob matching only; the tool does not open or read file contents to make the block/allow decision (this also keeps evaluation fast per NFR-1).
- Assumption: The initial pilot audience is individual developers and small teams opting in voluntarily; organization-wide enforced rollout and bypass prevention are explicitly deferred (see PRFAQ risk: "Developers bypass the tool").

## Open Questions
- TODO(dm): Which exact Claude Code settings.json hook schema version should `install claude` target, and should it detect/support both project-level and user-level settings files?
- TODO(dm): What is the canonical current Codex hook configuration file location/schema (config.toml key names) to target for `install codex`, given the PRFAQ notes command-handler-only support?
- TODO(dm): Should the repo-level policy file live at `.context-guard/policy.yaml`, `context-guard.yaml` at repo root, or another path — needs a decision before `init`/config-resolution code is finalized.
- TODO(dm): What is the acceptable default JSONL audit log location and rotation/retention policy (e.g. `.context-guard/audit.jsonl`, size-based rotation)?
- TODO(dm): Is a 100 ms median latency budget measured with or without Python interpreter cold-start; does this require a `--fast` compiled path or persistent worker in a later phase?

## Decision Status
- Decision: Proceed with MVP scope, architecture, and constraints as specified in the PRFAQ, using documented assumptions above for provider hook schema details pending confirmation (see Open Questions). Recorded as DEC-001 in `decision-log.md`.
- Status: Draft requirements ready for design; no blocking unresolved decision prevents starting `design.md`, since assumed defaults are reasonable and reversible (config paths and hook schema targets are adapter-local and can change without affecting the core engine contract).

