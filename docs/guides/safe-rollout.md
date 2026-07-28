# Roll out Context Guard safely

## Goal

Evaluate policy fit without blocking work, then advance only with reviewed
evidence.

## When to use it

Use this for a personal evaluation, team pilot, or packaged-policy change.

## Prerequisites

Complete the [first run](../start-here/first-run.md) and read
[Stage 1 and Stage 2](../how-it-works/stages.md).

## Procedure

1. Keep the packaged policy in `observe`.
2. Collect normal-work audit and compact-runtime evidence.
3. Review false positives, missed operations, provider differences, and
   sensitive artifact handling.
4. Define explicit warning and enforcement acceptance criteria.
5. Change packaged policy only in a reviewed source change with focused tests.
6. Revalidate, self-test, and run a bounded pilot before broader rollout.

## Verify

Document the evaluated version, policy fingerprint, providers, observed rule
counts, reviewed false positives, known gaps, and rollback owner. Do not advance
if a self-test fails or evidence cannot be inspected.

## Troubleshooting

If local configuration appears to override policy, stop: version `0.1.2` does
not support such overrides. If a provider misses events, treat the gap as a
compatibility limitation.

## Next step

Use [compact output](compact-output.md) in normal read-only work or review the
[policy reference](../reference/policy.md).
