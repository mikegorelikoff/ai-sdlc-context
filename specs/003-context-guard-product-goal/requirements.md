---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "requirements.md"
  path: "specs/003-context-guard-product-goal/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs/003-context-guard-product-goal/decision-log.md"
  status: "draft"
  owner: "Engineering and QA"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "AC-009"
    - "AC-010"
    - "AC-011"
    - "AC-012"
    - "AC-013"
    - "AC-014"
    - "AC-015"
    - "AC-016"
    - "AC-017"
    - "AC-018"
    - "AC-019"
    - "AC-020"
    - "AC-021"
    - "AC-022"
    - "AC-023"
    - "AC-024"
    - "AC-025"
    - "AC-026"
    - "AC-027"
    - "AC-028"
    - "AC-029"
    - "AC-030"
    - "AC-031"
    - "AC-032"
    - "AC-033"
    - "AC-034"
    - "AC-035"
    - "AC-036"
    - "AC-037"
    - "AC-038"
    - "AC-039"
    - "AC-040"
    - "AC-041"
    - "AC-042"
    - "AC-043"
    - "AC-044"
    - "AC-045"
    - "AC-046"
    - "AC-047"
    - "AC-048"
    - "AC-049"
    - "AC-050"
    - "AC-051"
    - "AC-052"
    - "AC-053"
    - "AC-054"
    - "AC-055"
    - "AC-056"
    - "AC-057"
    - "AC-058"
    - "AC-059"
    - "AC-060"
    - "AC-061"
    - "AC-062"
    - "AC-063"
    - "DEC-001"
    - "DEC-005"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
  related_artifacts:
    - "specs/003-context-guard-product-goal/branch-plan.md"
    - "specs/003-context-guard-product-goal/change-impact.md"
    - "specs/003-context-guard-product-goal/decision-log.md"
    - "specs/003-context-guard-product-goal/design.md"
    - "specs/003-context-guard-product-goal/plan.md"
    - "specs/003-context-guard-product-goal/qa.md"
    - "specs/003-context-guard-product-goal/tasks.md"
    - "specs/003-context-guard-product-goal/test-cases.md"
    - "specs/003-context-guard-product-goal/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "draft"
    - "slice-5"
    - "slice-4"
    - "slice-1"
---

# Requirements

## Goal
Implement deterministic policy and inventory controls, privacy-safe receipts, supported Claude and Codex guarded-profile verticals, hard quality gates, and reproducible provider-specific cache-token measurement while preserving existing Stage 1 behavior and user configuration.

## Problem Statement
The existing policy loader supports version 1 operational rules only and has no authoritative skill inventory or privacy-safe replay evidence. Context Guard needs explicit deterministic contracts for all three before provider visibility can be reduced safely.

## Scope
In scope: completed Slice 1–4 contracts plus Slice 5 Codex inventory alignment, explicit reversible profile control for supported CLI/app-server startup, exact or cumulative cached-input extraction, authorized pair comparison, five-by-three exact qualification, local evidence, and privacy-safe recovery. Live provider execution, performance qualification, and combined rollout remain later tasks.

## Actors
Repository maintainers author repo rules; developers consume effective policy and diagnostics; Engineering implements the contract; QA validates deterministic safe behavior.

## Inputs
Inputs include policy YAML; exact provider/version/surface; HOME/.claude/skills for Claude inventory; HOME/.agents/skills for current Codex user inventory; explicit Claude settings or Codex profile paths; explicit provider JSONL or cumulative boundaries; frozen fixture evidence; and current quality authorization.

## Outputs
Outputs include validated classification/inventory, governed receipts, verified Claude and Codex profile outcomes, quality authorization, provider-specific run totals and pair reductions, exact fixture/provider statistics, and bounded pass/fail qualification decisions. Unsupported, stale, uncertain, edited, corrupt, unauthorized, unmeasurable, or incomplete states earn no optimization credit.

