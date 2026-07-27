# Run the repository examples

## Goal

Reproduce the checked demonstration output from bundled local fixtures.

## When to use it

Use it when evaluating behavior without depending on your real agent history.

## Prerequisites

Clone the repository and use Python 3.10 or newer.

## Procedure

```bash
python3 examples/run_demo.py --check
```

The script compares its result with
`examples/output/demo-output.json`.

## Verify

The command must exit zero. The checked output covers positive reductions,
regressions, cumulative accounting, profile application/restoration,
fail-closed cases, and privacy checks. Treat it as fixture evidence, not as a
benchmark for your repository or provider.

## Troubleshooting

If the fixture check fails, record the exact diff and Python version. Do not
replace the expected fixture merely to make the check pass.

## Next step

Run a normal [compact-output command](compact-output.md), or read
[advanced measurement](measurement.md).
