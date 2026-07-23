---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-context-guard"
  artifact: "design.md"
  path: "specs/001-context-guard/design.md"
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
  related_artifacts:
    - "specs/001-context-guard/decision-log.md"
    - "specs/001-context-guard/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "review"
---

# Design

## Overview
Context Guard is a local, stateless-per-invocation CLI process invoked synchronously by Claude Code and Codex lifecycle hooks. Each hook call pipes a provider JSON payload to `context-guard hook <provider> <event>` on stdin; the process normalizes the payload, evaluates it against layered YAML policy with a pure-Python deterministic engine (no LLM calls, no network), writes a provider-compatible JSON decision to stdout, appends a compact JSONL audit record locally, and exits. There is no daemon, no persistent process, and no database; cross-call session state (e.g. repeated-read detection) is kept in a small local per-session JSON state file keyed by session id, written under a local `.context-guard/` directory.

## Architecture
```text
Claude Code / Codex lifecycle hook
        │  (JSON on stdin)
        ▼
cli.py  --  entrypoint: parses argv (provider, event), reads stdin
        │
        ▼
adapters/{claude_code.py,codex.py}  --  parse provider JSON -> events.Event
        │
        ▼
engine.py  --  loads layered policy (policies/config.py-equivalent inline),
               dispatches Event to the matching policy module by operation kind
        │
        ├─ policies/files.py     (file-read operations)
        ├─ policies/commands.py  (shell-command operations)
        ├─ policies/searches.py  (search-command operations)
        └─ policies/sessions.py  (SessionStart/PreCompact/PostCompact/Stop bookkeeping)
        │
        ▼
decisions.py  --  builds a normalized Decision (allow/warn/block + message + suggestions)
        │
        ├──▶ adapters/{claude_code,codex}.py  --  render Decision back to provider-specific JSON on stdout
        └──▶ audit/jsonl.py  --  append one compact JSONL record to the local audit log
```
Data flow is strictly one-shot per process invocation: stdin -> normalize -> evaluate -> stdout + audit append -> exit. The engine core (`engine.py`, `decisions.py`, `policies/*`) has no knowledge of provider JSON shapes; only the two adapter modules parse/render provider-specific formats, so a provider schema change is isolated to one file.

## Components
- `context_guard/cli.py`: argparse-based entrypoint exposing `hook`, `install`, `validate`, `test`, `doctor`, `report`, `init` subcommands; reads stdin for `hook`, prints JSON to stdout, sets process exit code.
- `context_guard/events.py`: defines the internal `Event` dataclass (provider, event_name, operation_kind, path, command, session_id, cwd, raw metadata) and `operation_kind` classification (`file_read`, `shell_command`, `search_command`, `session_lifecycle`, `other`).
- `context_guard/engine.py`: loads and merges policy layers (`Policy` object), routes an `Event` to the right policy module, returns a `Decision`.
- `context_guard/decisions.py`: defines `Decision` (status: allow/warn/block, message, suggestions: list[str], rule_id, estimated_risk) and helpers to build common decisions.
- `context_guard/adapters/claude_code.py`: `parse(payload: dict) -> Event` and `render(decision: Decision) -> dict` for Claude Code's hook JSON shape; isolates all Claude-Code-specific field names.
- `context_guard/adapters/codex.py`: same contract as above for Codex's hook JSON shape.
- `context_guard/policies/files.py`: evaluates file-read events against deny globs, size thresholds, and bounded-range detection.
- `context_guard/policies/commands.py`: evaluates shell-command events against the `require_bounds` command family list and known unbounded-pattern detectors.
- `context_guard/policies/searches.py`: evaluates search-command events (ripgrep/grep/find family) against path-scope and result-limit requirements.
- `context_guard/policies/sessions.py`: tracks per-session repeated-read counters and cumulative prevented-context estimate, persisted to a small local JSON state file per session id; handles `SessionStart`, `PreCompact`/`PostCompact`, `Stop`.
- `context_guard/audit/jsonl.py`: appends one compact JSON line per evaluated event to the local audit log, and a `summarize()` function used by `report`.
- `context_guard/policy_config.py`: loads/merges built-in `defaults/policy.yaml`, user config, repo config, and environment overrides into a validated `Policy` object; used by `engine.py`, `validate`, `init`, and `doctor`.
- `integrations/claude-code/`: template hook-config fragment(s) and install helper used by `cli.py install claude`.
- `integrations/codex/`: template hook-config fragment(s) and install helper used by `cli.py install codex`.
- `defaults/policy.yaml`: the built-in default policy shipped with the package.