## Functional Requirements
FR-001: accept versions 1/2 and reject future versions. FR-002: v2 `skills.rules` supports the accepted exact rule fields. FR-003: later layers replace same-ID rules as whole objects and duplicates fail. FR-004: disabled rules do not match. FR-005: precedence is safety-critical, required, irrelevant. FR-006: only exact identity/selectors match; unknown returns required. FR-007: v1 remains compatible. FR-008: doctor reports version/rule/conflict counts. FR-009: init writes v2 without overwriting. FR-010: migration validates, backs up, validates output, and atomically replaces. FR-011: provider preflight accepts only Claude Code >=2.1.218 CLI and Codex >=0.144.1 CLI/app-server; other versions/surfaces are unsupported without mutation. FR-012: supported inventory reads only provider-authoritative `~/.claude/skills/*/SKILL.md` or `~/.agents/skills/*/SKILL.md`. FR-013: each record contains provider, scope, frontmatter name, canonical locator, canonical metadata digest, body digest, and exact identity. FR-014: duplicate provider/scope/name, missing/invalid frontmatter name, read error, or changed double-read returns uncertain with no inventory credit. FR-015: inventory fingerprint is SHA-256 over canonical sorted record evidence and is stable across unchanged reads. FR-016: every decision attempt may be persisted only as a versioned receipt containing an exact allowlist of non-sensitive scalar or string-list evidence fields. FR-017: receipt validation rejects unknown fields, malformed identifiers, invalid timestamps, invalid statuses, and prohibited prompt, response, source, credential, secret, environment-value, or full-body fields before a file is created. FR-018: receipt directories use mode 0700 and files use mode 0600 where supported; writes use a same-directory temporary file, flush, fsync, validation, and atomic replace without overwriting an existing run. FR-019: all receipt mutations use a non-blocking single-writer lock and fail safely on contention. FR-020: inspection validates the receipt schema and quarantines corrupt records rather than returning them as usable evidence. FR-021: deletion accepts one validated run identifier and removes only its exact record. FR-022: pruning defaults to 30 days and removes only completed, unreferenced receipts older than the cutoff; active, referenced, recent, and corrupt records are retained or quarantined. FR-023: quarantine preserves corrupt bytes in a private directory and excludes them from inspection and pruning credit. FR-024: validated receipt fields are sufficient to replay the recorded classification, requested/actual action, fallback reason, and restoration status without storing provider content. FR-025: Claude guarded planning maps only exact irrelevant non-plugin skills to user-invocable-only; explicit invocation, required, safety-critical, uncertain, and absent classifications receive no reducing override. FR-026: Claude profile mutation is permitted only after supported Claude CLI preflight and stable inventory, and it requires a fresh session after verified application. FR-027: one non-blocking persistent lease per Claude settings profile records run ownership and process identity; live contention uses full load without mutation. FR-028: before mutation, the adapter atomically records the exact baseline bytes, existence state, and SHA-256 digest in private application storage. FR-029: profile application changes only the requested skillOverrides entries and preserves unrelated settings and baseline overrides. FR-030: the adapter atomically writes and rereads the settings file; requested/actual mismatch triggers full-load fallback and no savings credit. FR-031: normal restoration is idempotent and compare-and-swap guarded by the applied-state digest; a matching state restores exact baseline bytes or absence. FR-032: post-application user edits prevent automatic overwrite, disable further optimization for the profile, preserve evidence, and return one actionable recovery path. FR-033: an abandoned lease is recoverable only when owner liveness is false and compare-and-swap proves the applied state remains unchanged; otherwise user state is preserved and optimization remains disabled. FR-034: every apply, fallback, restore, and recovery attempt writes an allowlisted local decision receipt without raw settings content. FR-035: quality manifests use a versioned exact schema and collectively contain exactly the read-only analysis, isolated test-only change, and explicit AI-SDLC skill fixture kinds with immutable task, repository, provider, model, and profile fingerprints. FR-036: attempt evidence contains only identifiers, fingerprints, boolean oracle outcomes, required-instruction identifiers, receipt references, and restoration state; raw prompts, responses, source, credentials, environment values, and provider token values are rejected. FR-037: pair evaluation requires one baseline and one guarded attempt with the same pair/fixture/provider/version/model/repository/task inputs and the manifest-declared role-specific profile fingerprints. FR-038: QG-301 validates manifest/schema; QG-302 validates pair correlation and roles; QG-303 validates immutable fingerprints; QG-304 requires fresh sessions; QG-305 requires both completion oracles; QG-306 requires complete required-instruction identifiers; QG-307 requires explicit skill invocation for that fixture; QG-308 requires successful or not-required restoration; QG-309 requires schema-valid privacy-safe correlated receipts. FR-039: all QG-301 through QG-309 are hard gates with no bypass; any failure makes the pair invalid and denies measurement access. FR-040: every evaluation appends a private immutable sanitized ledger record containing gate outcomes and stable reasons; invalid attempts are retained and excluded rather than deleted. FR-041: QA invalidation appends a new reasoned record and immediately denies measurement without rewriting prior evidence. FR-042: later valid retries use new pair identifiers and never erase invalid attempts. FR-043: measurement authorization reads the ledger and returns allowed only for the latest non-invalidated valid pair record; missing evidence is denied, never treated as zero. FR-044: evaluation and invalidation write sanitized decision receipts linked by pair/quality references without raw fixture or output content.

