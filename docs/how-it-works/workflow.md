# Workflow and rollout

Context Guard separates initial observation from policy enforcement and
evidence compaction.

<div class="workflow" aria-label="Observe to inspect workflow">
  <div class="workflow-step"><strong>Observe</strong><span>Collect applicable local decisions without blocking work.</span></div>
  <div class="workflow-step"><strong>Warn</strong><span>Confirm that warnings are actionable and correctly scoped.</span></div>
  <div class="workflow-step"><strong>Enforce</strong><span>Block only after reviewed evidence supports the policy.</span></div>
  <div class="workflow-step"><strong>Compact</strong><span>Use bounded active output for supported commands and tests.</span></div>
  <div class="workflow-step"><strong>Inspect</strong><span>Recover complete evidence by artifact or fragment ID.</span></div>
</div>

## Safe default

Begin with the packaged observe policy. Review false positives, missed
operations, failure behavior, provider differences, and local artifact
handling. Do not infer readiness from output-reduction percentages alone.

## Advancing modes

The runtime supports `warn` and `enforce`, but the current product accepts one
packaged policy only. A rollout decision therefore belongs in a reviewed
source/package change with tests and release evidence. Local override files and
environment variables do not change the mode.

## Evidence strength

Fixture evidence proves deterministic behavior against known inputs. A single
baseline/guarded pair shows one bounded comparison. Repeated, counterbalanced
pairs provide stronger evidence about consistency. None of these alone proves
provider cost savings or model-quality improvement.

Use the [safe rollout guide](../guides/safe-rollout.md) for a task-oriented
procedure.
