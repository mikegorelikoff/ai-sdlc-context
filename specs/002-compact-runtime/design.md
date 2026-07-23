---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "002-compact-runtime"
  artifact: "design.md"
  path: "specs/002-compact-runtime/design.md"
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
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
  related_artifacts:
    - "specs/002-compact-runtime/decision-log.md"
    - "specs/002-compact-runtime/requirements.md"
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
Compact Runtime is an additive subsystem, `context_guard/compact/`, alongside the existing Stage-1 `context_guard` package. The core flow for Increment 2.1 is: `context-guard test -- <command>` executes the command as a subprocess, captures stdout/stderr/exit status/duration, writes the complete result to a local artifact directory, invokes a pytest-aware parser (native junitxml first, deterministic text parser fallback, safe-fallback last), returns a small JSON summary with evidence references, and appends one row to a local SQLite ledger. `context-guard artifact show` reads back either the full artifact or an exact fragment referenced by a prior compact result. No network calls, no vector database, and no additional LLM call are used in this path.

## Architecture
```text
context-guard test -- <command>
        |
        v
compact/runner.py  --  subprocess execution: stdout, stderr, exit_status, duration, repo commit
        |
        v
compact/artifact_store.py  --  writes complete raw result under .context-guard/artifacts/test/<id>/
        |
        v
compact/parsers/pytest_junitxml.py  --  preferred: parse native --junitxml report
        |  (unavailable/unparseable)
        v
compact/parsers/pytest_text.py  --  deterministic fallback: text-based pytest summary/failure parser
        |  (unrecognized format)
        v
compact/parsers/fallback.py  --  safe fallback: exit status + bounded preview + artifact reference
        |
        v
compact/result.py  --  builds the bounded CompactResult (status, tests, failures[], artifact ref)
        |
        +--> stdout: compact JSON result (to the agent)
        +--> compact/ledger.py  --  one SQLite row per invocation
        +--> artifact remains on disk for compact/artifact_store.py show/fragment retrieval
```
`context-guard artifact show <id> [--fragment <fragment-id>]` reads directly from `compact/artifact_store.py`, independent of the run that produced the artifact. Parser selection is a fixed priority chain (native machine-readable -> deterministic framework parser -> generic/safe fallback), matching PRFAQ FAQ #4's "preferred processing order."

## Components
- `context_guard/compact/runner.py`: executes the given command via `subprocess.run` (argv list, `shell=False`), captures stdout/stderr/exit code/duration, and reads the current git commit hash via `git rev-parse HEAD` (best-effort, `None` if not a git repo).
- `context_guard/compact/artifact_store.py`: allocates a new artifact id per kind (e.g. `test-018`), writes `stdout.txt`, `stderr.txt`, `meta.json` (exit status, duration, command, commit, timestamp) and any native report file (e.g. `junit.xml`) under `.context-guard/artifacts/<kind>/<id>/`; exposes `read_full(id)` and `read_fragment(id, fragment_id)`.
- `context_guard/compact/parsers/pytest_junitxml.py`: parses a `--junitxml` report into totals and structured failures with `<file>:<line>` and a `fragment_id` per failure pointing at that failure's stored full traceback.
- `context_guard/compact/parsers/pytest_text.py`: deterministic regex/line-based fallback parser for pytest's default text summary line and `FAILED`/`short test summary info` sections when junitxml is unavailable.
- `context_guard/compact/parsers/fallback.py`: safe-fallback parser used when no framework-specific parser recognizes the output; returns exit status, a bounded head/tail preview, and the artifact reference only.
- `context_guard/compact/result.py`: defines `CompactResult` and `Failure` dataclasses and serializes them to the PRFAQ's compact JSON shape.
- `context_guard/compact/ledger.py`: opens/creates `.context-guard/ledger.sqlite`, defines the `invocations` table, and exposes `record(...)` used by the CLI after each run.
- `context_guard/compact/fragments.py`: shared fragment-id scheme (e.g. `failure-1`, `preview-head`, `preview-tail`) used consistently by all parsers and by `artifact show --fragment`.
- CLI additions in `context_guard/cli.py`: `test` positional-passthrough subcommand (`context-guard test -- <command...>`) and `artifact show <id> [--fragment <fragment-id>]` subcommand, both dispatching into `compact/`.
- `tests/fixtures/compact/`: a small checked-in pytest fixture suite (many passing tests, one deliberate failure) used by both the pytest test-cases and the CTX-01 benchmark script.
- `scripts/benchmark_ctx01.py` (or `context_guard/compact/benchmark.py`): runs the fixture suite via both a raw baseline invocation and `context-guard test`, and reports the PRFAQ's Metrics Collected fields for CTX-01.

