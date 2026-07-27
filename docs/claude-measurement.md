# Claude cache-token measurement

Context Guard measures Claude cache tokens from an explicit local JSONL session
file. It never searches your home directory, launches Claude, uploads logs, or
infers billed cost.

Measurement is available only after the corresponding baseline/guarded quality
pair passes the [quality runner](quality-runner.md).

## Extract a run

```bash
context-guard claude-measurement extract ~/.claude/projects/PROJECT/SESSION.jsonl \
  --run-id fixture-read-baseline-1 \
  --quality-pair fixture-read-quality-1 \
  --fixture-kind read-only-analysis \
  --role baseline \
  --version 2.1.218 \
  --model MODEL \
  --session-id SESSION
```

The adapter considers only matching assistant rows with Claude usage data. It
sums `cache_creation_input_tokens` and `cache_read_input_tokens`. Rows with the
same session, request ID, and message ID count once when their counters are
identical. Inconsistent duplicates, missing identifiers, malformed counters,
model drift, an empty window, or failed quality authorization are errors; no
missing value is reported as zero.

The result contains only identifiers, provider/model metadata, a source digest,
row counts, and native cache-token totals. Raw JSONL, paths, prompts, responses,
and message content are not persisted.

## Compare a pair

Save the two extraction results as JSON, then run:

```bash
context-guard claude-measurement pair \
  --baseline baseline.json \
  --guarded guarded.json \
  --pair-id fixture-read-pair-1 \
  --execution-order baseline-first
```

Reduction is the exact signed fraction:

```text
(baseline cache tokens - guarded cache tokens) / baseline cache tokens
```

Negative results are valid evidence and remain in the distribution. A zero
baseline, correlation mismatch, or later QA invalidation denies the pair.

## Qualify Claude

Qualification requires 15 distinct pair files: five for each frozen fixture
kind, in declared alternating baseline-first/guarded-first order.

```bash
context-guard claude-measurement qualify pairs/*.json \
  --qualification-id claude-pilot-1
```

Claude passes only when all quality authorizations remain current and:

- provider median reduction is at least 30%;
- nearest-rank Q1 is at least zero;
- every fixture median is at least zero.

Statistics use exact rational arithmetic and no outlier deletion. Inspect the
sanitized append-only local evidence with:

```bash
context-guard claude-measurement ledger
```