## Interfaces and Contracts
- CLI contract: `context-guard hook <claude|codex> <event-name>` reads one JSON object from stdin and writes exactly one JSON object to stdout; non-zero process exit is reserved for genuine CLI usage errors (missing args), never for a `block` decision — `block` is communicated via the JSON payload per each provider's documented hook-response contract, not via process exit code, so the host provider always receives a structured response.
- Internal `Event` contract (`events.py`): `{provider: str, event_name: str, operation_kind: str, path: str|None, command: str|None, session_id: str, cwd: str, raw: dict}`. Adapters MUST populate `operation_kind` using a shared classification table so policy modules never inspect provider-specific fields directly.
- Internal `Decision` contract (`decisions.py`): `{status: "allow"|"warn"|"block", message: str|None, suggestions: list[str], rule_id: str|None, estimated_risk: "low"|"medium"|"high"}`. Adapters translate this into the provider's expected hook-response JSON shape (e.g. Claude Code's `PreToolUse` decision fields) and MUST NOT invent fields not in this contract.
- Policy module contract: every `policies/*.py` module exposes `evaluate(event: Event, policy: Policy) -> Decision | None`, returning `None` when the module does not apply to this event's `operation_kind`; `engine.py` calls modules in a fixed order and takes the first non-`None` result.
- Policy config contract (`policy_config.py`): `load(repo_root: Path) -> Policy`, merging YAML layers field-by-field (later layer wins per key, lists are replaced not appended unless a key is explicitly named `*_extra`).
- Audit record contract (`audit/jsonl.py`): one JSON object per line matching the "What data will be recorded" schema from the PRFAQ (timestamp, provider, event, operation, rule, decision, estimated_risk, command_hash, repository); no other module writes to the audit log directly.

## Data Model
- `Policy` (in-memory, merged from YAML layers): `mode: observe|warn|enforce` (global default, overridable per rule group); `files: {max_full_read_bytes, require_range_above_bytes, deny: [glob,...]}`; `commands: {maximum_expected_output_lines, require_bounds: [command-family,...]}`; `search: {require_path_scope: bool, maximum_results: int}`; `fail_closed_rules: [rule_id,...]`.
- `Event` (in-memory, per-invocation): see Interfaces and Contracts.
- `Decision` (in-memory, per-invocation): see Interfaces and Contracts.
- Audit record (on-disk JSONL, append-only, one file per repository e.g. `.context-guard/audit.jsonl`): `{timestamp, provider, event, operation, rule, decision, estimated_risk, command_hash, repository}`; raw command/path text is omitted by default and only included when an explicit local-debug config flag is set.
- Session state (on-disk JSON, one file per active session id, e.g. `.context-guard/sessions/<session_id>.json`): `{session_id, started_at, reads_by_path: {path: count}, prevented_bytes_estimate: int, prevented_lines_estimate: int, last_compaction_at: str|None}`; created on `SessionStart`, updated on each evaluated event, removed or archived on `Stop`.

## Error Handling
- stdin parse failure (invalid JSON) or unrecognized provider/event: return `allow` for token-optimization rule groups (fail-open per FR-9), log the parse error with a distinct `rule: "internal-error"` audit record, exit 0.
- Policy load/merge failure (e.g. invalid YAML): same fail-open behavior for cost rules; for any rule id present in `fail_closed_rules`, the corresponding operation is blocked with a generic "policy could not be verified" message instead (FR-10).
- Any unhandled exception inside a policy module: caught at the `engine.py` dispatch boundary, converted to the same fail-open/fail-closed-by-rule-group behavior, and never allowed to propagate to a non-zero exit or hang (NFR-7).
- Filesystem errors reading `stat` for a target path (e.g. race where file no longer exists): treated as "cannot verify size" and falls through to fail-open for that specific check only, not the whole event.
- Audit log write failure (e.g. disk full, permissions): swallowed with a best-effort `stderr` warning; never blocks or delays returning the decision to the provider.

