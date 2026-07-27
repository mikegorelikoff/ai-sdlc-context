# Real-world examples

These examples use the same inventory, guarded-profile planning, quality, and
provider measurement code as Context Guard itself. They are split into three
evidence levels so fixture numbers are never confused with measured local
results or a qualified savings claim.

## 1. Run the reproducible demo

From a source checkout:

```bash
python3 examples/run_demo.py --check
```

The runner creates a temporary home directory, installs three example skills,
authorizes one quality pair per provider, reads provider-native JSONL fixtures,
and prints privacy-safe evidence. It neither reads nor changes your real home
directory.

Selected output:

```json
{
  "evidence_kind": "deterministic-fixture",
  "claude": {
    "profile_plan": {
      "overrides": {"unused": "user-invocable-only"},
      "fresh_session_required": true
    },
    "measurement": {
      "cache_creation_tokens": 1200,
      "cache_read_tokens": 3800,
      "cache_tokens": 5000
    },
    "paired_example": {
      "baseline_cache_tokens": 5000,
      "guarded_cache_tokens": 3000,
      "reduction_percent": 40
    }
  },
  "codex": {
    "profile_plan": {
      "disabled_skills": ["unused"],
      "fresh_process_required": true
    },
    "measurement": {
      "measurement_mode": "exact-event",
      "cached_input_tokens": 4200
    },
    "paired_example": {
      "baseline_cached_input_tokens": 4200,
      "guarded_cached_input_tokens": 2520,
      "reduction_percent": 40
    }
  },
  "fail_closed_examples": {
    "missing_quality_evidence": {
      "measurement_allowed": false,
      "reason_code": "missing-quality-evidence"
    },
    "unsupported_provider_version": {
      "status": "unsupported",
      "reason_code": "unsupported-version"
    }
  }
}
```

The paired fixture demonstrates the exact fraction `(baseline - guarded) /
baseline`: Claude falls from 5000 to 3000 cache tokens and Codex from 4200 to
2520 cached-input tokens, which is 40% in both cases. This is an executable
calculation example, not a published production-savings claim.

The same run also demonstrates three safety properties:

- `needed` remains enabled because it is classified `required`;
- `manual` remains enabled despite an `irrelevant` classification because it
  was explicitly invoked;
- unsupported provider versions and missing quality evidence fail closed
  instead of receiving savings credit.

Additional executable scenarios in the complete output:

| Scenario | Claude | Codex |
| --- | --- | --- |
| Apply and restore | `reduced → restored`, original settings restored byte-for-byte | `reduced → restored`, generated profile removed |
| Negative pair | `5000 → 6000`, `-20%`, regression retained | `4200 → 5040`, `-20%`, regression retained |
| Cumulative boundary | Not applicable | `1000 → 4200`, measured delta `3200` |
| Stale inventory | `uncertain`, no savings credit | Same fail-closed inventory contract |

Negative results are intentionally visible. Context Guard does not delete
outliers or turn a regression into zero savings.

The complete result is generated at
`examples/output/demo-output.json`. Refresh it intentionally with:

```bash
python3 examples/run_demo.py --write
```

`--check` returns non-zero if production behavior and the checked-in example
drift apart.

## 2. Inspect your real local skill inventory

Inventory reads the current provider-owned skill directories twice and accepts
them only when both reads match:

```bash
context-guard inventory \
  --provider claude \
  --version 2.1.218 \
  --surface cli \
  --home "$HOME"

context-guard inventory \
  --provider codex \
  --version 0.144.1 \
  --surface cli \
  --home "$HOME"
```

The inventory output includes local skill locators, so do not paste the raw
result into public issues. A sanitized local smoke run on 2026-07-27 produced:

```text
claude: status=supported reason=stable-inventory skills=27 fingerprint_present=True
codex:  status=supported reason=stable-inventory skills=27 fingerprint_present=True
```

This snapshot proves that both real provider roots can be inventoried on one
active developer machine. It is not a token-reduction benchmark.

