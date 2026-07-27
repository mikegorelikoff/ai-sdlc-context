# How it works

Context Guard combines two independent mechanisms: policy hooks that make
context-risk decisions and a compact runtime that bounds active command output
while retaining full local evidence.

## Recommended reading order

1. [Stage 1 and Stage 2](stages.md)
2. [Workflow and rollout](workflow.md)
3. [Trust boundaries](trust-boundaries.md)
4. [Packaged policy reference](../reference/policy.md)
5. [CLI reference](../reference/cli.md)

The default first path is observe mode. Warn and enforce are supported policy
modes, but version `0.1.1` loads one packaged policy and does not accept user,
repository, or environment overrides. Advancing a mode therefore requires a
reviewed packaged-policy change, not an ad hoc local file.

Context Guard complements AI SDLC Harness and AI SDLC Metrics but installs and
operates independently.