## Security Considerations
- Context Guard is explicitly not a security product (per requirements Constraints); any secrets/protected-path/destructive-command rules are best-effort convenience blocks and must be documented as such, not as a substitute for OS permissions, sandboxing, secret scanning, or endpoint protection.
- The tool must never read or persist full file contents, full command stdout, environment-variable values, or secret values by default; only path/command hashes and size metadata are recorded.
- `command_hash` in audit records uses a one-way hash (e.g. sha256) of the raw command string so audit logs cannot leak command arguments while still enabling duplicate-detection and reporting.
- Local audit and session-state files are written with restrictive file permissions (user-only read/write) since they may indirectly reveal repository names and operation patterns.
- Because the tool executes as a hook command with the same privileges as the developer's shell, it must not execute, `eval`, or shell out to any part of the inspected command/path — all evaluation is pure string/glob/stat inspection, never execution of the candidate command.
- Install commands (`install claude`, `install codex`) only ever add/update a scoped hook entry; they must not disable or remove other unrelated hooks or security controls already configured by the user.

## Observability
- Every evaluated `PreToolUse`/`PostToolUse`/`PostToolUseFailure` event produces exactly one JSONL audit record, giving a complete local trail of allow/warn/block decisions per repository (NFR-6).
- `context-guard report` reads the JSONL audit log and aggregates: count of blocked/warned/allowed operations by rule id, estimated prevented bytes/lines, and compaction-checkpoint history, clearly labeled as an internal estimate rather than a provider-reported token metric (FR-17).
- `context-guard doctor` surfaces the resolved policy layer chain (which file each effective setting came from) and detected hook installation status, so a user can debug why a rule did or did not fire.
- Internal errors (parse failures, policy load failures, unhandled exceptions) are always logged to the audit log with `rule: "internal-error"` so silent fail-open behavior is still visible and countable.

## Risks and Tradeoffs
- Provider hook schemas may change (Claude Code and Codex are both actively evolving): mitigated by isolating all provider-specific parsing/rendering to the two adapter modules and covering them with fixture-based contract tests (NFR-8), per PRFAQ risk #1.
- Overly aggressive default policy could block legitimate work and erode trust: mitigated by defaulting new installs to `observe` mode and requiring an explicit opt-in to `enforce`, matching the PRFAQ's recommended weekly rollout (observe -> warn -> enforce).
- Per-process CLI startup latency (Python interpreter cold start) could threaten the <100 ms median latency NFR on slower machines: tracked as an open question (see requirements Open Questions); mitigated short-term by keeping the engine dependency-light (stdlib + PyYAML only) and deferring a persistent-daemon architecture to a later phase if measurements show it is needed.
- A small number of security-adjacent fail-closed rules could be mistaken for real security enforcement: mitigated by explicit product-boundary language in `doctor`/`report` output and documentation (per requirements Constraints and PRFAQ FAQ #10).
- Session-state files could grow unbounded across many sessions: mitigated by removing/archiving the per-session state file on `Stop`.

## Validation Strategy
- Unit tests per policy module (`policies/files.py`, `commands.py`, `searches.py`, `sessions.py`) covering allow/warn/block boundaries with table-driven cases.
- Adapter contract tests using captured JSON fixtures for both Claude Code and Codex hook payloads (covering all required events per FR-1/FR-2), asserting correct `Event` normalization and correct provider-shaped `Decision` rendering.
- End-to-end CLI tests invoking `context-guard hook <provider> <event>` as a subprocess with fixture stdin and asserting stdout JSON and audit-log side effects, matching AC-001 through AC-009.
- A latency benchmark test (`context-guard test --bench` or equivalent) running representative fixtures N times and asserting median latency under 100 ms, matching AC-010.
- `context-guard validate` is itself exercised in tests against both a valid and an intentionally invalid `policy.yaml` to confirm non-zero exit and explicit error messages (AC-008).
- Install idempotency test: run `install claude`/`install codex` twice against a temp directory containing a pre-existing unrelated hook entry, and assert the file is stable after the second run and the unrelated entry survives (AC-007).
- Use `$ai-sdlc-validation` for repository-wide command selection when running these suites during implementation and commit prep.

## Migration Notes
This is a greenfield MVP in a currently empty repository; there is no prior Context Guard version, existing hook configuration, or existing policy file to migrate from. `context-guard init`/`install` are additive-only against any pre-existing, unrelated Claude Code/Codex configuration the user may already have (see NFR-5). No data migration is required.