FR-045: Claude measurement accepts only an explicit JSONL path, declared supported provider version/model/session/pair/fixture/role, and an already authorized quality pair; it never discovers logs automatically or launches Claude. FR-046: only assistant rows with matching declared session and exact message usage fields are eligible; token counters must be non-negative integers. FR-047: eligible rows are deduplicated by sessionId, requestId, and message.id; identical duplicates count once, while missing identifiers or inconsistent duplicate usage makes the run unmeasurable. FR-048: the Claude run total is the exact integer sum of cache_creation_input_tokens plus cache_read_input_tokens across deduplicated rows; absent, malformed, uncorrelated, or empty windows are unmeasurable and never become zero. FR-049: measurement evidence persists only run/pair/fixture/role identifiers, provider/version/model, source fingerprint, row counts, deduplication counts, cache creation/read totals, combined total, quality reference, status, and stable reasons; raw JSONL content and paths are prohibited. FR-050: one measurement pair requires matching fixture/provider/version/model and one baseline plus one guarded measurable run whose quality pair is authorized. FR-051: pair reduction is the signed unrounded fraction (baseline total minus guarded total) divided by baseline total; a zero baseline is unmeasurable and valid negative reductions remain retained. FR-052: a Claude qualification requires exactly five valid distinct pairs for each of the three frozen fixture kinds; roles alternate by declared order and no outlier is deleted. FR-053: aggregation reports exact per-pair fractions, per-fixture medians, provider median, and nearest-rank Q1 where rank is ceil(0.25*n) over sorted reductions. FR-054: Claude passes only when every referenced quality pair remains authorized, provider median is at least 0.30, nearest-rank Q1 is at least 0, and every fixture median is at least 0. FR-055: extraction, pair evaluation, and qualification write privacy-safe receipts and append-only measurement evidence; missing, corrupt, ambiguous, invalidated, or unauthorized evidence denies qualification.

FR-056: Codex guarded planning maps only exact irrelevant user-authored skills to absolute-path skills.config entries with enabled=false; explicit invocation, required, safety-critical, uncertain, system/admin/plugin skills, and absent classifications remain enabled.
FR-057: Codex profile mutation requires supported Codex CLI or app-server preflight, a stable HOME/.agents/skills inventory, and a fresh process/thread after verified application.
FR-058: the adapter accepts only an explicit profile path beneath HOME/.codex whose basename ends in .config.toml; it never edits the main config implicitly or searches for another profile.
FR-059: one persistent non-blocking lease per profile records ownership; before mutation the adapter stores exact baseline existence, bytes, and digest in private state.
FR-060: a generated Codex profile contains only canonical absolute-path [[skills.config]] entries and enabled=false, sorted deterministically, with no arbitrary TOML supplied by evidence.
FR-061: profile application atomically writes, parses, rereads, and verifies exact requested state before returning the profile selector and fresh-thread readiness; mismatch or unsupported input uses full load.
FR-062: restoration and dead-owner recovery are idempotent and applied-digest compare-and-swap guarded; user edits are preserved, optimization is disabled, and one recovery action is returned.
FR-063: apply, fallback, restore, and recovery write allowlisted receipts without config bytes, skill bodies, paths, prompts, or credentials.
FR-064: Codex measurement accepts either one explicit Codex exec JSONL path with a declared thread/turn correlation or explicit start/end cumulative cached-input boundaries; it never discovers logs or launches Codex.
FR-065: exact-event mode accepts one correlated turn.completed usage.cached_input_tokens non-negative integer; missing, multiple, drifted, or malformed completion events are unmeasurable.
FR-066: cumulative mode requires non-negative integer start/end values from the same declared provider/version/model/session boundary and computes end minus start only when monotonic; resets or ambiguity are unmeasurable.
FR-067: measurement requires current quality authorization matching Codex provider, version, model, and fixture before reading token data.
FR-068: Codex run evidence stores only identifiers, mode, source fingerprint where applicable, event/boundary counts, cached-input total, quality reference, status, and stable reasons; raw JSONL, paths, content, and billed cost are prohibited.
FR-069: a comparable Codex pair requires matching fixture/provider/version/model, one baseline and one guarded measurable run, distinct run IDs, and current quality authorization.
FR-070: pair reduction is the exact signed unrounded fraction over a non-zero baseline; negative and extreme valid results remain retained without outlier deletion.
FR-071: Codex qualification requires exactly five distinct alternating pairs for each frozen fixture kind and rejects incomplete, duplicate, mixed-context, corrupt, or unauthorized populations.
FR-072: aggregation reports exact per-pair fractions, per-fixture medians, provider median, and nearest-rank Q1 without pooling Claude and Codex.
FR-073: Codex passes only when provider median is at least 0.30, nearest-rank Q1 is at least zero, every fixture median is at least zero, and all current quality gates pass.
FR-074: profile and measurement evidence uses private append-only state, writer locking, fsync, sanitized receipts, and fail-closed behavior on persistence or receipt failure.
FR-075: existing stale Codex inventory evidence rooted at HOME/.codex/skills is unsupported for guarded credit and must be regenerated from the current HOME/.agents/skills contract.

