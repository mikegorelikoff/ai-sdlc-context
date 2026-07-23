# Contributing to Context Guard

Thanks for your interest in contributing. Context Guard is a small, deterministic local tool — contributions that keep it simple, dependency-light, and provider-agnostic are especially welcome.

## Getting started

```bash
git clone https://github.com/mikegorelikoff/ai-sdlc-context.git
cd ai-sdlc-context
python3 -m pip install -e .
python3 -m pytest tests/ -q
```

Python 3.10+ is required.

## Project structure

See `specs/001-context-guard/design.md` for the architecture and `docs/policy.md` for the policy schema. Requirements, design, test cases, QA plan, and tasks for the current feature set live under `specs/001-context-guard/`.

## Making a change

1. Open an issue describing the bug or proposal before large changes, so scope can be agreed on first.
2. Keep provider-specific parsing isolated to `context_guard/adapters/`; the engine and policy modules must stay provider-agnostic.
3. Add or update tests under `tests/` for any behavior change. Run `python3 -m pytest tests/ -q` (and `-m perf` for the latency benchmark) before opening a PR.
4. Update `docs/policy.md` and `README.md` when you change the policy schema or CLI surface.
5. Keep commits focused; explain the *why* in the commit message and PR description.

## Reporting bugs / requesting features

Use the issue templates under `.github/ISSUE_TEMPLATE/`. Security-sensitive reports should follow `SECURITY.md` instead of a public issue.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
