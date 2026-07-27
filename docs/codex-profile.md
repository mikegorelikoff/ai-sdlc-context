# Codex guarded profiles

Context Guard can generate a dedicated Codex configuration profile that
disables only exact user-authored skills classified as `irrelevant`. It never
edits `~/.codex/config.toml` and never launches Codex.

Current Codex user skills are inventoried from:

```text
~/.agents/skills/*/SKILL.md
```

The generated profile contains only sorted entries of this form:

```toml
[[skills.config]]
path = "/absolute/path/to/SKILL.md"
enabled = false
```

Required, safety-critical, uncertain, and explicitly invoked skills remain
enabled.

## Apply and select a profile

Pass an explicit home directory, profile name, stable inventory fingerprint,
classification for every skill, and its exact absolute path:

```bash
context-guard codex-profile apply \
  --home "$HOME" \
  --profile context-guard \
  --run-id task-123-apply \
  --version 0.144.1 \
  --inventory-fingerprint SHA256 \
  --classification unused-skill=irrelevant \
  --skill "unused-skill=$HOME/.agents/skills/unused-skill/SKILL.md"
```

The profile is written to
`~/.codex/context-guard.config.toml`. A verified result reports
`fresh_process_required: true`; select it for a new Codex process with:

```bash
codex --profile context-guard
```

Context Guard records a private persistent lease, exact baseline bytes, and
digests below `.context-guard/profiles/codex/`. Receipts and CLI results contain
neither skill paths nor TOML content.

## Restore, inspect, and recover

```bash
context-guard codex-profile status \
  --home "$HOME" --profile context-guard

context-guard codex-profile restore \
  --home "$HOME" --profile context-guard \
  --run-id task-123-restore --version 0.144.1
```

Restoration is byte-exact and compare-and-swap protected. If the generated
profile changed after application, Context Guard preserves the user edit,
disables further optimization for that profile, and returns a recovery action.

An abandoned lease can be recovered only after its owner process is dead and
the profile still matches the applied digest:

```bash
context-guard codex-profile recover \
  --home "$HOME" --profile context-guard \
  --run-id task-123-recover --version 0.144.1
```

Live owners, missing state, invalid state, and edited profiles are never
overwritten.
