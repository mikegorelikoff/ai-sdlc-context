# Codex cached-input measurement

Context Guard measures Codex `cached_input_tokens` without launching Codex,
searching your home directory, uploading logs, or inferring billed cost.
Measurement is allowed only after the matching baseline/guarded pair passes the
[quality runner](quality-runner.md).

## Exact `codex exec --json` event

Give Context Guard one explicit JSONL file containing exactly one matching
`thread.started` event and one `turn.completed` event:

```bash
context-guard codex-measurement exact codex-exec.jsonl \
  --run-id fixture-read-baseline-1 \
  --quality-pair fixture-read-quality-1 \
  --fixture-kind read-only-analysis \
  --role baseline \
  --version 0.144.1 \
  --model MODEL \
  --thread-id THREAD
```

Only `usage.cached_input_tokens` is retained. Missing usage, malformed or
negative counters, thread mismatch, multiple completion events, malformed
JSONL, and failed quality authorization are errors. The local ledger contains a
source digest but no path, raw event, prompt, response, or item content.

## Cumulative boundary delta

For a local Codex session log, first read two explicit cumulative
`cached_input_tokens` boundaries, then pass only their identifiers and values:

```bash
context-guard codex-measurement cumulative \
  --run-id fixture-read-baseline-1 \
  --quality-pair fixture-read-quality-1 \
  --fixture-kind read-only-analysis \
  --role baseline \
  --version 0.144.1 \
  --model MODEL \
  --thread-id THREAD \
  --start-boundary before-turn \
  --end-boundary after-turn \
  --start-cached-input 1000 \
  --end-cached-input 1400
```

The measured value is the exact `end - start` delta. Equal boundary IDs,
negative values, and counter resets are rejected rather than replaced with
zero.

## Compare and qualify

Save baseline and guarded run results as JSON, then compare them:

```bash
context-guard codex-measurement pair \
  --baseline baseline.json \
  --guarded guarded.json \
  --pair-id fixture-read-pair-1 \
  --execution-order baseline-first
```

Reduction is retained as an exact signed fraction:

```text
(baseline cached input - guarded cached input) / baseline cached input
```

Qualification requires 15 distinct pairs—five for each frozen fixture kind—in
alternating baseline-first/guarded-first order:

```bash
context-guard codex-measurement qualify pairs/*.json \
  --qualification-id codex-pilot-1
```

Codex passes only when the provider median is at least 30%, nearest-rank Q1 is
non-negative, every fixture median is non-negative, and every quality
authorization remains current. No providers are pooled and no outliers are
deleted.

```bash
context-guard codex-measurement ledger
```
