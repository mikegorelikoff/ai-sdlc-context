---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "test-cases.md"
  path: "specs/003-context-guard-product-goal/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs/003-context-guard-product-goal/decision-log.md"
  status: "active"
  owner: "QA"
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
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
    - "TC-010"
    - "TC-011"
    - "TC-012"
    - "TC-013"
    - "TC-014"
    - "TC-015"
    - "TC-016"
    - "TC-017"
    - "TC-018"
    - "TC-019"
    - "TC-020"
    - "TC-021"
    - "TC-022"
    - "TC-023"
    - "TC-024"
    - "TC-025"
    - "TC-026"
    - "TC-027"
    - "TC-028"
    - "TC-029"
    - "TC-030"
    - "TC-031"
    - "TC-032"
    - "TC-033"
    - "TC-034"
    - "TC-035"
    - "TC-036"
    - "TC-037"
    - "TC-038"
    - "TC-039"
    - "TC-040"
    - "TC-041"
    - "TC-042"
    - "TC-043"
    - "TC-044"
    - "TC-045"
    - "TC-046"
    - "TC-047"
    - "TC-048"
    - "TC-049"
    - "TC-050"
    - "TC-051"
    - "TC-052"
    - "TC-053"
    - "TC-054"
    - "TC-055"
    - "TC-056"
    - "TC-057"
    - "TC-058"
    - "TC-059"
    - "TC-060"
    - "TC-061"
    - "TC-062"
    - "TC-063"
  related_artifacts:
    - "specs/003-context-guard-product-goal/branch-plan.md"
    - "specs/003-context-guard-product-goal/change-impact.md"
    - "specs/003-context-guard-product-goal/decision-log.md"
    - "specs/003-context-guard-product-goal/design.md"
    - "specs/003-context-guard-product-goal/plan.md"
    - "specs/003-context-guard-product-goal/qa.md"
    - "specs/003-context-guard-product-goal/requirements.md"
    - "specs/003-context-guard-product-goal/tasks.md"
    - "specs/003-context-guard-product-goal/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "active"
    - "slice-5"
    - "slice-4"
    - "slice-1"
---

# Test Cases

## Scope
Covers AC-001–AC-063 through deterministic Claude and Codex guarded-profile and provider-specific measurement verticals. Live provider execution, performance qualification, and combined rollout remain excluded.

## Scenario Matrix
| Test ID | Acceptance Ref | Scenario | Expected Result |
| --- | --- | --- | --- |
| TC-001 | AC-001 | load valid layered v2 twice | identical effective rules |
| TC-002 | AC-002 | override same id | only later object remains |
| TC-003 | AC-003 | disabled exact rule | required default |
| TC-004 | AC-004 | precedence and unknown | only exact irrelevant reduces |
| TC-005 | AC-005 | invalid version/field | stable code and path |
| TC-006 | AC-006 | v1 regression | existing behavior passes |
| TC-007 | AC-007 | init absent/existing | valid v2; no overwrite |
| TC-008 | AC-008 | migrate valid v1 | backup plus atomic v2 |
| TC-009 | AC-009 | migration negative paths | unchanged or safe failure |
| TC-010 | AC-010 | preflight supported and unsupported matrix | exact eligibility/reason |
| TC-011 | AC-011 | read unchanged Claude/Codex fixtures twice | stable sorted records and digests |
| TC-012 | AC-012 | duplicate name or invalid frontmatter | uncertain, empty records/fingerprint |
| TC-013 | AC-013 | mutate fixture between reads | stale uncertainty |
| TC-014 | AC-014 | reverse enumeration order | same canonical fingerprint |
| TC-015 | AC-015 | write and inspect valid receipt | validated JSON and private modes |
| TC-016 | AC-016 | unknown/prohibited fields, malformed values, duplicate run | stable failure; no overwrite |
| TC-017 | AC-017 | hold writer lock while mutating | contention error and unchanged records |
| TC-018 | AC-018 | inspect/delete exact and traversal-like ids | exact result/removal; traversal rejected |
| TC-019 | AC-019 | prune mixed old/recent active/referenced receipts | only eligible old receipt deleted |
| TC-020 | AC-020 | inspect and prune corrupt JSON/schema | original bytes quarantined; no usable result |
| TC-021 | AC-021 | plan mixed Claude classifications and explicit invocation | only exact irrelevant receives user-invocable-only |
| TC-022 | AC-022 | bypass and live-lease contention | no settings mutation; full-load receipt |
| TC-023 | AC-023 | apply to settings with unrelated fields and verify | exact baseline/private state; only requested merge; fresh-session ready |
| TC-024 | AC-024 | restore unchanged applied profile twice | exact baseline then idempotent success |
| TC-025 | AC-025 | edit settings after application then restore | edit preserved; disabled marker and recovery action |
| TC-026 | AC-026 | recover dead-owner unchanged and edited leases | unchanged restores; edited preserves and disables |
| TC-027 | AC-027 | inspect all Claude attempt receipts | replayable allowed fields; no raw settings values |
| TC-028 | AC-028 | validate all required fixture kinds and malformed/duplicate suites | exact three-kind suite passes; incomplete/duplicate fails |
| TC-029 | AC-029 | evaluate fully passing baseline/guarded evidence | QG-301–309 pass and authorization is allowed |
| TC-030 | AC-030 | parameterize one failure for each QG | named gate fails; pair invalid and denied |
| TC-031 | AC-031 | mismatch pair, fixture, provider, model, repository, task, or role profile | QG-302/303 failure retained |
| TC-032 | AC-032 | add prompt/source/token/unknown fields | validation fails before ledger write |
| TC-033 | AC-033 | append invalid pair then valid retry | both retained; only valid retry authorized |
| TC-034 | AC-034 | QA invalidates previously valid pair | append-only invalidation revokes authorization |
| TC-035 | AC-035 | missing/corrupt/ambiguous ledger | authorization denied without zero substitution |
| TC-036 | AC-036 | scan evaluation/invalidation receipts and ledger | replayable reasons with no raw content/token fields |

