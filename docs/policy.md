# Context Guard Policy Reference

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

## Modes

- `observe`: never blocks; the audit log records what *would* have happened (`would_have` field logic in `decisions.py`).
- `warn`: never blocks; a `block`-eligible decision is downgraded to a warning message.
- `enforce`: blocks per policy.

Per the PRFAQ rollout recommendation, start new installs in `observe`, move to `warn`, then `enforce` once false positives have been reviewed.

## Fail-open vs fail-closed

Cost/token-optimization rules (files, commands, search) fail open on any internal error by default — an evaluation failure never blocks a developer's work. `fail_closed_rules` lists rule ids that should block instead of allow on internal error; use this sparingly for genuinely security-adjacent rules, and remember Context Guard is not a security product (see `specs/001-context-guard/requirements.md`).
