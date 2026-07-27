# Decision receipts

Context Guard stores decision receipts locally so a classification and fallback can be audited without retaining prompts, responses, source code, credentials, environment values, or full skill bodies.

## Storage and privacy

Receipts use the versioned schema `context-guard-receipt/v1` and live under:

```text
.context-guard/receipts/
├── records/
└── quarantine/
```

Application directories are restricted to mode `0700` and files to `0600` on platforms that support POSIX permissions. Writes are validated before persistence, serialized to a same-directory temporary file, flushed and synchronized, then atomically installed. An existing run ID is never overwritten.

The schema accepts only documented replay evidence: provider and version, timestamps, fingerprints and identity digests, reason codes and classifications, requested and actual actions, fallback reason, quality or measurement references, and restoration status. Unknown fields are rejected.

Receipt data is not synchronized remotely.

## Inspect and delete

```bash
context-guard receipt inspect RUN_ID
context-guard receipt delete RUN_ID
```

Run IDs permit only letters, numbers, dots, underscores, and hyphens. Inspection validates the complete record. Invalid JSON or schema is moved into private quarantine and is never returned as usable evidence. Deletion targets only the exact validated run ID.

## Retention

```bash
context-guard receipt prune
context-guard receipt prune --days 45
```

The default retention period is 30 days. Pruning removes only receipts that are all of the following:

- older than the retention cutoff;
- marked completed;
- not marked referenced.

Active, referenced, and recent receipts remain. Corrupt records are quarantined with their original bytes preserved. All mutations use a non-blocking single-writer lock; lock contention fails without a partial change.
