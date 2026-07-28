# Security and privacy

This page helps security and privacy reviewers locate data, configuration, and
trust boundaries.

## Local evidence

Policy audit records, compact artifacts, receipts, profiles, quality evidence,
and measurements remain under the current repository's `.context-guard/`
directory. Audit commands and paths are hashed by default. Full compact
artifacts retain captured stdout and stderr and may include secrets or
restricted data.

## External behavior

Context Guard does not upload those records. The installer downloads from the
configured package source, and wrapped commands may access networks. Claude
Code, Codex, GitHub, pip, model providers, and executed tools retain their own
data behavior.

## Configuration and authority

Installation changes provider hook configuration and user-level executable
paths. If Python or `venv` is missing, it can invoke Homebrew or a supported
Linux package manager and may request `sudo`. Review the installer and keep
configuration backups. Policy changes, warn or enforce rollout, retention,
sharing, and deletion require a human owner.

## Reporting

Use the repository's
[private security reporting path](https://github.com/mikegorelikoff/ai-sdlc-context/security/policy).
Do not attach raw `.context-guard/` evidence to a public issue without
reviewing and redacting it.