## Interfaces and Contracts
- CLI contract: `context-guard test -- <command...>` executes exactly the given argv (no shell interpretation), always writes an artifact before printing any result, and always prints exactly one JSON object to stdout representing a `CompactResult`, even on parser or safe-fallback paths (FR-2, FR-5).
- `CompactResult` contract (`result.py`): `{"status": "passed"|"failed"|"error"|"unparsed", "tests": {"collected": int, "passed": int, "failed": int} | None, "failures": [Failure], "artifact": "artifact:<kind>-<id>", "notes": [str]}`. `notes` carries FR-10's "what was grouped/excluded/truncated/unparsed" statement; it is always present, even if empty.
- `Failure` contract: `{"name": str, "file": str, "line": int, "diagnostic": str, "evidence": "artifact:<kind>-<id>#<fragment-id>"}`. Every `evidence` string MUST be resolvable by `artifact_store.read_fragment`.
- Parser module contract: each parser under `compact/parsers/` exposes `parse(raw: RawCapture) -> CompactResult | None`, returning `None` when it cannot confidently parse the given output so the next parser in the priority chain is tried; the fallback parser never returns `None`.
- `artifact_store.py` contract: `allocate(kind: str) -> ArtifactId`, `write(id, files: dict[str, bytes])`, `read_full(id) -> RawCapture`, `read_fragment(id, fragment_id) -> str`; fragment ids are stable strings recorded alongside the artifact so a later `show --fragment` call is independent of parser internals.
- `ledger.py` contract: `record(command: str, commit: str | None, artifact_id: str, summary: dict, timestamp: str) -> None`; no `read`/query API is required by this increment beyond what manual SQLite inspection provides (query API is deferred to Increment 2.4's deduplication work).

## Data Model
- `RawCapture` (in-memory, per-invocation): `{command: list[str], stdout: bytes, stderr: bytes, exit_code: int, duration_seconds: float, commit: str|None, timestamp: str, native_report_path: str|None}`.
- Artifact on disk (`.context-guard/artifacts/test/<id>/`): `stdout.txt`, `stderr.txt`, `meta.json` (command, exit_code, duration_seconds, commit, timestamp), and `junit.xml` when native machine-readable output was produced. `<id>` is a monotonically increasing per-kind sequence, e.g. `test-018`.
- `CompactResult`/`Failure` (in-memory + serialized JSON): see Interfaces and Contracts.
- Ledger table `invocations` (SQLite, `.context-guard/ledger.sqlite`): columns `id INTEGER PRIMARY KEY`, `timestamp TEXT`, `command TEXT`, `commit TEXT`, `artifact_kind TEXT`, `artifact_id TEXT`, `status TEXT`, `summary_json TEXT`. This is intentionally the minimal invocation-level schema; PRFAQ FAQ #6's richer per-file/per-range ledger fields are additive columns/tables planned for Increment 2.4, not built here.
- Fragment index (`.context-guard/artifacts/test/<id>/fragments.json`): maps each `fragment_id` (e.g. `failure-1`, `preview-head`) to a byte offset/length or line range within `stdout.txt`/`stderr.txt`/`junit.xml`, so `read_fragment` is a direct lookup rather than re-parsing.

## Error Handling
- Subprocess launch failure (e.g. command not found): captured as `exit_code` from the OS error, artifact still written with whatever stdout/stderr exists (possibly empty) plus an explanatory `meta.json` field; result status is `"error"` with an empty `failures` list and a `notes` entry explaining the launch failure (AC-007).
- Native junitxml parse failure (malformed XML): `pytest_junitxml.py` returns `None`; the chain falls through to `pytest_text.py`, then to `fallback.py` if that also fails — never raises out of the parser chain.
- Text parser ambiguity (output doesn't match known pytest patterns): `pytest_text.py` returns `None` rather than guessing; falls through to the safe fallback (FR-5).
- Ledger write failure (e.g. SQLite locked/disk full): best-effort, logged to stderr, and does not block returning the compact result to the caller — the artifact on disk remains the durable record even if the ledger entry is lost (mirrors specs/001-context-guard's audit-log fail-safety pattern).
- Artifact write failure (disk full, permissions): this is fatal for the increment's core guarantee (FR-2: artifact before compact result) — `context-guard test` exits non-zero with a clear error rather than returning a compact result with no backing evidence.
- `artifact show` on an unknown id/fragment: returns a clear "not found" error (non-zero exit), never silently returns empty or unrelated content.

## Security Considerations
- `runner.py` executes the given command with `shell=False` and an explicit argv list (never a raw shell string), so `context-guard test -- <command>` cannot be used for shell-metacharacter injection the way a naive `shell=True` wrapper could.
- The capture path does not read `os.environ` and does not write environment-variable values into `meta.json`, `stdout.txt`/`stderr.txt` capture is limited to what the child process itself printed (FR-13, AC-008).
- Artifacts and the ledger are local-only (no network transmission); the security surface is equivalent to the test command's own output already being on disk, not a new exposure vector, but retention is unbounded in this increment (tracked as a residual risk in qa.md pending the retention-policy Open Question).
- `context-guard artifact show` performs no path traversal beyond validated artifact ids resolved against the known `.context-guard/artifacts/<kind>/` root; a malformed or unknown id must be rejected rather than resolved as an arbitrary filesystem path.
- This remains explicitly not a security product, consistent with specs/001-context-guard's requirements Constraints; Compact Runtime does not scan stored output for secrets before writing it (that is a future hardening item, not a Increment 2.1 requirement).

## Observability
- Every `context-guard test` invocation produces one artifact directory and one ledger row, giving a complete local audit trail of what was executed, when, and what compact result was returned (NFR-7).
- The `notes` field on every `CompactResult` (FR-10) makes truncation/grouping/exclusion decisions visible in the result itself, rather than requiring a separate log inspection to understand what was left out.
- The CTX-01 benchmark script (FR-14) is itself an observability tool: it reports the compression ratio and evidence-preservation outcome for a known fixture, giving a repeatable signal for whether the compaction is working as intended before any cost claim is made.
- `context-guard artifact show <id>` (no flags) gives a direct way to audit exactly what a compact result was derived from, supporting manual verification during development and review.

## Risks and Tradeoffs
- Parser blind spots: a pytest output variant (plugin-modified output, custom reporters) could fall through both the junitxml and text parsers; mitigated by the mandatory safe-fallback path (FR-5) so the agent always gets exit status and a full artifact reference even when parsing fails, per PRFAQ risk "parsers routinely miss the root diagnostic."
- Unbounded artifact growth: repeated runs accumulate artifacts with no retention policy in this increment; tracked as an explicit residual risk (see Open Questions and qa.md) rather than silently deferred.
- Perceived vs. actual savings: this spec deliberately keeps the benchmark's evidence separate from any published cost claim (PRFAQ "Evidence status" notice); the risk of overclaiming is mitigated by qa.md's evidence section staying TBD until a clean benchmark run.
- Drill-down overuse: if fragment/evidence references are miscomputed, an agent's drill-down request could return the wrong fragment; mitigated by AC-002/AC-003 test coverage asserting fragment correctness against the fixture's known failure.
- Scope creep into Increment 2.2+: because the compact/ subsystem is designed to be reused by later increments (parser priority chain, artifact store, ledger), there is a temptation to over-generalize now; mitigated by keeping this spec's Scope strictly to Increment 2.1 and deferring generalization decisions to when Increment 2.2 actually needs them.

## Validation Strategy
- Unit tests per parser (`compact/parsers/pytest_junitxml.py`, `pytest_text.py`, `fallback.py`) against captured/fixture pytest output covering: all-pass, single-failure, multiple-failure, and unrecognized-format cases.
- Unit tests for `artifact_store.py` covering allocate/write/read_full/read_fragment round-trips and unknown-id/unknown-fragment error handling.
- Unit tests for `ledger.py` covering record insertion and schema correctness.
- End-to-end CLI tests invoking `context-guard test -- <fixture command>` as a subprocess/direct call and asserting the compact JSON result, the artifact on disk, and the ledger row — matching AC-001, AC-003, AC-005, AC-007.
- A drill-down test asserting `context-guard artifact show <id> --fragment <fragment-id>` returns the correct fragment for a known fixture failure (AC-002).
- The CTX-01 benchmark script itself, run against `tests/fixtures/compact/` (a large generated passing suite plus one deliberate failure), asserting compact_output_bytes < baseline_output_bytes and required evidence found (AC-006).
- Use `$ai-sdlc-validation` for repository-wide command selection during implementation and commit prep, consistent with specs/001-context-guard.

## Migration Notes
This is an additive subsystem alongside the existing specs/001-context-guard implementation; no changes to `context_guard/engine.py`, `policies/`, or the Stage-1 CLI subcommands (`install`, `validate`, `doctor`, `report`, `init`, `hook`) are required. `.context-guard/` gains new subdirectories (`artifacts/`, `ledger.sqlite`) alongside the existing `audit.jsonl` and `sessions/`; no migration of existing Stage-1 data is needed. `context-guard test` and `context-guard artifact` are new subcommands added to the existing `cli.py` argument parser.

