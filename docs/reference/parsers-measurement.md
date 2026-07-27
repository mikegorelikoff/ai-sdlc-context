# Parser and measurement contracts

This advanced reference summarizes the evidence boundaries behind compact
tests and provider comparisons.

## Compact parsers

Pytest compacting prefers native JUnit XML when available, falls back to
recognized pytest text, and then uses a generic bounded parser. Failure-first
output retains exact fragments and the complete artifact. Parser notes identify
approximation or missing structured cases.

## Provider measurement

Claude and Codex measurement ledgers are separate and use provider-specific
schemas. Evidence is accepted only when required identities, receipts,
fingerprints, roles, order, and quality conditions correlate.

## Evidence levels

- Fixture evidence: deterministic expected behavior for a known input.
- Single-pair evidence: one baseline and guarded comparison.
- Repeated evidence: multiple valid, preferably counterbalanced pairs.

Output bytes and `bytes / 4` estimates are local measures. They are not
provider token counts, billing reduction, cost prevention, or model-quality
proof.

Use [the advanced measurement guide](../guides/measurement.md) for a procedure.
