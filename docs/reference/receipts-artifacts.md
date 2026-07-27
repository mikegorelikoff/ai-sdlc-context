# Receipts and artifacts

This page distinguishes metadata receipts from full compact-output artifacts.

## Receipts

Receipts use schema `context-guard-receipt/v1` and live under
`.context-guard/receipts/`. Required fields include run identity, timestamp,
provider, provider version, surface, status, and completion/reference flags.
Receipt writes validate exact fields, use private directories, do not overwrite
an existing run ID, and use a nonblocking single-writer lock.

The default prune retention is 30 days. Use:

```bash
context-guard receipt inspect <run-id>
context-guard receipt prune --days 30
context-guard receipt delete <run-id>
```

## Artifacts

Compact artifacts live under `.context-guard/artifacts/<kind>/<artifact-id>/`.
They may contain stdout, stderr, metadata, native test reports, and a fragment
index. Retrieve them with:

```bash
context-guard artifact show <artifact-id>
context-guard artifact show <artifact-id> --fragment <fragment-id>
```

Artifacts retain full evidence and may contain sensitive content. Receipts are
correlation metadata; they are not a substitute for the artifact.
