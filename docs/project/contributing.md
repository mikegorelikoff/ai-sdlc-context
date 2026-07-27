# Contributing

Use this page to make documentation or product changes without weakening
evidence and compatibility contracts.

1. Read the root [CONTRIBUTING.md](https://github.com/mikegorelikoff/ai-sdlc-context/blob/main/CONTRIBUTING.md)
   and `AGENTS.md`.
2. Keep runtime and documentation changes separate when practical.
3. Verify every published command against CLI help and tests.
4. Add focused tests for source and rendered documentation contracts.
5. Update the decision log and changelog for material documentation changes.

Validate documentation with:

```bash
python3 -m pip install -r requirements-docs.txt
python3 docs/scripts/validate_docs.py
python3 -m unittest discover -s docs/tests -v
mkdocs build --strict
git diff --check
```

Do not edit runtime behavior merely to make a documentation claim true.
