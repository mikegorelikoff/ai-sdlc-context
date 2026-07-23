# Compact Runtime Reference

Compact Runtime is Context Guard Stage 2 (`specs/002-compact-runtime`): it executes a command, preserves the complete result locally, and returns a bounded structured summary with drill-down references instead of raw output. This document covers Increment 2.1 (test output) — see `specs/002-compact-runtime/requirements.md` for the full rollout plan and out-of-scope increments.

## Usage

```bash
context-guard test -- pytest
```

```json
{
  "status": "failed",
  "tests": {"collected": 20001, "passed": 20000, "failed": 1},
  "failures": [
    {
      "name": "test_duplicate_callback",
      "file": "tests/payment/test_callbacks.py",
      "line": 143,
      "diagnostic": "Expected one event, found two",
      "evidence": "artifact:test-018#failure-1"
    }
  ],
  "artifact": "artifact:test-018",
  "notes": []
}
```

Drill down into exact evidence:

```bash
context-guard artifact show test-018 --fragment failure-1   # one failure's exact traceback
context-guard artifact show test-018                        # the complete stdout/stderr/junit.xml
```

## Parser priority chain

1. **Native machine-readable output** — when the command is `pytest`, Context Guard adds `--junitxml=<tmp>` and parses that report (`context_guard/compact/parsers/pytest_junitxml.py`).
2. **Deterministic text parser** — falls back to parsing pytest's default console summary/failure lines when junitxml is unavailable or unparseable (`pytest_text.py`).
3. **Safe fallback** — when no parser recognizes the output, returns exit status, a bounded preview, and the full artifact reference, and never fabricates a root cause (`fallback.py`).

Every `CompactResult` includes a `notes` list stating what was grouped, excluded, truncated, or left unparsed, even when that list is empty.

## Storage layout

```text
.context-guard/
├── artifacts/
│   └── test/
│       └── test-018/
│           ├── stdout.txt
│           ├── stderr.txt
│           ├── meta.json        # command, exit_code, duration, commit, timestamp
│           ├── junit.xml        # present only when native machine-readable output was produced
│           └── fragments.json   # fragment_id -> {"content": str} or {"file","start","end"}
└── ledger.sqlite                 # one row per invocation: command, commit, artifact id, status, summary
```

Artifacts are never deleted by the compact path — the full raw output is always retrievable via `context-guard artifact show`, even after the compact result has left the agent's context.

## What is and is not stored

- Full stdout/stderr and (when available) the native test report are stored, since they were already being printed by the underlying command.
- Environment-variable values are never read or written to the artifact/ledger by construction — the capture path does not access `os.environ`.
- The ledger schema in this increment is invocation-level only (command, commit, artifact id, status, summary). The richer per-file/per-range ledger needed for deduplication is planned for a later increment (PRFAQ Increment 2.4) and is not built here.

## CTX-01 benchmark

```bash
python3 -m context_guard.compact.benchmark tests/fixtures/compact/test_generated.py
```

Reports `baseline_output_bytes`, `compact_output_bytes`, `baseline_output_lines`, `compact_output_lines`, `compression_ratio`, `required_evidence_found`, and `full_artifact_available` for the CTX-01 (noisy test suite) scenario. Per the PRFAQ's evidence-status requirement, no percentage-reduction claim should be published until this has been run on a clean checkout against a named Context Guard version/commit — see `specs/002-compact-runtime/qa.md` for the evidence-recording template.

## Not included in this increment

Logs/build output grouping, Git diff and repository search compaction, Context Ledger deduplication (suppressing repeated unchanged reads), and provider-usage cost correlation are later PRFAQ increments (2.2–2.5), not part of this build. See `specs/002-compact-runtime/requirements.md#Out of Scope`.