## Non-Functional Requirements
NFR-001: classification is deterministic and local with no model/network call. NFR-002: diagnostics identify the dotted field and stable error code. NFR-003: existing policy tests remain green on Python 3.10+.

## Constraints
Do not infer semantic similarity, omit required/unknown content, infer billed cost, pool providers, delete outliers, discover logs automatically, or launch paid provider sessions. Mutations require explicit paths, supported preflight, stable inventory, exact irrelevant classifications, a lease, private baseline evidence, actual-state verification, fresh sessions, and CAS-safe restoration.

## Acceptance Criteria
AC-001: valid v2 layers produce deterministic rules. AC-002: same-id later layer replaces whole object. AC-003: disabled rule returns required default. AC-004: only exact unconflicted irrelevant reduces. AC-005: invalid schema reports stable code/path. AC-006: v1 behavior remains unchanged. AC-007: init writes non-overwriting valid v2. AC-008: valid v1 migration creates byte-identical backup and atomic valid v2. AC-009: v2/invalid/existing-backup migration is no-op or safe failure. AC-010: supported provider/version/surface preflight records eligibility; unsupported inputs return unsupported. AC-011: two unchanged inventory reads return identical ordered identities and metadata/body digests. AC-012: duplicate or missing identity/frontmatter returns uncertain and no usable records. AC-013: changed content between the required double read returns stale-inventory uncertainty. AC-014: inventory fingerprint is identical for unchanged content independent of directory enumeration order. AC-015: a valid receipt is atomically persisted with the versioned schema, required replay evidence, private directory permissions, and private file permissions. AC-016: unknown or prohibited receipt fields, malformed values, or an existing run id produce a stable validation failure and leave existing records unchanged. AC-017: writer-lock contention prevents receipt write, delete, prune, and quarantine mutation. AC-018: inspect returns only a validated exact run; delete removes only the requested valid run id and rejects traversal-like identifiers. AC-019: default retention removes only completed, unreferenced receipts older than 30 days while retaining active, referenced, and recent records. AC-020: corrupt receipt inspection or pruning moves the original bytes into private quarantine and never treats the record as usable. AC-021: supported Claude input produces user-invocable-only only for exact irrelevant non-plugin skills, with explicit invocation and all conservative outcomes left fully visible. AC-022: bypass or a live lease produces full-load/no-mutation behavior and a sanitized reason receipt. AC-023: successful application preserves unrelated settings, records a private exact baseline, atomically writes the requested profile, and verifies actual state before reporting fresh-session readiness. AC-024: normal restore with an unchanged applied digest returns the exact baseline bytes or exact prior absence and is idempotent. AC-025: a user edit after application causes CAS restore refusal, preserves the edit, disables optimization, and reports one recovery action. AC-026: an abandoned dead-owner lease restores only an unchanged applied state; ambiguous or edited state is preserved and disabled. AC-027: apply, mismatch, contention, restore, and recovery receipts contain replay evidence but no raw settings values. AC-028: the required three-manifest suite validates only when all fixture kinds are unique, schema-valid, and fully fingerprinted. AC-029: a matching baseline/guarded pair with passing completion, instruction, explicit-skill where applicable, restoration, receipt, privacy, and fresh-session evidence passes QG-301 through QG-309 and becomes measurement-authorized. AC-030: each individual QG failure deterministically invalidates the pair with its QG identifier and denies measurement. AC-031: provider/model/repository/task/profile/pair/fixture mismatch is retained as invalid evidence and cannot be authorized. AC-032: attempt and ledger schemas reject unknown or prohibited content fields before persistence. AC-033: invalid and valid retry records coexist; authorization never selects the invalid pair or erases it. AC-034: QA invalidation appends a stable reason and revokes a formerly valid pair without altering earlier records. AC-035: missing, corrupt, ambiguous, or unrecognized ledger evidence denies measurement and never substitutes a zero value. AC-036: quality evaluation and invalidation receipts reproduce gate/action outcomes without raw task, source, provider output, or token data.

