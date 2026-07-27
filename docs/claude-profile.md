# Claude guarded profiles

Context Guard can prepare a supported Claude Code settings profile before a fresh session. It does not launch Claude or make a model request.

Only skills classified as exact `irrelevant` are assigned:

```json
{
  "skillOverrides": {
    "unused-skill": "user-invocable-only"
  }
}
```

Required, safety-critical, uncertain, and explicitly invoked skills receive no reducing override. Existing overrides are never weakened or silently replaced.

## Apply a profile

Use an explicit settings path and a fingerprint from a stable Claude inventory:

```bash
context-guard claude-profile apply .claude/settings.local.json \
  --run-id task-123-apply \
  --version 2.1.218 \
  --inventory-fingerprint SHA256 \
  --classification unused-skill=irrelevant \
  --classification required-skill=required
```

A successful result reports `fresh_session_required: true`. Start a new Claude session only after that result. Unsupported versions, missing inventory evidence, bypass, contention, invalid settings, and verification mismatch use full load and receive no savings credit.

Application changes only requested `skillOverrides` entries. Before mutation, Context Guard stores the exact baseline and digest beneath `.context-guard/profiles/claude/` with owner-only permissions. Raw settings never enter decision receipts or normal CLI output.

## Restore and inspect

```bash
context-guard claude-profile status .claude/settings.local.json

context-guard claude-profile restore .claude/settings.local.json \
  --run-id task-123-restore \
  --version 2.1.218
```

Restoration uses compare-and-swap. If the applied settings are unchanged, the exact original bytes—or original file absence—are restored. Repeating restore is safe when a new attempt run ID is used.

If settings changed after application, Context Guard refuses to overwrite them, disables optimization for that profile, preserves recovery evidence, and returns one recovery action.

## Abandoned lease recovery

```bash
context-guard claude-profile recover .claude/settings.local.json \
  --run-id task-123-recover \
  --version 2.1.218
```

Recovery proceeds only when the recorded owner process is no longer alive and the settings digest still matches the applied state. Live owners, edits, missing state, or invalid state remain full-load and are not overwritten.
