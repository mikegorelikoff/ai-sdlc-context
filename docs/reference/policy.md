# Packaged policy reference

Context Guard `0.1.1` loads exactly one version 2 policy from
`context_guard/defaults/policy.yaml`. Repository files, user files, and
environment variables do not override it.

```yaml
version: 2
mode: observe

files:
  max_full_read_bytes: 200000
  require_range_above_bytes: 50000
  deny:
    - "**/node_modules/**"
    - "**/vendor/**"
    - "**/dist/**"
    - "**/build/**"
    - "**/coverage/**"
    - "**/.git/**"
    - "**/*.min.js"
    - "**/*.map"
    - "**/package-lock.json"
    - "**/yarn.lock"
    - "**/pnpm-lock.yaml"
    - "**/Cargo.lock"

commands:
  maximum_expected_output_lines: 500
  require_bounds:
    - "docker logs"
    - "docker compose logs"
    - "kubectl logs"
    - "git log"

search:
  require_path_scope: true
  maximum_results: 100

fail_closed_rules: []

skills:
  rules: []
```

Valid modes are `observe`, `warn`, and `enforce`. File, command, and search
groups may carry an effective mode in the runtime data model, but the shipped
policy above is the only accepted source. Unknown fields, invalid types,
unsupported versions, and invalid enum values fail validation.

Policy behavior is defined by `context_guard/policy_config.py` and the policy
modules under `context_guard/policies/`.
