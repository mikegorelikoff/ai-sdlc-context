---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "design.md"
  path: "specs/003-context-guard-product-goal/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs/003-context-guard-product-goal/decision-log.md"
  status: "active"
  owner: "Engineering"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids: []
  related_artifacts:
    - "specs/003-context-guard-product-goal/branch-plan.md"
    - "specs/003-context-guard-product-goal/change-impact.md"
    - "specs/003-context-guard-product-goal/decision-log.md"
    - "specs/003-context-guard-product-goal/plan.md"
    - "specs/003-context-guard-product-goal/qa.md"
    - "specs/003-context-guard-product-goal/requirements.md"
    - "specs/003-context-guard-product-goal/tasks.md"
    - "specs/003-context-guard-product-goal/test-cases.md"
    - "specs/003-context-guard-product-goal/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "active"
    - "slice-5"
    - "slice-4"
    - "slice-3"
    - "slice-1"
---

# Design

## Overview
Extend context_guard.policy_config with backward-compatible v2 relevance, provide authoritative minimized inventory in context_guard.inventory, privacy-safe local decision evidence in context_guard.receipts, a bounded Claude Code guarded-profile adapter in context_guard.claude_profile, and provider-neutral frozen-fixture hard gates in context_guard.quality. Policy, inventory, receipt, and quality evaluation make no model or network call; Claude mutation occurs only through an explicit settings path and never launches a provider session. Token measurement remains outside this slice and is denied until quality authorization passes.

Slice 4 adds deterministic read-only Claude usage extraction and provider-specific qualification. It consumes explicit local JSONL evidence only after quality authorization, computes native cache tokens without cost inference, and makes no model or network call.

Slice 5 aligns Codex inventory with current official skill discovery, adds reversible generated profile control for supported CLI/app-server startup, and adds provider-specific cached-input measurement. It uses explicit paths/evidence and never launches Codex.

## Architecture
Policy layers parse independently and exact relevance is conservative. Inventory gates provider/version/surface before canonical double-read evidence. Receipts validate an exact allowlist before private atomic persistence. The Claude adapter derives only exact irrelevant overrides, acquires a per-profile persistent lease, snapshots exact baseline bytes/digest, atomically mutates and verifies only skillOverrides, and requires a fresh session. Restore and dead-owner recovery use applied-digest compare-and-swap; edits create a disabled marker and are never overwritten. The quality boundary accepts only versioned sanitized manifests and attempt evidence, evaluates QG-301–QG-309, appends immutable outcomes under one writer lock, writes privacy-safe receipts, and authorizes measurement only for exactly one valid non-invalidated pair.

After quality authorization, the measurement boundary parses one declared Claude session file, filters and deduplicates eligible assistant usage events, persists minimized run evidence, correlates baseline/guarded pairs, and aggregates exactly fifteen pairs. Authorization is rechecked at pair and qualification time so later QA invalidation fails closed.

The Codex control boundary consumes stable HOME/.agents/skills inventory, writes a dedicated explicit HOME/.codex profile under a persistent lease, verifies only generated skills.config entries, and returns a profile selector for a fresh process/thread. CAS restore/recovery mirrors Claude safety. The measurement boundary accepts either one exact turn.completed JSONL event or declared monotonic cumulative boundaries, then uses the shared quality-first paired protocol without pooling providers.

## Components
`policy_config.py` owns policy v2. `context_guard/inventory.py` owns capability tables, semantic-version checks, authoritative provider roots, strict SKILL.md frontmatter parsing, minimized records, double-read stability, duplicate detection, and canonical fingerprints. New `context_guard/receipts.py` owns the versioned allowlist schema, safe run identifiers, private storage layout, atomic persistence, writer locking, inspection, exact deletion, retention pruning, and corruption quarantine. `cli.py` exposes read-only inventory plus explicit receipt inspect, delete, and prune operations. New context_guard/claude_profile.py owns guarded override planning, persistent profile leases, private baseline state, atomic JSON mutation, actual-state verification, receipt emission, compare-and-swap restoration, disabled-profile markers, and dead-owner recovery. cli.py exposes explicit claude-profile apply, restore, recover, and status controls without launching a paid provider session. New context_guard/quality.py owns manifest/attempt validation, the fixed QG-301–QG-309 evaluator, three-fixture suite validation, private append-only outcome ledger, QA invalidation, measurement authorization, and quality receipts. cli.py exposes quality evaluate, authorize, invalidate, and validate-suite without executing provider commands or exposing token data.

