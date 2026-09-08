# Documentation decision log

Execution date: 2026-07-27

## Previous model

The repository had one long README, no public docs tree, no MkDocs
configuration, and a Pages workflow that referenced an undefined `docs`
optional dependency.

## Selected architecture

The site now uses Home, Start here, How it works, Guides, Reference, and
Project. Observe-mode first run is the recommended path. Stage 1 and Stage 2
are explained before policy internals.

## Alternatives considered

- Keep README as the only guide: rejected because onboarding, CLI, policy,
  measurement, privacy, and history competed on one page.
- Make measurement a primary section: rejected because it is an advanced
  evidence method, not the normal usage path.
- Add a runtime `sessions` command to match the old README: rejected because
  runtime changes are outside this documentation task.

## Product-specific decisions

- The one-line remote installer is primary; a local source checkout remains
  the review-first alternative, and both paths carry explicit trust guidance.
- The fixed packaged observe policy is documented rather than implying local
  mode overrides.
- Claude and Codex measurement material is hidden from primary navigation but
  built, searchable, and linked from Guides and Reference.
- No existing public page moved; README was rewritten in place.

## Reference influences

Spec Kit informed the short stage sequence; OpenSpec informed example-first
progressive disclosure; BMAD Method informed task, explanation, reference, and
next-step separation. No text, commands, branding, or assets were copied.

## Validation

Exact evidence is recorded in the workspace
`.docs-unification/validation-report.md`.

## One-line installation

On 2026-07-28, the existing remote `install.sh` pipeline became the primary
install action in README, Home, and Start here. It remains one state-changing
command followed by separate validation, self-test, and report commands. The
documentation retains the local-clone alternative and states that the shorter
path follows `main`, downloads through GitHub and pip, and changes user-level
provider configuration.

## Dependency bootstrap

On 2026-07-28, the installer began detecting and installing missing Python
3.10+ and `venv` dependencies through Homebrew or a supported Linux package
manager. Automatic bootstrap was selected over a hard failure to make the
one-line installation complete on fresh systems. Documentation now makes the
possible package-manager and `sudo` changes explicit; Bash and curl remain
bootstrap prerequisites for the remote pipeline itself.

## 2026-09-08 — Per-skill chat presentation contracts

Each of the 44 Context Guard skills owns its semantic table columns and failure
format. The shared helper handles bounded rendering and structural checks only;
it cannot grant approval, advance lifecycle state or replace native artifacts.
Evidence remains attached to results, and large previews retain exact totals and
the full artifact reference.

The contract registry (`evals/chat/registry.md`) records each design and its eight
executed simulation scenarios. Baselines are authored simulations, not recorded
provider runs; semantic review by the implementing assistant is recorded separately.
Normal product tests execute output regression checks.

## 2026-09-08 — Deterministic execution reinforcement

- Add explicit deterministic/semantic boundaries to all 44 skills, linked to their existing Python entry points.
- Preserve punctuation and control characters in state/TOON, reject ambiguous keys and malformed state, make unchanged atomic writes no-ops, and bound repeated assumptions.
- Add fixed-date state inputs and hash-seed, working-directory, round-trip and failure-atomicity regressions.

The canonical execution boundary and product-specific reproducibility limits are documented in [Reference](../reference/determinism.md). Native formats and release authority remain unchanged. Structural tests do not claim semantic correctness or live model evaluation.

- Restore hidden contributor-skill regressions to the normal test command, replace removed `_shared` test routes with the owning runtime, and use isolated installation/layout fixtures. Remove obsolete mirror-sync instructions and suggested commands.

## 2026-09-08 — Release 0.1.4

Publish the user-authorized determinism reinforcement from feature 026. Keep native artifact formats and existing approval boundaries. Structural and fixture-based tests do not establish live model reliability. Roll back by pinning 0.1.3; do not rewrite published tags.
