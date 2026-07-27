<div class="product-hero" markdown>
<p class="product-hero__eyebrow">AI SDLC product family · Control context</p>

# Context Guard

Stop predictable context waste before it reaches the active model context
while preserving full local evidence for later inspection.

Context Guard gives Claude Code and Codex users an observe-first policy layer
and a compact-output path. It keeps the active result bounded while retaining
the complete command or test evidence in the working repository.

<div class="product-hero__actions" markdown>
[Get started](start-here/index.md){ .md-button .md-button--primary }
[See how it works](how-it-works/index.md){ .md-button }
</div>
</div>

## The problem

- Large or generated files can fill active context before their useful ranges
  are identified.
- Unbounded logs, histories, and repository-wide searches often return far
  more evidence than the current decision needs.
- Summarizing output can lose failure detail unless the complete evidence is
  retained somewhere inspectable.

Context Guard is for developers and evaluators using Claude Code, Codex, or
both. It manages supported local events and command output; it does not control
the provider, model, billing system, or every tool operation.

## How it works

<div class="workflow" aria-label="Context Guard workflow">
  <div class="workflow-step"><strong>1. Observe</strong><span>Record policy-relevant events without blocking them.</span></div>
  <div class="workflow-step"><strong>2. Warn</strong><span>Surface a policy decision while allowing the operation.</span></div>
  <div class="workflow-step"><strong>3. Enforce</strong><span>Block a recognized operation when the packaged policy requires it.</span></div>
  <div class="workflow-step"><strong>4. Compact</strong><span>Return bounded command or test evidence.</span></div>
  <div class="workflow-step"><strong>5. Inspect</strong><span>Recover the complete local artifact or fragment.</span></div>
</div>

[Stage 1](how-it-works/stages.md#stage-1-policy-hooks) evaluates recognized
file-read, command, and search events. [Stage 2](how-it-works/stages.md#stage-2-compact-runtime)
captures full command output locally and emits a smaller result. The packaged
`0.1.1` policy starts in observe mode.

## Five-minute first success

Review and install from a local clone:

```bash
git clone https://github.com/mikegorelikoff/ai-sdlc-context.git
cd ai-sdlc-context
CONTEXT_GUARD_PACKAGE="$PWD" ./install.sh
context-guard validate
context-guard selftest
context-guard report
```

The installer initializes hooks for both providers and changes files under
`~/.claude/`, `~/.codex/`, and `~/.local/`. Success requires a `packaged:`
policy source, a self-test summary with no `FAIL`, and a JSON report. An empty
report is valid before the hooks observe normal activity.

Use [the full first-run guide](start-here/first-run.md) to check each result
and understand rollback before evaluating enforcement.

## What you get

<div class="path-cards" markdown>

- **Observe-first rollout**

  The default policy records what it would have prevented without blocking
  normal work.

- **Bounded active output**

  Recognized command families use specialized compactors; other explicitly
  proxied commands use generic bounded output.

- **Recoverable evidence**

  Full stdout, stderr, metadata, test reports, and exact fragments remain under
  `.context-guard/` for inspection.

- **Local evidence reports**

  Reports distinguish measured output bytes and a `bytes / 4` estimate from
  provider-reported token or billing data.

</div>

## Choose your path

<div class="path-cards" markdown>

- **New user**

  [Install in observe mode](start-here/index.md), validate, run self-test, and
  inspect the empty or initial report.

- **Evaluator or team lead**

  Review [safe rollout](guides/safe-rollout.md), trust boundaries, retained
  evidence, and stop criteria before considering warn or enforce.

- **Advanced user or maintainer**

  Use [Reference](reference/index.md) for policy, CLI, artifacts, profiles, and
  parser contracts. Measurement methodology is an advanced evidence path.

</div>

## Scope and limitations

<div class="scope-panel" markdown>

Context Guard does not intercept every provider operation. Claude Code may
rewrite recognized Bash calls through its installed hook; Codex can use the
proxy directly where the host exposes the required hook surface. Compound,
mutating, deployment, and unrecognized transparent-hook commands are left
unchanged. Output reduction does not guarantee model quality, prevented cost,
or lower provider billing. [Review all limitations](project/status-limitations.md).

</div>

## AI SDLC product family

<div class="product-family" markdown>

- [AI SDLC Harness](https://github.com/mikegorelikoff/ai-sdlc-harness) —
  structure delivery from request through evidence and handoff.
- <span class="status-badge">Current product</span> **Context Guard** — control
  avoidable context growth and retain complete local evidence.
- [AI SDLC Metrics](https://github.com/mikegorelikoff/ai-sdlc-metrics) —
  measure local Codex CLI and Claude Code adoption from available evidence.

</div>

The products are complementary and independently installed. No built-in
technical integration is implied.