New context_guard/claude_measurement.py owns strict Claude JSONL usage extraction, identical-row deduplication, run evidence, baseline/guarded pair comparison, exact-fraction aggregation, qualification gates, private append-only measurement records, and measurement receipts. cli.py exposes explicit extract, pair, and qualify commands; it never discovers files or starts Claude.

context_guard/inventory.py updates the Codex authoritative user root. New context_guard/codex_profile.py owns exact irrelevant planning, canonical TOML generation, private state/lease, atomic verification, selector output, CAS restoration, disabled markers, recovery, and receipts. New context_guard/codex_measurement.py owns exact-event/cumulative extraction, sanitized evidence, pair/statistical qualification, private ledger, and receipts. cli.py exposes explicit Codex controls without provider execution.

## Interfaces and Contracts
CLI `inventory --provider claude|codex --version VERSION --surface SURFACE [--home PATH]` prints one JSON result and never mutates provider state. Unsupported or uncertain results have an empty records list and null fingerprint. Supported roots are `HOME/.claude/skills` and `HOME/.agents/skills`; stale `HOME/.codex/skills` content is ignored. Receipt APIs use `<repo>/.context-guard/receipts/{records,quarantine}`. `write_receipt(root, payload)` validates and atomically creates one `<run_id>.json`; `inspect_receipt`, `delete_receipt`, and `prune_receipts` accept the same root. CLI `receipt inspect RUN_ID`, `receipt delete RUN_ID`, and `receipt prune [--days 30]` print sanitized JSON results. ClaudeProfileResult reports guarded, full-load, restored, or recovery-required status plus a stable reason and fresh_session_required flag. apply_profile accepts a caller-supplied settings path, exact classifications, explicit invocations, version, surface, and run id; it never searches or mutates another profile. restore_profile and recover_profile operate only on the matching stored lease/state. CLI controls require an explicit settings path, making mutations visible and testable. QualityManifest and AttemptEvidence parse exact JSON allowlists. evaluate_pair(manifest, baseline, guarded) returns PairEvaluation with nine ordered GateResults and measurement_allowed. QualityLedger append/evaluate/invalidate/authorize stores only sanitized hashes, gate IDs, reasons, and references under .context-guard/quality. CLI accepts explicit JSON evidence paths and prints minimized evaluation results.

Claude extraction accepts an explicit JSONL Path plus run_id, quality_pair_id, fixture_kind, role, declared session_id, provider_version, and model. It returns a minimized ClaudeRunMeasurement with measurable status or stable reason. Pair evaluation consumes two stored or supplied run measurements and current QualityLedger authorization. Qualification consumes exactly fifteen distinct valid pair records, five for each frozen fixture kind, and returns exact rational statistics plus a bounded pass/fail decision.

Codex profile APIs accept repo root, HOME root, explicit profile name, run/version/surface, exact classifications, exact absolute skill paths, explicit invocations, and stable inventory fingerprint. Verified application writes only `HOME/.codex/<profile>.config.toml`, returns the `--profile <profile>` selector and `fresh_process_required`, and never edits the main config. Exact measurement accepts one explicit JSONL path plus a declared thread; cumulative measurement accepts explicit start/end boundary identifiers and values. Pair and qualification contracts mirror Claude exact-fraction semantics but remain Codex-specific.

