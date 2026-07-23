# Context Guard

## The problem

Claude Code and Codex sessions grow expensive in predictable, repeatable ways: an agent reads a full lock file to check one dependency version, a test command returns thousands of passing lines to surface two failures, container logs stream unbounded, a repository-wide search scans `node_modules/` and build output, and the same large file gets read in full more than once in a session.

None of this raw data is useless — the problem is that the *entire* result commonly lands in the active model context even when the agent needed only a small, identifiable part of it. Once that happens, it can keep being reprocessed on every subsequent model call in the session, adding ordinary input tokens, cache reads, and cache writes, and pushing sessions toward compaction sooner.

Provider dashboards show token totals after the fact. They don't give a repository-level policy that stops the inefficient action *before* it happens, and they don't distinguish "this agent needed this evidence" from "this agent got 20,000 lines it never looked at."

## What Context Guard does about it

Context Guard is a local policy engine, not an AI model or a proxy. It hooks into Claude Code's and Codex's lifecycle events and intervenes at two points:

- **[Stage 1 — Context Guard](policy.md)** stops the predictable waste outright: it blocks or warns on full reads of oversized/generated files, unbounded log and history commands, and unscoped repository search — before the tool call happens, deterministically, with no model in the loop.
- **[Stage 2 — Compact Runtime](compact-runtime.md)** handles the operations that can't just be blocked, because the agent genuinely needs the outcome (did the tests pass? what changed?). It runs the operation, keeps the complete result on disk, and hands the agent a bounded summary — one failing test out of twenty thousand passing lines, with an exact reference to drill into if the summary isn't enough. Nothing is discarded; the full evidence stays addressable.

Both stages run entirely on the developer's machine: no vector database, no cloud control plane, and no centralized collection of source code or prompts.

## Install

```bash
git clone https://github.com/mikegorelikoff/ai-sdlc-context.git
cd ai-sdlc-context
pipx install .
```

## Quickstart

```bash
context-guard init             # creates .context-guard/policy.yaml (starts in observe mode)
context-guard install claude   # wires Context Guard into Claude Code hooks
context-guard install codex    # wires Context Guard into Codex hooks
context-guard validate         # checks policy schema + hook install status
context-guard selftest         # runs the bundled fixture smoke tests

context-guard test -- pytest   # Compact Runtime: run a test command, get a compact result
```

## Where to go next

- [Policy Reference](policy.md) — the full Stage 1 policy schema, modes, and config layering.
- [Compact Runtime Reference](compact-runtime.md) — Stage 2's artifact store, ledger, and parser chain.
- [Source on GitHub](https://github.com/mikegorelikoff/ai-sdlc-context) — requirements, design, and test-case packages live under `specs/`.