| TC-037 | AC-037 | extract authorized supported Claude JSONL with repeated identical usage rows | exact creation/read/combined totals; duplicates count once |
| TC-038 | AC-038 | parameterize inconsistent duplicates, missing IDs, drift, malformed counters, and empty window | stable unmeasurable reason; no zero substitution |
| TC-039 | AC-039 | instrument file access and scan persisted evidence | only explicit file read; no provider launch, raw content, or path |
| TC-040 | AC-040 | compare matching baseline/guarded totals including guarded greater than baseline | exact signed rational reduction; zero baseline/mismatch invalid |
| TC-041 | AC-041 | append negative and extreme valid pair reductions | both remain addressable and enter statistics |
| TC-042 | AC-042 | qualify complete five-by-three population then remove/duplicate/reorder pairs | exact complete alternating population passes shape gate; variants deny |
| TC-043 | AC-043 | aggregate odd/even and boundary rational datasets | deterministic exact medians and nearest-rank Q1 match oracle |
| TC-044 | AC-044 | exercise 30 percent, Q1, fixture median, and later quality invalidation boundaries | all gates required; any failed boundary denies |
| TC-045 | AC-045 | inspect extraction/pair/qualification ledger and receipts plus fault injection | replayable minimized evidence, private modes, receipt failure denies, prohibited data absent |

| TC-046 | AC-046 | inventory current and stale Codex user roots | HOME/.agents records stable; stale root receives no credit |
| TC-047 | AC-047 | plan mixed classifications/explicit invocation | only exact irrelevant user skills disabled in sorted absolute-path entries |
| TC-048 | AC-048 | apply explicit absent/existing Codex profile | private baseline, exact generated TOML, verified selector and fresh-thread readiness |
| TC-049 | AC-049 | unsupported/bypass/contention/path/parse/verification variants | full load, bounded/no unrelated mutation, sanitized receipt |
| TC-050 | AC-050 | restore unchanged applied profile twice | exact baseline/absence then idempotent success |
| TC-051 | AC-051 | edit after apply and recover dead-owner unchanged/edited | user edit preserved/disabled; unchanged state safely restores |
| TC-052 | AC-052 | inspect all Codex profile receipts | replayable outcomes without TOML, paths, or skill content |
| TC-053 | AC-053 | parse one correlated Codex exec turn.completed event | exact cached_input_tokens value |
| TC-054 | AC-054 | evaluate monotonic cumulative start/end boundary | exact cached-input delta |
| TC-055 | AC-055 | missing/multiple/drifted/malformed/reset/ambiguous inputs | unmeasurable stable reason; no zero substitution |
| TC-056 | AC-056 | compare matching baseline/guarded including guarded greater | exact signed rational reduction; zero/mismatch invalid |
| TC-057 | AC-057 | retain negative and extreme valid reductions | both remain addressable and enter aggregation |
| TC-058 | AC-058 | qualify five-by-three then remove/duplicate/mix/reorder/invalidate | only complete current alternating population eligible |
| TC-059 | AC-059 | aggregate rational boundary datasets | exact provider median, nearest-rank Q1, fixture medians |
| TC-060 | AC-060 | exercise 30 percent/Q1/fixture boundaries | every conjunctive gate required |
| TC-061 | AC-061 | QA invalidates after pair creation | qualification denied; prior evidence unchanged |
| TC-062 | AC-062 | inspect/scan/fault-inject Codex measurement evidence | minimized private append-only evidence; receipt failure denies |
| TC-063 | AC-063 | instrument process launch and file access | no provider start; only declared files read |

## Layer Mapping
TC-001–TC-045 retain existing policy, inventory, receipt, Claude profile/measurement, quality, and CLI mappings. TC-046 uses updated inventory tests. TC-047–TC-052 use tests/test_codex_profile.py and CLI tests with temporary HOME/config roots. TC-053–TC-063 use tests/test_codex_measurement.py and CLI tests with synthetic exact/cumulative evidence and no provider execution.

## Automation Plan
Run focused inventory, profile, quality, provider measurement, receipt, and CLI suites through tests/run_pytest.py; then all tests and git diff --check through the canonical validation plan. Build docs strictly and run every full-flow SDD gate.

## Open Gaps
No deterministic coverage gap through Slice 5. Live Codex app-server/desktop capability checks, both providers five-by-three execution, performance/net-value evidence, and combined rollout remain later evidence tasks.
