# Repository instructions

Keep existing engineering rules in `CONTRIBUTING.md`, the product tests, and
the repository specifications.

## Documentation contract

- Product name: **Context Guard**.
- Ecosystem wording: **AI SDLC product family** and “Structure delivery.
  Control context. Measure adoption.”
- Public top-level navigation must remain, in order: Home; Start here; How it
  works; Guides; Reference; Project.
- README order is product name, outcome, badges, description, Why use it?,
  Quick start, expected result, workflow, scope, documentation paths, product
  family, security/privacy, status, contributing, license.
- Keep the primary install action in README, Home, and Start here to one shell
  command; put validation and self-test commands in a separate step.
- Use the guide template: Goal; When to use it; Prerequisites; Procedure;
  Verify; Troubleshooting; Next step.
- Start here is canonical for install and first run; How it works for Stage 1,
  Stage 2, and rollout; Reference for exact contracts; Project for status and
  trust.
- Do not duplicate canonical explanations. Link to them.
- Preserve the product-family block and
  `docs/assets/stylesheets/ai-sdlc.css`.
- Verify commands against source, CLI help, tests, or fixtures.
- Keep generated evidence and runtime contracts generated; do not hand-edit
  output to support a claim.
- Preserve public paths. Record moves and stubs in
  `docs/project/decision-log.md`.
- Update the decision log and `CHANGELOG.md` for material documentation
  changes.

## Build and validate

```bash
python3 -m pip install -r requirements-docs.txt
python3 docs/scripts/validate_docs.py
python3 -m unittest discover -s docs/tests -v
mkdocs build --strict
python3 docs/scripts/validate_rendered.py site
python3 tests/run_pytest.py -q
git diff --check
```
