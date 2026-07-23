## Summary

<!-- What does this PR change and why? -->

## Related spec / issue

<!-- e.g. specs/001-context-guard, Fixes #123 -->

## Test plan

- [ ] `python3 -m pytest tests/ -q` passes
- [ ] `python3 -m pytest tests/ -m perf -q` passes (if latency-sensitive code changed)
- [ ] `context-guard validate` and `context-guard test` pass locally
- [ ] Updated `docs/policy.md` / `README.md` if the policy schema or CLI surface changed
- [ ] Updated `specs/001-context-guard/` artifacts if requirements, design, or acceptance criteria changed

## Checklist

- [ ] Provider-specific parsing stays isolated to `context_guard/adapters/`
- [ ] No network calls or new external services introduced
- [ ] No secrets, full file contents, or full command output added to the audit log by default
