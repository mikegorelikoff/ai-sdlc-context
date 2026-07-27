#!/usr/bin/env python3
"""Run a deterministic, privacy-safe Context Guard demonstration."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from context_guard import (  # noqa: E402
    claude_measurement,
    claude_profile,
    codex_measurement,
    codex_profile,
    inventory,
    quality,
    receipts,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"
DEFAULT_EXPECTED = Path(__file__).resolve().parent / "output" / "demo-output.json"
FORBIDDEN_KEYS = {"content", "path", "prompt", "raw", "response"}


def _install_skills(home: Path, provider_root: str) -> None:
    destination = home / provider_root / "skills"
    shutil.copytree(FIXTURES / "skills", destination)


def _authorize(
    repo: Path,
    *,
    provider: str,
    version: str,
    model: str,
    pair_id: str,
) -> None:
    manifest = quality.QualityManifest.from_dict(
        {
            "schema": quality.MANIFEST_SCHEMA,
            "fixture_id": f"{provider}-demo",
            "fixture_kind": "read-only-analysis",
            "provider": provider,
            "provider_version": version,
            "model": model,
            "repository_fingerprint": "demo-repository",
            "task_fingerprint": "demo-task",
            "baseline_profile_fingerprint": "baseline",
            "guarded_profile_fingerprint": "guarded",
            "required_instruction_ids": ["DEMO-REQ-1"],
        }
    )

    def attempt(role: str) -> quality.AttemptEvidence:
        return quality.AttemptEvidence.from_dict(
            {
                "schema": quality.ATTEMPT_SCHEMA,
                "attempt_id": f"{pair_id}-{role}",
                "pair_id": pair_id,
                "role": role,
                "fixture_id": f"{provider}-demo",
                "provider": provider,
                "provider_version": version,
                "model": model,
                "repository_fingerprint": "demo-repository",
                "task_fingerprint": "demo-task",
                "profile_fingerprint": role,
                "fresh_session": True,
                "completion_passed": True,
                "observed_instruction_ids": ["DEMO-REQ-1"],
                "explicit_skill_invoked": True,
                "restoration_passed": True,
                "receipt_ref": f"{pair_id}-{role}-receipt",
                "receipt_valid": True,
                "privacy_passed": True,
            }
        )

    result = quality.QualityLedger(repo).record_evaluation(
        manifest,
        attempt("baseline"),
        attempt("guarded"),
        run_id=f"{pair_id}-evaluation",
    )
    if not result.measurement_allowed:
        raise RuntimeError(f"quality authorization failed for {provider}")


def _provider_inventory(home: Path, provider: str, version: str) -> Any:
    result = inventory.read_inventory(
        home,
        provider=provider,
        version=version,
        surface="cli",
    )
    if result.status != "supported" or result.fingerprint is None:
        raise RuntimeError(f"{provider} inventory is not stable: {result.reason_code}")
    return result


def build_demo() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="context-guard-example-") as temporary:
        sandbox = Path(temporary)
        home = sandbox / "home"
        repo = sandbox / "repo"
        repo.mkdir()
        _install_skills(home, ".claude")
        _install_skills(home, ".agents")

        claude_inventory = _provider_inventory(home, "claude", "2.1.218")
        codex_inventory = _provider_inventory(home, "codex", "0.144.1")
        classifications = {
            "manual": "irrelevant",
            "needed": "required",
            "unused": "irrelevant",
        }

        claude_overrides = claude_profile.plan_overrides(
            classifications,
            explicit_invocations={"manual"},
        )
        codex_paths = {
            record.name: Path(record.locator) for record in codex_inventory.records
        }
        codex_disabled = codex_profile.plan_disabled_paths(
            classifications,
            codex_paths,
            explicit_invocations={"manual"},
        )

        claude_settings = home / ".claude" / "settings.local.json"
        claude_baseline = b'{"model":"demo"}\n'
        claude_settings.write_bytes(claude_baseline)
        claude_applied = claude_profile.apply_profile(
            repo,
            claude_settings,
            run_id="claude-demo-apply",
            version="2.1.218",
            surface="cli",
            classifications=classifications,
            explicit_invocations={"manual"},
            inventory_fingerprint=claude_inventory.fingerprint,
        )
        claude_restored = claude_profile.restore_profile(
            repo,
            claude_settings,
            run_id="claude-demo-restore",
            version="2.1.218",
        )

        codex_profile_path = home / ".codex" / "context-guard.config.toml"
        codex_applied = codex_profile.apply_profile(
            repo,
            home,
            profile="context-guard",
            run_id="codex-demo-apply",
            version="0.144.1",
            surface="cli",
            classifications=classifications,
            skill_paths=codex_paths,
            explicit_invocations={"manual"},
            inventory_fingerprint=codex_inventory.fingerprint,
        )
        codex_restored = codex_profile.restore_profile(
            repo,
            home,
            profile="context-guard",
            run_id="codex-demo-restore",
            version="0.144.1",
        )

        _authorize(
            repo,
            provider="claude",
            version="2.1.218",
            model="claude-demo",
            pair_id="claude-demo-quality",
        )
        claude_run = claude_measurement.extract_run(
            repo,
            FIXTURES / "claude-session.jsonl",
            run_id="claude-demo-baseline",
            quality_pair_id="claude-demo-quality",
            fixture_kind="read-only-analysis",
            role="baseline",
            provider_version="2.1.218",
            model="claude-demo",
            session_id="demo-claude",
        )
        claude_guarded = claude_measurement.extract_run(
            repo,
            FIXTURES / "claude-session-guarded.jsonl",
            run_id="claude-demo-guarded",
            quality_pair_id="claude-demo-quality",
            fixture_kind="read-only-analysis",
            role="guarded",
            provider_version="2.1.218",
            model="claude-demo",
            session_id="demo-claude-guarded",
        )
        claude_pair = claude_measurement.compare_pair(
            repo,
            claude_run,
            claude_guarded,
            pair_id="claude-demo-pair",
            execution_order="baseline-first",
        )
        claude_regression = claude_measurement.extract_run(
            repo,
            FIXTURES / "claude-session-regression.jsonl",
            run_id="claude-demo-regression",
            quality_pair_id="claude-demo-quality",
            fixture_kind="read-only-analysis",
            role="guarded",
            provider_version="2.1.218",
            model="claude-demo",
            session_id="demo-claude-regression",
        )
        claude_negative_pair = claude_measurement.compare_pair(
            repo,
            claude_run,
            claude_regression,
            pair_id="claude-demo-negative-pair",
            execution_order="guarded-first",
        )

        _authorize(
            repo,
            provider="codex",
            version="0.144.1",
            model="codex-demo",
            pair_id="codex-demo-quality",
        )
        codex_run = codex_measurement.extract_exact_run(
            repo,
            FIXTURES / "codex-exec.jsonl",
            run_id="codex-demo-baseline",
            quality_pair_id="codex-demo-quality",
            fixture_kind="read-only-analysis",
            role="baseline",
            provider_version="0.144.1",
            model="codex-demo",
            thread_id="demo-codex",
        )
        codex_guarded = codex_measurement.extract_exact_run(
            repo,
            FIXTURES / "codex-exec-guarded.jsonl",
            run_id="codex-demo-guarded",
            quality_pair_id="codex-demo-quality",
            fixture_kind="read-only-analysis",
            role="guarded",
            provider_version="0.144.1",
            model="codex-demo",
            thread_id="demo-codex-guarded",
        )
        codex_pair = codex_measurement.compare_pair(
            repo,
            codex_run,
            codex_guarded,
            pair_id="codex-demo-pair",
            execution_order="baseline-first",
        )
        codex_regression = codex_measurement.extract_exact_run(
            repo,
            FIXTURES / "codex-exec-regression.jsonl",
            run_id="codex-demo-regression",
            quality_pair_id="codex-demo-quality",
            fixture_kind="read-only-analysis",
            role="guarded",
            provider_version="0.144.1",
            model="codex-demo",
            thread_id="demo-codex-regression",
        )
        codex_negative_pair = codex_measurement.compare_pair(
            repo,
            codex_run,
            codex_regression,
            pair_id="codex-demo-negative-pair",
            execution_order="guarded-first",
        )
        codex_cumulative = codex_measurement.measure_cumulative_run(
            repo,
            run_id="codex-demo-cumulative",
            quality_pair_id="codex-demo-quality",
            fixture_kind="read-only-analysis",
            role="baseline",
            provider_version="0.144.1",
            model="codex-demo",
            thread_id="demo-codex-cumulative",
            start_boundary_id="before-turn",
            end_boundary_id="after-turn",
            start_cached_input_tokens=1000,
            end_cached_input_tokens=4200,
        )
        missing_quality = quality.QualityLedger(repo).authorize_measurement(
            "missing-demo-quality",
            provider="claude",
            provider_version="2.1.218",
            model="claude-demo",
            fixture_kind="read-only-analysis",
        )
        unsupported = inventory.preflight("claude", "2.1.217", "cli")
        unstable_home = sandbox / "unstable-home"
        _install_skills(unstable_home, ".claude")
        changing_skill = unstable_home / ".claude" / "skills" / "unused" / "SKILL.md"

        def mutate_inventory() -> None:
            changing_skill.write_text(
                changing_skill.read_text(encoding="utf-8") + "\nchanged\n",
                encoding="utf-8",
            )

        stale_inventory = inventory.read_inventory(
            unstable_home,
            provider="claude",
            version="2.1.218",
            surface="cli",
            between_reads=mutate_inventory,
        )
        claude_apply_receipt = receipts.inspect_receipt(repo, "claude-demo-apply")

        result: dict[str, object] = {
            "schema": "context-guard-example/v1",
            "evidence_kind": "deterministic-fixture",
            "privacy": {
                "raw_logs_persisted": False,
                "prompts_or_responses_persisted": False,
                "absolute_user_paths_persisted": False,
            },
            "claude": {
                "provider_version": "2.1.218",
                "inventory": {
                    "status": claude_inventory.status,
                    "reason_code": claude_inventory.reason_code,
                    "skill_count": len(claude_inventory.records),
                    "skill_names": [record.name for record in claude_inventory.records],
                    "fingerprint_present": bool(claude_inventory.fingerprint),
                },
                "profile_plan": {
                    "status": "reduced",
                    "overrides": claude_overrides,
                    "explicit_skill_preserved": "manual",
                    "fresh_session_required": True,
                },
                "profile_lifecycle": {
                    "apply_status": claude_applied.status,
                    "restore_status": claude_restored.status,
                    "baseline_restored": claude_settings.read_bytes()
                    == claude_baseline,
                    "receipt_status": claude_apply_receipt["status"],
                    "receipt_action": claude_apply_receipt["actual_action"],
                },
                "measurement": {
                    "status": claude_run.status,
                    "reason_code": claude_run.reason_code,
                    "eligible_rows": claude_run.eligible_rows,
                    "duplicate_rows": claude_run.duplicate_rows,
                    "cache_creation_tokens": claude_run.cache_creation_tokens,
                    "cache_read_tokens": claude_run.cache_read_tokens,
                    "cache_tokens": claude_run.cache_tokens,
                    "source_fingerprint": claude_run.source_fingerprint,
                },
                "paired_example": {
                    "baseline_cache_tokens": claude_pair.baseline_cache_tokens,
                    "guarded_cache_tokens": claude_pair.guarded_cache_tokens,
                    "reduction_numerator": claude_pair.reduction_numerator,
                    "reduction_denominator": claude_pair.reduction_denominator,
                    "reduction_percent": 100
                    * claude_pair.reduction_numerator
                    // claude_pair.reduction_denominator,
                },
                "negative_pair_example": {
                    "baseline_cache_tokens": (
                        claude_negative_pair.baseline_cache_tokens
                    ),
                    "guarded_cache_tokens": (
                        claude_negative_pair.guarded_cache_tokens
                    ),
                    "reduction_percent": 100
                    * claude_negative_pair.reduction_numerator
                    // claude_negative_pair.reduction_denominator,
                    "outcome": "regression-visible",
                },
            },
            "codex": {
                "provider_version": "0.144.1",
                "inventory": {
                    "status": codex_inventory.status,
                    "reason_code": codex_inventory.reason_code,
                    "skill_count": len(codex_inventory.records),
                    "skill_names": [record.name for record in codex_inventory.records],
                    "fingerprint_present": bool(codex_inventory.fingerprint),
                },
                "profile_plan": {
                    "status": "reduced",
                    "disabled_skills": [item.parent.name for item in codex_disabled],
                    "explicit_skill_preserved": "manual",
                    "fresh_process_required": True,
                },
                "profile_lifecycle": {
                    "apply_status": codex_applied.status,
                    "restore_status": codex_restored.status,
                    "baseline_restored": not codex_profile_path.exists(),
                },
                "measurement": {
                    "status": codex_run.status,
                    "reason_code": codex_run.reason_code,
                    "measurement_mode": codex_run.measurement_mode,
                    "cached_input_tokens": codex_run.cached_input_tokens,
                    "source_fingerprint": codex_run.source_fingerprint,
                },
                "paired_example": {
                    "baseline_cached_input_tokens": (
                        codex_pair.baseline_cached_input_tokens
                    ),
                    "guarded_cached_input_tokens": (
                        codex_pair.guarded_cached_input_tokens
                    ),
                    "reduction_numerator": codex_pair.reduction_numerator,
                    "reduction_denominator": codex_pair.reduction_denominator,
                    "reduction_percent": 100
                    * codex_pair.reduction_numerator
                    // codex_pair.reduction_denominator,
                },
                "negative_pair_example": {
                    "baseline_cached_input_tokens": (
                        codex_negative_pair.baseline_cached_input_tokens
                    ),
                    "guarded_cached_input_tokens": (
                        codex_negative_pair.guarded_cached_input_tokens
                    ),
                    "reduction_percent": 100
                    * codex_negative_pair.reduction_numerator
                    // codex_negative_pair.reduction_denominator,
                    "outcome": "regression-visible",
                },
                "cumulative_boundary_example": {
                    "start_cached_input_tokens": 1000,
                    "end_cached_input_tokens": 4200,
                    "measured_delta": codex_cumulative.cached_input_tokens,
                    "measurement_mode": codex_cumulative.measurement_mode,
                },
            },
            "fail_closed_examples": {
                "unsupported_provider_version": {
                    "status": unsupported.status,
                    "reason_code": unsupported.reason_code,
                },
                "missing_quality_evidence": {
                    "measurement_allowed": missing_quality.allowed,
                    "reason_code": missing_quality.reason_code,
                },
                "stale_inventory": {
                    "status": stale_inventory.status,
                    "reason_code": stale_inventory.reason_code,
                    "savings_credit_allowed": False,
                },
            },
        }
        _assert_private(result, forbidden_values=(temporary, str(Path.home())))
        return result


def _assert_private(value: object, *, forbidden_values: tuple[str, ...]) -> None:
    def visit(item: object) -> None:
        if isinstance(item, dict):
            for key, nested in item.items():
                lowered = str(key).lower()
                if lowered in FORBIDDEN_KEYS:
                    raise RuntimeError(f"forbidden output key: {key}")
                visit(nested)
        elif isinstance(item, list):
            for nested in item:
                visit(nested)
        elif isinstance(item, str):
            for forbidden in forbidden_values:
                if forbidden and forbidden in item:
                    raise RuntimeError("private path leaked into output")

    visit(value)


def _render(value: dict[str, object]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="verify checked-in output")
    mode.add_argument("--write", action="store_true", help="refresh checked-in output")
    parser.add_argument(
        "--expected",
        type=Path,
        default=DEFAULT_EXPECTED,
        help="expected output used by --check or --write",
    )
    args = parser.parse_args()

    rendered = _render(build_demo())
    if args.write:
        args.expected.parent.mkdir(parents=True, exist_ok=True)
        args.expected.write_text(rendered, encoding="utf-8")
    elif args.check:
        if not args.expected.is_file():
            print(f"missing expected output: {args.expected}", file=sys.stderr)
            return 1
        if args.expected.read_text(encoding="utf-8") != rendered:
            print(f"example output drift: {args.expected}", file=sys.stderr)
            return 1
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