## Data Model
PreflightResult has provider/version/surface/status/reason. SkillRecord has provider/scope/name/locator/metadata_digest/body_digest/identity. InventoryResult has status/reason/provider/version/surface/records/fingerprint. Inventory output never contains SKILL.md body or frontmatter values beyond the authoritative name. Receipt schema `context-guard-receipt/v1` requires run_id, timestamp, provider, provider_version, surface, status, completed, and referenced. It permits only documented replay fields such as fingerprints, identity digests, reason codes, classifications, requested/actual action, fallback reason, quality/measurement references, and restoration status; values are scalars or lists of strings, never arbitrary nested content. Claude profile state stores schema, run id, owner pid, canonical settings path, baseline existence/digest/base64 bytes, and applied digest beneath .context-guard/profiles/claude/<profile-hash>. Lease, state, and disabled marker files use private modes. Stored baseline bytes are operational recovery state and are never copied into receipts or CLI output. Manifest schema context-guard-quality-manifest/v1 stores fixture id/kind and declared fingerprints plus required instruction IDs. Attempt schema context-guard-quality-attempt/v1 stores attempt/pair/role identifiers, matching fingerprints, booleans for fresh session/completion/explicit skill/restoration/receipt/privacy, observed instruction IDs, and receipt ref. Ledger schema context-guard-quality-ledger/v1 stores evaluation or invalidation events, timestamps, pair/fixture refs, gate outcomes/reasons, evidence digests, and authorization only.

Claude run evidence records schema, identifiers, declared version/model/session, source SHA-256, eligible and duplicate row counts, integer cache-creation/cache-read/combined totals, quality reference, status, and reasons. The deduplication key is sessionId/requestId/message.id and duplicate usage tuples must match exactly. Pair evidence stores baseline/guarded refs and totals plus a signed rational reduction numerator/denominator. Qualification stores ordered pair refs, per-fixture median fractions, provider median, nearest-rank Q1, gate outcomes, and decision.

Codex profile state stores exact baseline existence/bytes/digest, applied digest, owner, and canonical profile path privately. Generated TOML contains only sorted [[skills.config]] path/enabled entries. Codex run evidence stores mode, identifiers, version/model/thread/turn, source digest or boundary digests, native cached-input total, quality ref, status, and reason. Pair and qualification evidence uses exact numerator/denominator statistics and provider-separated refs.

## Error Handling
Policy errors retain stable `POLICY_*` codes and dotted paths. Receipt failures expose stable categories for schema validation, invalid run id, existing receipt, writer contention, missing record, and corrupt record. Validation occurs before persistence. A corrupt record is never returned; the mutating recovery path moves its original bytes to quarantine under the writer lock. Failed temporary writes are cleaned without changing an existing record. Invalid settings, unsupported input, live contention, disabled profiles, verification mismatch, receipt failure, and CAS mismatch return conservative full-load or recovery-required results with stable reason codes. A failed application restores when CAS-safe. Recovery never overwrites an edited file. Unknown fields or malformed evidence raise stable QUALITY_INVALID errors before ledger persistence. Gate failures are expected invalid results, not exceptions. Ledger corruption or ambiguous duplicate evaluation state denies authorization with a stable reason. Append and receipt failures never report authorization.

Malformed JSON, unsupported version, wrong row type/session/model, missing identifiers or counters, negative or non-integer counters, inconsistent duplicates, empty eligible windows, unauthorized quality, correlation mismatch, zero baseline, duplicate pair IDs, incomplete fixture populations, corrupt ledger state, and receipt failures produce stable unmeasurable or denied outcomes. Missing data is never converted to zero. Persistence or receipt failure cannot authorize a pair or qualification.

Stale HOME/.codex/skills inventory, unsupported surface/version, invalid profile location, live lease, parse/verification mismatch, user edit, ambiguous recovery, missing/multiple exact completion events, malformed counters, non-monotonic cumulative totals, missing boundaries, quality mismatch/invalidation, zero baseline, mixed populations, receipt failure, or corrupt ledger fail closed with stable reasons and no zero substitution.

