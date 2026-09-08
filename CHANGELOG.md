# Changelog

## v0.1.4 - 2026-09-08

### Changed

- Restore hidden contributor-skill regressions to the normal test command, replace removed `_shared` test routes with the owning runtime, and use isolated installation/layout fixtures. Remove obsolete mirror-sync instructions and suggested commands.

- Add explicit deterministic/semantic boundaries to all 44 skills, linked to their existing Python entry points.
- Preserve punctuation and control characters in state/TOON, reject ambiguous keys and malformed state, make unchanged atomic writes no-ops, and bound repeated assumptions.
- Add fixed-date state inputs and hash-seed, working-directory, round-trip and failure-atomicity regressions.

## v0.1.3 - 2026-09-08

### Changed

- Bound test discovery to source test directories so a documentation build cannot
  cause duplicate collection from generated `site/` copies.

- Give all 44 Context Guard skills individual table-first chat contracts, domain-specific
  result/failure/clarification tables, compact evidence and owned next actions.
  Keep native artifacts and lifecycle authority unchanged.
- Add bounded deterministic chat rendering and structural evaluation, eight
  captured simulation scenarios per skill, negative tests and semantic review.
  Simulations are explicitly distinguished from live model evaluations.


## 0.1.2 - 2026-07-28

### Fixed

- Updated Codex hook installation to emit nested TOML array tables, preserve
  unrelated hooks, and migrate the flat format emitted by version 0.1.1.
- Made `install.sh` install missing Python and `venv` system dependencies
  through supported macOS and Linux package managers.

### Documentation

- Redesigned the README around an observe-first, locally reviewable start.
- Added a six-section GitHub Pages information architecture.
- Added plain-language Stage 1 and Stage 2 explanations and safe rollout.
- Added task guides, exact reference catalogs, privacy boundaries, and
  advanced measurement evidence guidance.
- Aligned the visual system with AI SDLC Harness and AI SDLC Metrics.
- Added documentation governance, contract tests, pinned dependencies, and a
  validated Pages workflow.
- Made the one-line installer the primary onboarding action while retaining a
  review-first local-clone alternative.