AC-037: a supported explicit Claude JSONL file with authorized quality evidence yields a reproducible deduplicated cache-creation, cache-read, and combined total. AC-038: identical duplicate request/message rows count once; inconsistent duplicates, missing IDs, drifted session/model/version, malformed counters, or no eligible rows return unmeasurable without zero substitution. AC-039: extraction reads no undeclared file, launches no provider, and persists no raw content or source path. AC-040: a comparable authorized baseline/guarded pair produces the exact signed unrounded reduction; zero baseline or mismatched correlation is invalid. AC-041: valid negative and extreme reductions remain present in the append-only evidence and aggregation. AC-042: qualification rejects any fixture count other than five valid pairs for each of all three fixture kinds, duplicate pair IDs, or non-alternating declared order. AC-043: median, nearest-rank Q1, and fixture medians match deterministic exact-fraction oracles. AC-044: Claude qualification passes only at provider median >=30 percent, Q1 >=0, every fixture median >=0, and current quality authorization for every pair. AC-045: extraction, pair, and qualification receipts and ledger records reproduce measurement decisions without raw JSONL, prompt, response, source, path, or inferred billed cost.

AC-046: supported Codex inventory reads HOME/.agents/skills and no longer grants guarded credit to HOME/.codex/skills evidence.
AC-047: mixed Codex classifications generate enabled=false entries only for exact irrelevant user-authored skills, with canonical absolute paths and deterministic ordering.
AC-048: applying a supported explicit Codex profile creates or updates only that profile, records a private exact baseline, verifies parse and requested state, and reports the required profile selector plus fresh-thread readiness.
AC-049: unsupported input, bypass, live lease, invalid profile path, parse failure, or verification mismatch produces full-load/no-credit behavior without altering unrelated config.
AC-050: unchanged applied state restores exact baseline bytes or absence and repeated restore is safe.
AC-051: user edit or ambiguous dead-owner state is preserved, disables optimization, and returns one recovery action; unchanged dead-owner state restores safely.
AC-052: Codex profile receipts reproduce requested/actual outcomes and recovery without raw TOML, paths, or skill content.
AC-053: one correlated exact turn.completed event yields its native cached_input_tokens value reproducibly.
AC-054: a correlated monotonic cumulative start/end boundary yields the exact cached-input delta.
AC-055: missing/multiple/drifted/malformed exact events and missing/reset/ambiguous cumulative boundaries are unmeasurable without zero substitution.
AC-056: a matching authorized baseline/guarded Codex pair yields the exact signed reduction; zero baseline or mismatch is invalid.
AC-057: valid negative and extreme Codex reductions remain in append-only evidence and aggregation.
AC-058: qualification requires five distinct alternating valid pairs for each frozen fixture; incomplete, duplicate, mixed-context, or unauthorized populations deny.
AC-059: Codex provider median, nearest-rank Q1, and fixture medians match exact deterministic oracles.
AC-060: Codex passes only at provider median >=30 percent, Q1 >=0, every fixture median >=0, and current quality authorization.
AC-061: later QA invalidation revokes pair/qualification eligibility without rewriting prior measurement evidence.
AC-062: Codex measurement ledger and receipts contain replayable identifiers, fingerprints, counters, fractions, and reasons without raw logs, paths, prompts, responses, source, or billed cost.
AC-063: deterministic Codex profile and measurement commands do not launch a paid provider session or read undeclared files.

## Out of Scope
Automated provider process launch, live qualification execution, performance/net-value qualification, remote synchronization, billed-cost claims, provider pooling, outlier deletion, unsupported IDE/desktop surfaces, and combined rollout.

## Assumptions
The existing built-in/user/repo/environment order remains authoritative. Version-2 relevance rules live under `skills.rules`; provider inventory supplies opaque exact identities.

## Open Questions
No Slice 5 implementation blocker. Live app-server/desktop capability qualification, real five-by-three provider outcomes, and the observed 30 percent reductions remain evidence gaps for later execution.

## Decision Status
Accepted DEC-005 resolves CHG-001 by aligning Codex user skill discovery and profile control with the current official contract. DEC-001 through DEC-005 cover implemented and planned Slices 1–5. No unresolved scope decision blocks deterministic Slice 5 implementation.
