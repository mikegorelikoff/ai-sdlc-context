---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-context-guard-product-goal"
  artifact: "security-review.md"
  path: "specs/003-context-guard-product-goal/security-review.md"
  workspace: "implementation"
  skill: "ai-sdlc-security-testing"
  flow_mode: "full"
  state_file: "specs/003-context-guard-product-goal/_ai_sdlc/state.toon"
  decision_log: "specs/003-context-guard-product-goal/decision-log.md"
  status: "approved"
  owner: "Engineering and Security"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "TC-015"
    - "TC-020"
    - "TC-028"
    - "TC-036"
    - "TC-046"
    - "TC-063"
  related_artifacts:
    - "specs/003-context-guard-product-goal/branch-plan.md"
    - "specs/003-context-guard-product-goal/change-impact.md"
    - "specs/003-context-guard-product-goal/code-review.md"
    - "specs/003-context-guard-product-goal/decision-log.md"
    - "specs/003-context-guard-product-goal/design.md"
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
    - "ai-sdlc-security-testing"
    - "security-review"
    - "approved"
    - "mvp"
---

# security-review.md

## Trust Boundaries
Confirmed facts:\n- Context Guard is a local same-user CLI, not a network service or multi-tenant control plane.\n- Explicit repository and HOME roots bound all mutations. Provider JSONL, TOML, JSON, YAML, skill metadata, and persisted ledgers are treated as untrusted evidence.\n- Privileged local effects are limited to a dedicated Codex profile, an explicit Claude settings file, and private repository-local Context Guard storage.\nEvidence:\n- requirements FR-011 through FR-075; design Architecture, Error Handling, and Security Considerations; inventory.py; claude_profile.py; codex_profile.py; receipts.py.\nOpen questions or blockers:\n- No blocker. A hostile process already running as the same OS user remains outside the isolation boundary and can race ordinary filesystem operations.

## Authn/Authz
Confirmed facts:\n- There is no application authentication, tenant, organization, or remote authorization boundary in the MVP.\n- The OS user account is the authority for explicit local files. Reducing actions additionally require supported provider preflight, current stable inventory correlation, exact classifications, and a quality-authorized measurement pair.\n- Context Guard never launches Claude or Codex and never performs a remote provider action.\nEvidence:\n- FR-026, FR-027, FR-039, FR-043, FR-057, FR-058, FR-064; profile and measurement command implementations.\nOpen questions or blockers:\n- No blocker. Shared-machine access control is delegated to operating-system file permissions.

## Input Validation
Confirmed facts:\n- Run identifiers, provider versions and surfaces, profile names, classification enums, exact skill locators, JSON and TOML schemas, counters, boundary identifiers, pair roles, fixture populations, and rational statistics are validated before credit.\n- Codex reducing profiles reread HOME/.agents/skills, require an exact fingerprint match, and correlate every supplied name and locator to that inventory.\n- Unknown evidence fields, negative or Boolean counters, duplicate identifiers, malformed JSONL, model or provider drift, counter resets, stale evidence, and corrupt nested ledger records fail closed.\nEvidence:\n- inventory.py; receipts.py; quality.py; claude_measurement.py; codex_measurement.py; code-review.md.\nOpen questions or blockers:\n- No blocker.

## Secret Handling
Confirmed facts:\n- Receipts use an exact allowlist and reject prompt, response, source, credential, secret, environment-value, and full-body fields.\n- Raw provider logs and model content are read only from explicit paths and are never copied into measurement ledgers.\n- Exact profile baselines are retained only in private state with owner-only directory and file modes.\nEvidence:\n- FR-016 through FR-024, FR-034, FR-036, FR-044, FR-050, FR-063, FR-069, FR-074; receipt and privacy tests.\nOpen questions or blockers:\n- No blocker. The application does not read provider credentials or make network requests.

## Data Exposure
Confirmed facts:\n- Normal CLI results expose identifiers, status, reason codes, counts, digests, selectors, and exact token statistics only.\n- Receipts, quality ledgers, and measurement ledgers exclude raw paths, profile contents, prompts, responses, message content, credentials, and environment values.\n- Private roots reject preexisting symlinks before creating storage, preventing a malicious repository from redirecting state writes through a committed .context-guard link.\nEvidence:\n- receipt schemas; profile result schemas; measurement schemas; symlink rejection tests in test_receipts.py and test_codex_profile.py.\nOpen questions or blockers:\n- No blocker.

## Abuse Cases
Confirmed facts:\n- Duplicate run IDs cannot overwrite receipts or ledger evidence.\n- Live leases prevent concurrent profile writers; dead-owner recovery requires liveness failure and compare-and-swap; user edits are preserved and disable optimization.\n- Malformed or ambiguous provider events, forged quality context, stale inventory fingerprints, outside-inventory skill paths, cumulative counter resets, corrupt ledgers, and symlinked private roots are rejected without savings credit.\n- The security review resolved one medium local-filesystem finding by adding no-follow checks across receipt, profile, quality, and measurement private roots.\nEvidence:\n- TC-015 through TC-020, TC-028 through TC-036, TC-046 through TC-063; 229-test repository suite.\nOpen questions or blockers:\n- No blocker. Residual low risk: explicit very large local JSONL or ledger files can consume local CPU and I/O; inputs are same-user selected and streamed where practical, but hard byte limits are not part of MVP.

## Security Validation
Findings:\n- No open critical, high, medium, or low security findings remain.\nResolved finding:\n- MEDIUM: preexisting symlinks beneath the repository private-state root could redirect local writes into another same-user directory. Private storage creation now rejects symlinks before and after directory creation across receipts, profiles, quality, and measurements; negative tests confirm no redirected files are created.\nValidation:\n- The canonical command plan passes with 229 repository tests and zero failures.\n- Strict MkDocs, sandbox-safe Python compilation, SDD analysis and validation, plan-link validation, receipt freshness verification, and git diff hygiene pass.\n- Security-focused negative coverage includes traversal-like IDs, unknown sensitive fields, private modes, non-overwrite, lock contention, user-edit preservation, stale inventory, outside-inventory paths, malformed and corrupt evidence, and symlink redirection.\nValidation gaps:\n- Live provider pilots and observed 30 percent savings are not security requirements and remain unexecuted.\n- No hostile same-user concurrent filesystem race test is claimed; the OS account is the stated trust boundary.\nOpen questions or blockers:\n- None.
