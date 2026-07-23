# Security Policy

Context Guard is a local context/cost-control tool, not a security product (see `specs/001-context-guard/requirements.md`). That said, we take reports of real vulnerabilities seriously — for example, anything that could cause the tool to execute untrusted input, leak secret values into the audit log, or bypass its own fail-safe behavior.

## Reporting a vulnerability

Please do **not** open a public GitHub issue for security reports. Instead, open a [GitHub Security Advisory](https://github.com/mikegorelikoff/ai-sdlc-context/security/advisories/new) for this repository, or contact the maintainer directly.

Include:

- A description of the issue and its potential impact.
- Steps to reproduce, including a minimal policy config and hook payload if relevant.
- The Context Guard version and Python version in use.

## Scope

In scope: the `context_guard` package (engine, adapters, policy loading, CLI, audit logging).

Out of scope: vulnerabilities in Claude Code or Codex themselves — report those to Anthropic or OpenAI respectively. Context Guard explicitly does not replace OS permissions, sandboxing, secret scanning, or endpoint protection.

## Response

We aim to acknowledge reports within a few business days and to disclose fixes once a patch is available.
