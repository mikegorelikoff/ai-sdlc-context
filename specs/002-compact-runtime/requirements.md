---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "002-compact-runtime"
  artifact: "requirements.md"
  path: "specs/002-compact-runtime/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/002-compact-runtime/_ai_sdlc/state.toon"
  decision_log: "specs/002-compact-runtime/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-07-24"
  updated_at: "2026-07-24"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "DEC-001"
  related_artifacts:
    - "specs/002-compact-runtime/decision-log.md"
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
Deliver Compact Runtime Increment 2.1: a local, deterministic execution and context-compaction layer that runs a supported command (starting with test runners via `context-guard test`), preserves the complete raw output as a local artifact, parses it deterministically, and returns Claude Code/Codex a bounded structured summary with drill-down references instead of raw output — reducing model-facing context without discarding evidence.

## Problem Statement
Context Guard Stage 1 (specs/001-context-guard) blocks predictably expensive operations, but a blocked agent still needs diagnostic evidence and may retry with arbitrary line limits, miss the root cause, or over-request context. Test runners, log commands, repository search, and diffs can each produce thousands of lines when the agent needs only a small identifiable part (e.g. one failing test out of 20,000 passing lines). Once large raw output enters a session it can remain part of subsequent model calls, increasing context pressure and potentially increasing input/cache-related token consumption. There is no local, deterministic mechanism that executes the operation once, preserves the full result, and returns only the smallest sufficient representation with a path to inspect more evidence on demand.

## Scope
This spec covers PRFAQ Rollout Increment 2.1 ("Test output") only: one complete vertical slice of command execution -> raw artifact -> deterministic test parser -> compact result -> failure fragment drill-down -> ledger record, plus the shared foundation later increments will reuse.