## 3. Apply guarded profiles

Classify every inventoried skill. Only an exact `irrelevant` classification is
reduced; required, safety-critical, uncertain, and explicitly invoked skills
remain available.

Claude Code:

```bash
context-guard claude-profile apply "$HOME/.claude/settings.local.json" \
  --run-id example-claude-apply \
  --version 2.1.218 \
  --inventory-fingerprint INVENTORY_SHA256 \
  --classification unused-skill=irrelevant \
  --classification required-skill=required
```

Start a fresh Claude Code session only when the result reports
`fresh_session_required: true`. Restore afterward:

```bash
context-guard claude-profile restore "$HOME/.claude/settings.local.json" \
  --run-id example-claude-restore \
  --version 2.1.218
```

Codex:

```bash
context-guard codex-profile apply \
  --home "$HOME" \
  --profile context-guard \
  --run-id example-codex-apply \
  --version 0.144.1 \
  --inventory-fingerprint INVENTORY_SHA256 \
  --classification unused-skill=irrelevant \
  --classification required-skill=required \
  --skill "unused-skill=$HOME/.agents/skills/unused-skill/SKILL.md" \
  --skill "required-skill=$HOME/.agents/skills/required-skill/SKILL.md"

codex --profile context-guard
```

Restore the generated profile after the fresh process finishes:

```bash
context-guard codex-profile restore \
  --home "$HOME" \
  --profile context-guard \
  --run-id example-codex-restore \
  --version 0.144.1
```

Both providers preserve private recovery state and use compare-and-swap
restoration, so a user edit is never silently overwritten.

## 4. Measure real provider logs

Measurement never searches your home directory. Select one explicit local file
after its baseline/guarded pair passes the [Quality Runner](quality-runner.md).

Claude Code:

```bash
context-guard quality authorize REAL_CLAUDE_QUALITY_PAIR

context-guard claude-measurement extract \
  "$HOME/.claude/projects/PROJECT/SESSION.jsonl" \
  --run-id real-claude-baseline-1 \
  --quality-pair REAL_CLAUDE_QUALITY_PAIR \
  --fixture-kind read-only-analysis \
  --role baseline \
  --version 2.1.218 \
  --model MODEL \
  --session-id SESSION_ID
```

The result contains cache creation/read totals, row counts, and a source digest.
It does not persist the source path, prompts, responses, or raw JSONL.

Codex exact `exec --json` event:

```bash
context-guard quality authorize REAL_CODEX_QUALITY_PAIR

context-guard codex-measurement exact ./codex-exec.jsonl \
  --run-id real-codex-baseline-1 \
  --quality-pair REAL_CODEX_QUALITY_PAIR \
  --fixture-kind read-only-analysis \
  --role baseline \
  --version 0.144.1 \
  --model MODEL \
  --thread-id THREAD_ID
```

For cumulative session counters, declare the two observed boundaries:

```bash
context-guard codex-measurement cumulative \
  --run-id real-codex-baseline-1 \
  --quality-pair REAL_CODEX_QUALITY_PAIR \
  --fixture-kind read-only-analysis \
  --role baseline \
  --version 0.144.1 \
  --model MODEL \
  --thread-id THREAD_ID \
  --start-boundary before-turn \
  --end-boundary after-turn \
  --start-cached-input 1000 \
  --end-cached-input 4200
```

## What counts as proof?

| Evidence | What it proves | What it does not prove |
| --- | --- | --- |
| Checked-in deterministic fixture | Production parsers, privacy filtering, and profile decisions behave reproducibly | Savings on your project |
| One local baseline/guarded pair | Exact reduction for that provider, model, fixture, and pair | A general 30% reduction |
| Qualified 5×3 run | Provider median is at least 30%, Q1 is non-negative, and every fixture median is non-negative | A universal guarantee for every future task |

Claude Code and Codex qualify independently. Context Guard never pools their
measurements or converts token counts into inferred billing cost.