## Security Considerations
Exact string comparison prevents fuzzy omission. Required wins conflict. Unknown and malformed states fail toward complete content. Receipt allowlisting rejects arbitrary keys by construction, so prompts, responses, source, credentials, secrets, environment values, and skill bodies have no serializable field. Receipt paths derive only from validated run ids. Application directories and files are tightened to 0700/0600 where supported, mutations are single-writer, and no receipt is synchronized remotely. Claude mutation is bounded to an explicit resolved settings path and changes only skillOverrides. Private recovery state may contain exact baseline settings and therefore uses owner-only permissions and never enters logs or receipts. CAS restoration, live-owner checks, and disabled markers prevent destructive overwrite after concurrent or user changes. Quality inputs and ledger records use exact allowlists and contain no executable commands, raw task text, source, prompt/response, credentials, environment values, or token values. The runner never executes evidence. Private 0700/0600 storage, a non-blocking writer lock, fsync, and append-only records protect local evidence.

The adapter reads only the caller-supplied file and never emits or persists its path or raw lines. Exact schemas reject prompt, response, content, source, path, credentials, environment values, and billed-cost fields. Stored files remain local with 0700 directories, 0600 files, non-blocking writer locking, fsync, and append-only evidence. Source content is represented only by SHA-256.

Only caller-declared files and scalar boundaries are read. Profile mutation is restricted to an explicit resolved path beneath HOME/.codex and generated allowlisted TOML. Private snapshots may contain exact prior profile bytes and remain 0700/0600 state; they never enter receipts. Logs, paths, prompts, responses, source, auth, environment values, and billed cost are prohibited from normal evidence.

## Observability
Policy sources expose effective layer names; relevance results expose rule and reason without instruction content; inventories expose eligibility, minimized identities/digests, and a fingerprint; receipt operations expose only allowlisted replay evidence and stable result/error categories. No raw prompt, response, source, environment value, or skill body is emitted.

## Risks and Tradeoffs
The highest risk is accidental omission, addressed by exact matching, required precedence, unsupported/uncertain safe failure, and no live provider mutation in this increment. Receipt risks are sensitive-data leakage, partial writes, path escape, concurrent mutation, and corrupt evidence; exact schema allowlisting, validated run IDs, atomic persistence, private modes, locking, and quarantine bound those risks.

## Validation Strategy
Run focused policy, inventory, receipt, Claude-profile, quality-evaluator, and CLI tests, followed by the full repository suite and git diff --check through the canonical validation plan. Quality tests cover the exact suite, every QG failure, immutable mismatch evidence, prohibited fields, valid retry coexistence, append-only invalidation, missing/corrupt/ambiguous denial, receipt failure, private modes, contention, CLI behavior, and content privacy. Strict MkDocs and full-flow refinement-context, clarify, checklist, plan-link, analyze, and spec-validation gates provide supplemental evidence. No production profile, live provider session, or token measurement is touched.

Add synthetic Claude JSONL contract fixtures covering identical duplicates, inconsistent duplicates, drift, missing fields, malformed counters, correlation, authorization, zero baselines, signed reductions, exact median and nearest-rank Q1, five-by-three qualification, negative retention, receipt failure, private modes, forbidden content, and CLI behavior. Run focused tests, the full suite, strict docs, diff hygiene, and all full-flow SDD gates. Live provider execution and the 30 percent observation remain outside deterministic validation.

Add inventory migration tests, deterministic Codex profile apply/restore/recovery fault injection, TOML/path privacy tests, exact turn.completed and cumulative boundary fixtures, ambiguity/reset negatives, quality correlation/invalidation, signed reductions, five-by-three exact statistics, receipt/ledger failures, CLI contracts, strict docs, full regression, and all SDD gates. No paid provider process is started.

## Migration Notes
Version 2 creation and migration are additive. `init` serializes v2 with empty `skills.rules`. `migrate-policy` validates a repository v1 file, refuses to overwrite its `.v1.bak`, writes and fsyncs a same-directory temporary v2 file, validates it, then uses atomic replace. Existing v2 is unchanged.