In scope:
- `context-guard test -- <command>` CLI subcommand that executes a test command, captures stdout/stderr/exit status/duration, and stores the complete raw output as a local artifact.
- A local filesystem artifact store under `.context-guard/artifacts/test/` with a stable artifact id/reference scheme (e.g. `artifact:test-018`).
- A deterministic pytest output parser (native `pytest --junitxml` machine-readable output preferred; fall back to deterministic text parsing) producing a bounded compact JSON result: status, collected/passed/failed totals, failure list (name, file, line, diagnostic, evidence reference), and an artifact reference.
- A safe-fallback path when the parser does not recognize the output format: exit status, a bounded preview, and the full artifact reference, with no invented root cause.
- `context-guard artifact show <id> --fragment <fragment>` for drill-down retrieval of exact fragments (e.g. a specific failure's full traceback) from the stored artifact.
- A minimal Context Ledger (SQLite, `.context-guard/ledger.sqlite`) recording each compact-tool invocation (command, input state/repository commit, artifact id, result summary) so a later increment can build deduplication on top of it; this increment only records entries, it does not yet suppress repeated unchanged reads.
- A reproducible local benchmark harness for scenario CTX-01 (Noisy test suite) per the PRFAQ's Test Matrix and Required Execution Controls, producing the metrics listed in the PRFAQ (baseline/compact bytes and lines, compression ratio, required evidence found, full artifact available).

Out of scope for this spec is listed under "Out of Scope" below and is deferred to future increments per the PRFAQ Rollout Plan.

## Actors
- Developer/agent: runs `context-guard test -- <command>` instead of the raw test command directly (or is redirected there by a future Stage-1 hook recommendation), receives the compact JSON result, and optionally drills down via `context-guard artifact show`.
- Claude Code / Codex hook runtime: may invoke compact tools directly or receive a Stage-1 hook recommendation to use them (integration wiring is scoped narrowly here; see Constraints).
- Repository/platform maintainer: reviews `.context-guard/artifacts/` retention and the ledger for security/size considerations.
- Benchmark operator: runs the reproducible CTX-01 benchmark scenario against a named Context Guard version/commit and publishes results into this spec's qa.md evidence section.

## Inputs
- CLI invocation: `context-guard test -- <test command and arguments>` (e.g. `context-guard test -- pytest`).
- The underlying test command's stdout, stderr, exit status, wall-clock duration, and current repository state (commit hash if available).
- Optional native machine-readable output from the test tool when available (e.g. `pytest --junitxml=<path>`), preferred over text parsing.
- `context-guard artifact show <artifact-id> [--fragment <fragment-id>]` CLI arguments for drill-down.
- Existing Context Guard policy/config (`.context-guard/policy.yaml`) is not required by Compact Runtime itself but the artifact store shares the repo's `.context-guard/` directory.

## Outputs
- A compact JSON result on stdout matching the PRFAQ's worked example shape: `{"status", "tests": {"collected","passed","failed"}, "failures": [{"name","file","line","diagnostic","evidence"}], "artifact": "artifact:<id>"}`.
- A complete raw artifact on the local filesystem at `.context-guard/artifacts/test/<id>/` containing the full stdout/stderr, exit status, duration, and (when available) the native machine-readable report.
- A ledger record appended to `.context-guard/ledger.sqlite` for each invocation (command, repository state, artifact id, result summary, timestamp).
- Drill-down output from `context-guard artifact show <id> --fragment <fragment-id>`: the exact raw fragment (e.g. one failure's full traceback) referenced by the compact result.
- A benchmark report (CTX-01) recording baseline_output_bytes, compact_output_bytes, baseline_output_lines, compact_output_lines, compression_ratio, required_evidence_found, full_artifact_available, per the PRFAQ's Metrics Collected list.

## Functional Requirements
- FR-1: `context-guard test -- <command>` MUST execute the given command as a subprocess, capturing stdout, stderr, exit status, wall-clock duration, and the current repository commit hash (when inside a git repo).
- FR-2: The system MUST persist the complete captured result as a local artifact under `.context-guard/artifacts/test/<artifact-id>/` before returning any compact result, so the compact path can never be produced without the full evidence existing first.
- FR-3: The system MUST prefer native machine-readable test output when available (e.g. invoke pytest with `--junitxml` to a temp path and parse that) over parsing free-text output.
- FR-4: When native machine-readable output is unavailable or unparseable, the system MUST fall back to a deterministic pytest-specific text parser that identifies collected/passed/failed totals and, for each failure, the test name, file, line, and diagnostic message.
- FR-5: When the output format is not recognized by any parser, the system MUST return a safe fallback: exit status, a bounded preview (first/last N lines), and the full artifact reference — and MUST NOT invent a root-cause diagnosis.
- FR-6: The compact JSON result MUST include, at minimum, `status`, `tests.collected`, `tests.passed`, `tests.failed`, a `failures` array (each with `name`, `file`, `line`, `diagnostic`, `evidence`), and an `artifact` reference to the full stored result.
- FR-7: Each `evidence` reference in a compact result MUST resolve to an exact retrievable fragment of the stored artifact (Traceability, per PRFAQ FAQ #3).
- FR-8: `context-guard artifact show <artifact-id> --fragment <fragment-id>` MUST return the exact raw fragment referenced by a compact result's `evidence` field (Reversibility, per PRFAQ FAQ #3).
- FR-9: `context-guard artifact show <artifact-id>` without `--fragment` MUST return the complete stored raw output for that artifact.
- FR-10: Every compact result MUST state what was grouped, excluded, truncated, or left unparsed when the result is not a complete representation of the raw output (Explicit completeness, per PRFAQ FAQ #3).
- FR-11: The system MUST append one ledger record per compact-tool invocation to `.context-guard/ledger.sqlite`, containing at minimum: command, repository commit/state, artifact id, result summary (status/counts), and timestamp.
- FR-12: The system MUST NOT invoke an LLM or other model call to produce the compact result in this increment (deterministic parsers and safe fallback only, per PRFAQ FAQ #4).
- FR-13: The system MUST NOT store known secret file contents or environment-variable values in the artifact store or ledger by default.
- FR-14: A reproducible benchmark command MUST exist that runs the CTX-01 (Noisy test suite) scenario against a fixture test suite and reports baseline_output_bytes, compact_output_bytes, baseline_output_lines, compact_output_lines, compression_ratio, required_evidence_found, and full_artifact_available.

## Non-Functional Requirements
- NFR-1 (No network, no vector DB): Artifact storage, ledger, and parsing MUST work entirely locally using the filesystem plus SQLite; no vector database, embeddings, or network calls are required or introduced (PRFAQ FAQ #8).
- NFR-2 (No required extra model call): The core compact path (FR-1..FR-11) MUST function correctly with zero additional LLM calls; an optional model-assisted parser for unknown formats is explicitly out of scope for this increment (PRFAQ FAQ #4).
- NFR-3 (Evidence durability): Stored artifacts MUST remain retrievable for the lifetime of the local `.context-guard/` directory; deleting a compact result from model context MUST NOT delete the underlying artifact.
- NFR-4 (Bounded compact size): A compact result for a "noisy" fixture (thousands of passing lines, few failures) MUST be smaller than a reasonable byte/line budget (target: under 5% of raw output bytes for the CTX-01 fixture; treated as an observed benchmark result, not a hardcoded test assertion, per PRFAQ's "Quality gate" guidance).
- NFR-5 (Portability): Runs on macOS/Linux with Python 3.10+, consistent with specs/001-context-guard's NFR-4.
- NFR-6 (Fail-safety): A parser crash or unexpected output MUST fall back to FR-5's safe-fallback behavior rather than raising an unhandled exception that prevents any result from reaching the caller.
- NFR-7 (Auditability): Every invocation's ledger record (FR-11) must be sufficient to reconstruct which artifact corresponds to which command/repository state without re-running the command.

## Constraints
- This increment implements PRFAQ Rollout "Increment 2.1 — Test output" only; Increments 2.2 (logs/build), 2.3 (diff/search), 2.4 (ledger deduplication/staleness), and 2.5 (provider usage correlation) are explicitly deferred to future specs (see Out of Scope).
- No numerical context/token/cost savings claim may be published until a clean benchmark run against a named Context Guard version and commit populates qa.md's evidence section, per the PRFAQ's "Evidence status" notice. Any interim documentation must distinguish directly-measured local metrics from estimated/provider-billed metrics (PRFAQ FAQ #11).
- The parser must not "invent" a root cause when it cannot confidently identify one; unknown/unparseable output always uses the safe-fallback path (FR-5), never a best-guess diagnosis.
- Storage remains project-local (`.context-guard/`) filesystem plus SQLite; no cloud control plane, centralized collector, or vector database (PRFAQ "It is not" table).
- Compact Runtime must not delete or discard the original raw output; every design decision must preserve Reversibility (PRFAQ FAQ #3).
- Full Claude Code/Codex hook wiring (auto-recommending compact commands from Stage-1's PreToolUse hook) is out of scope for this increment; this spec delivers the standalone CLI/artifact/ledger vertical slice that a later increment wires into hooks.

## Acceptance Criteria
- AC-001: Given a pytest fixture suite with 20,000 passing tests and 1 failing test, when run via `context-guard test -- pytest`, then the compact JSON result reports `tests.collected: 20001`, `tests.passed: 20000`, `tests.failed: 1`, and the correct failing test's name, file, and line.
- AC-002: Given the same run, when the compact result's `failures[0].evidence` reference is passed to `context-guard artifact show <id> --fragment <fragment-id>`, then the exact diagnostic block (or full traceback) for that failure is returned.
- AC-003: Given the same run, when `context-guard artifact show <id>` is called without `--fragment`, then the complete raw stdout/stderr captured during execution is returned unchanged.
- AC-004: Given a test command whose output format is not recognized by any parser, when run via `context-guard test -- <command>`, then the result includes the correct exit status, a bounded preview, and a valid artifact reference, with no fabricated failure diagnosis.
- AC-005: Given any `context-guard test` invocation, when it completes, then exactly one new ledger record exists in `.context-guard/ledger.sqlite` referencing the correct artifact id and command.
- AC-006: Given the CTX-01 benchmark fixture, when the benchmark command is run, then it reports baseline_output_bytes, compact_output_bytes, baseline_output_lines, compact_output_lines, compression_ratio, required_evidence_found (true), and full_artifact_available (true), and compact_output_bytes is smaller than baseline_output_bytes.
- AC-007: Given a parser or execution failure (e.g. the test command itself crashes before producing output), when `context-guard test` runs, then it still returns a structured result (exit status and artifact reference) rather than crashing without producing any result (NFR-6).
- AC-008: Given a run where the underlying command output contains no secrets, when the artifact and ledger are inspected, then no environment-variable values are present in either (FR-13); this is verified by construction (the capture path does not read `os.environ`) rather than by scanning arbitrary output content.

## Out of Scope
- Increment 2.2 (logs/build output grouping by diagnostic signature, repeated-line compression, representative occurrences).
- Increment 2.3 (Git diff compaction, repository search compaction, generated-file exclusion).
- Increment 2.4 (Context Ledger deduplication: content hashes suppressing repeated unchanged reads, staleness detection, delta responses) — this spec's ledger only records invocations; it does not yet suppress or reference prior results.
- Increment 2.5 (provider usage correlation and any published cost/token-savings claim tied to provider billing).
- Automatic Claude Code/Codex hook wiring that transparently redirects raw test commands to `context-guard test` (Stage 1's PreToolUse hook may recommend this manually in documentation, but automatic interception is not built here).
- An optional model-assisted parser for unknown output formats (PRFAQ FAQ #4) — explicitly deferred, may be evaluated later.
- Support for test frameworks other than pytest in this increment (Jest, JUnit/Java, etc. are future work using the same parser-module pattern).
- A web dashboard, cloud control plane, or centralized artifact collection service.
- Vector database or semantic search over stored artifacts.

## Assumptions
- Assumption: pytest is the representative first framework because it has a stable machine-readable output mode (`--junitxml`) and is already used by this repository's own test suite (specs/001-context-guard), making dogfooding straightforward.
- Assumption: "artifact id" format follows the PRFAQ's worked example style, `test-<sequence>` (e.g. `test-018`), scoped per artifact kind (test/build/logs/diff/search) under `.context-guard/artifacts/<kind>/`.
- Assumption: the ledger schema in this increment is intentionally minimal (invocation-level record only); the richer schema described in PRFAQ FAQ #6 (file path/content hash, line ranges, search query/state, etc.) is deferred to Increment 2.4 and will extend rather than replace this table.
- Assumption: "required evidence found" for the benchmark (AC-006) is judged by the fixture's known single failing test being correctly identified in the compact result — a deterministic, scriptable check rather than manual judgment.
- Assumption: no changes to specs/001-context-guard's engine/policies are required; Compact Runtime is an additive `context_guard/compact/` subsystem plus new CLI subcommands alongside the existing `context-guard` CLI.

## Open Questions
- TODO(dm): Should `context-guard test -- <command>` shell out via `subprocess` with `shell=False` and an explicit argv list only, or also support a raw shell-string form? (Security/consistency implication for argument parsing.)
- TODO(dm): What retention/cleanup policy should apply to `.context-guard/artifacts/` over time (unbounded growth risk) — deferred until a maintainer decision, noted as a residual risk in qa.md.
- TODO(dm): Should the benchmark fixture suite be checked into this repo (tests/fixtures/compact/) or generated at benchmark-run time? This spec assumes checked-in fixtures for reproducibility.
- TODO(dm): Exact provider-hook wiring for "recommend compact alternative" (deferred to a later increment per Out of Scope) still needs a decision on whether it reuses specs/001-context-guard's `commands.py` `require_bounds` mechanism or introduces a new policy category.

## Decision Status
- Decision: Proceed with Increment 2.1 (test-output compaction vertical slice) only, deferring logs/build/diff/search/dedup/cost-correlation to later increments, per the PRFAQ's own rollout sequencing. Recorded as DEC-001 in decision-log.md.
- Status: Draft requirements ready for design; no blocking unresolved decision prevents starting design.md — open questions above are adapter/retention-level details that do not change the core contract (execute -> artifact -> parse -> compact result -> drill-down -> ledger).

