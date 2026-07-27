# Status and limitations

Context Guard is currently package version `0.1.1`. Evaluate it against your
provider versions, hook surfaces, repositories, and data-handling requirements.

## Verified behavior

Repository tests cover policy loading, provider adapters, decisions, receipts,
profiles, measurement evidence, compact parsers, artifacts, CLI commands,
installation, examples, and latency checks. Bundled examples provide fixture
evidence.

## Known limitations

- The product loads one packaged policy; local policy overrides are not
  supported.
- The packaged policy remains in observe mode.
- Transparent command rewriting differs by provider hook capability.
- Compound, mutating, deployment, and unrecognized transparent-hook commands
  are left unchanged.
- Full artifacts can contain sensitive local output.
- Generic compaction cannot preserve every domain-specific semantic detail.
- Bytes and estimated tokens are not provider billing measurements.

## Claims not supported

Context Guard does not guarantee lower cost, fewer billed tokens, improved
model quality, complete interception, data-loss prevention, compliance, or
security certification.

Next, review [security and privacy](security-privacy.md).
