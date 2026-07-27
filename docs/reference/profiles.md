# Profile reference

Context Guard can build lease-safe, explicit skill profiles after inventory
and relevance classification.

## Claude profiles

Claude profiles write bounded `skillOverrides` for skills classified as
irrelevant and not explicitly invoked. Application records baseline bytes and
digests, verifies actual state, requires a fresh session when successful, and
supports restoration or recovery.

## Codex profiles

Codex profiles generate a dedicated explicit profile containing exact disabled
`SKILL.md` paths. Inventory names, paths, and fingerprints must correlate.
Application verifies the generated profile and requires a fresh process when
successful.

## Safety behavior

Unsupported provider versions, missing fingerprints, correlation mismatches,
lease contention, baseline conflicts, and failed verification return a
full-load or recovery result instead of silently applying an uncertain
profile. State lives beneath `.context-guard/profiles/`.

Inspect exact actions with:

```bash
context-guard claude-profile --help
context-guard codex-profile --help
```
