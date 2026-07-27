# Context Guard Policy Reference

Stage 1 stops a small set of high-cost operations before they ever reach the model: full reads of oversized or generated files, unbounded log/history commands, and unscoped repository search. Every rule below evaluates deterministically — no LLM call is involved in the decision.

## Configuration layering

Effective policy is resolved in this order, later layers overriding earlier ones field-by-field:

1. Built-in defaults — `context_guard/defaults/policy.yaml`, shipped with the package.
2. User config — `~/.config/context-guard/policy.yaml`.
3. Repo config — `<repo>/.context-guard/policy.yaml` (create with `context-guard init`).
4. Environment overrides — currently `CONTEXT_GUARD_MODE` overrides the global `mode`.

## Schema

```yaml
version: 1

mode: observe   # observe | warn | enforce (global default; overridable per rule group below)

files:
  max_full_read_bytes: 200000        # full reads above this size are blocked without a bounded range
  require_range_above_bytes: 50000   # reads above this size require an explicit bounded range
  deny:                              # glob patterns; matching paths are always blocked for full reads
    - "**/node_modules/**"
    - "**/dist/**"
    - "**/*.min.js"
    - "**/*.map"

commands:
  maximum_expected_output_lines: 500
  require_bounds:                    # command families that must include a recognized bound flag
    - "docker logs"
    - "docker compose logs"
    - "kubectl logs"
    - "git log"

search:
  require_path_scope: true           # unscoped repo-root searches are blocked
  maximum_results: 100               # searches without a result-limit flag are blocked when unscoped

fail_closed_rules: []                # rule ids that block (instead of allow) on internal evaluation errors
```

Version 1 remains supported and is interpreted as having no skill-relevance
rules. New relevance policies use version 2:

```yaml
version: 2

skills:
  rules:
    - id: test-tools-not-needed
      enabled: true
      provider: any                  # claude | codex | any
      skill: organization.test-tools # exact authoritative identity
      outcome: irrelevant            # safety-critical | required | irrelevant
      task_ids: [DOCS-ONLY]           # optional exact selectors
      repositories: [docs-site]       # optional exact selectors
      reason_code: task-excludes-tests
```

Rules are merged across layers by `id`. A later same-ID rule replaces the
entire earlier rule; omitted fields are not inherited. `enabled: false`
disables the rule. Duplicate IDs within one layer and unknown fields are
invalid.

Classification uses exact skill identities and the precedence
`safety-critical` > `required` > `irrelevant`. Only an exact, enabled,
unconflicted `irrelevant` match may reduce visibility. Unknown identities,
selector mismatches, and conflicts keep the skill required.

Validation errors include a stable code and dotted field path, for example
`POLICY_INVALID_VALUE at ...:skills.rules[0].provider`. Future policy versions
are rejected. Existing version-1 files load without being rewritten; migration
to version 2 is explicit.

`context-guard init` creates a version-2 repository policy and never overwrites
an existing file. To migrate an existing repository policy explicitly:

```bash
context-guard validate
context-guard migrate-policy
context-guard validate
```

Migration validates the version-1 source, creates a byte-identical
`policy.yaml.v1.bak` without overwriting an existing backup, validates the
version-2 candidate, and atomically replaces `policy.yaml`. Running it against
an existing version-2 policy is a no-op.

## Provider preflight and inventory

The read-only inventory command performs version/surface preflight, reads the
authoritative user skill root twice, and emits only identities and digests:

```bash
context-guard inventory --provider claude --version 2.1.218 --surface cli
context-guard inventory --provider codex --version 0.144.1 --surface cli
```

Claude reads `~/.claude/skills/*/SKILL.md`; Codex reads
`~/.agents/skills/*/SKILL.md`. Supported MVP surfaces are Claude Code CLI and
Codex CLI/app-server at or above the pinned versions. Other versions or
surfaces return `unsupported`.

Each record contains provider, user scope, frontmatter name, canonical locator,
canonical metadata digest, body digest, and exact identity. Raw skill
instructions and descriptive metadata are never printed. Duplicate names,
missing/invalid frontmatter, read failures, or a changed second read return
`uncertain` with an empty usable inventory and no fingerprint.

## Modes

- `observe`: never blocks; the audit log records what *would* have happened (`would_have` field logic in `decisions.py`).
- `warn`: never blocks; a `block`-eligible decision is downgraded to a warning message.
- `enforce`: blocks per policy.

Per the PRFAQ rollout recommendation, start new installs in `observe`, move to `warn`, then `enforce` once false positives have been reviewed.

## Fail-open vs fail-closed

Cost/token-optimization rules (files, commands, search) fail open on any internal error by default — an evaluation failure never blocks a developer's work. `fail_closed_rules` lists rule ids that should block instead of allow on internal error; use this sparingly for genuinely security-adjacent rules, and remember Context Guard is not a security product (see `specs/001-context-guard/requirements.md`).

## Related: Compact Runtime

This page covers Stage 1 (blocking/warning on high-cost operations). For Stage 2 — executing an operation and returning a bounded compact result with drill-down evidence instead of raw output — see [Compact Runtime](compact-runtime.md).
