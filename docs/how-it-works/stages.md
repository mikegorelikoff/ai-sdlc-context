# Stage 1 and Stage 2

This page separates the policy-hook behavior from compact-output behavior so
you can evaluate each boundary independently.

## Stage 1: policy hooks

Provider adapters parse supported hook events into file-read, command, and
search operations. The engine evaluates the packaged policy:

- `observe` records the decision but allows the operation.
- `warn` returns a visible warning and allows the operation.
- `enforce` returns the underlying block decision.

Internal policy errors fail open unless the matching rule is explicitly listed
in `fail_closed_rules`. The current packaged list is empty.

Stage 1 does not compact output. It identifies avoidable patterns such as full
reads of oversized or generated files, unbounded log/history commands, and
searches without path or result scope.

## Stage 2: compact runtime

`context-guard run -- <command>` and `context-guard test -- <command>` execute
an explicitly supplied command. Specialized filters handle recognized command
families; a generic bounded fallback handles other explicitly proxied
commands.

The runtime stores complete stdout, stderr, metadata, and available failure
fragments under `.context-guard/artifacts/`. The active result contains a
bounded summary and an artifact ID that can be inspected later.

## Provider difference

Claude Code's installed Bash hook can transparently rewrite recognized command
families to the proxy. Codex can call the proxy directly when its hook surface
does not provide equivalent transparent rewriting. Compound shell expressions
and mutating or deployment commands are left unchanged by transparent
rewriting.

Next, read the [rollout workflow](workflow.md).
