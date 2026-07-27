from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "examples" / "run_demo.py"
EXPECTED = ROOT / "examples" / "output" / "demo-output.json"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_checked_in_demo_output_is_current_and_has_native_token_totals():
    result = _run("--check")

    assert result.returncode == 0, result.stderr
    evidence = json.loads(result.stdout)
    assert evidence["evidence_kind"] == "deterministic-fixture"
    assert evidence["claude"]["measurement"]["cache_creation_tokens"] == 1200
    assert evidence["claude"]["measurement"]["cache_read_tokens"] == 3800
    assert evidence["claude"]["measurement"]["cache_tokens"] == 5000
    assert evidence["codex"]["measurement"]["cached_input_tokens"] == 4200
    assert evidence["claude"]["paired_example"] == {
        "baseline_cache_tokens": 5000,
        "guarded_cache_tokens": 3000,
        "reduction_denominator": 5,
        "reduction_numerator": 2,
        "reduction_percent": 40,
    }
    assert evidence["codex"]["paired_example"] == {
        "baseline_cached_input_tokens": 4200,
        "guarded_cached_input_tokens": 2520,
        "reduction_denominator": 5,
        "reduction_numerator": 2,
        "reduction_percent": 40,
    }
    assert evidence["claude"]["profile_plan"]["overrides"] == {
        "unused": "user-invocable-only"
    }
    assert evidence["codex"]["profile_plan"]["disabled_skills"] == ["unused"]
    assert evidence["claude"]["profile_plan"]["explicit_skill_preserved"] == "manual"
    assert evidence["codex"]["profile_plan"]["explicit_skill_preserved"] == "manual"


def test_demo_includes_fail_closed_examples():
    result = _run()

    assert result.returncode == 0, result.stderr
    evidence = json.loads(result.stdout)
    assert evidence["fail_closed_examples"]["missing_quality_evidence"] == {
        "measurement_allowed": False,
        "reason_code": "missing-quality-evidence",
    }
    assert evidence["fail_closed_examples"]["unsupported_provider_version"] == {
        "reason_code": "unsupported-version",
        "status": "unsupported",
    }
    assert evidence["fail_closed_examples"]["stale_inventory"] == {
        "reason_code": "stale-inventory",
        "savings_credit_allowed": False,
        "status": "uncertain",
    }


def test_demo_exercises_restore_cumulative_and_negative_evidence():
    result = _run()

    assert result.returncode == 0, result.stderr
    evidence = json.loads(result.stdout)
    assert evidence["claude"]["profile_lifecycle"]["baseline_restored"] is True
    assert evidence["claude"]["profile_lifecycle"]["apply_status"] == "reduced"
    assert evidence["claude"]["profile_lifecycle"]["restore_status"] == "restored"
    assert evidence["codex"]["profile_lifecycle"]["baseline_restored"] is True
    assert evidence["codex"]["profile_lifecycle"]["apply_status"] == "reduced"
    assert evidence["codex"]["profile_lifecycle"]["restore_status"] == "restored"
    assert evidence["codex"]["cumulative_boundary_example"] == {
        "end_cached_input_tokens": 4200,
        "measured_delta": 3200,
        "measurement_mode": "cumulative-boundary",
        "start_cached_input_tokens": 1000,
    }
    assert evidence["claude"]["negative_pair_example"]["reduction_percent"] == -20
    assert evidence["codex"]["negative_pair_example"]["reduction_percent"] == -20
    assert evidence["claude"]["negative_pair_example"]["outcome"] == (
        "regression-visible"
    )


def test_demo_output_excludes_raw_content_and_absolute_home():
    result = _run()

    assert result.returncode == 0, result.stderr
    serialized = result.stdout.lower()
    assert str(Path.home()).lower() not in serialized
    assert "fixture private content" not in serialized
    assert "second fixture private message" not in serialized
    evidence = json.loads(result.stdout)

    def keys(value):
        if isinstance(value, dict):
            for key, nested in value.items():
                yield key
                yield from keys(nested)
        elif isinstance(value, list):
            for nested in value:
                yield from keys(nested)

    assert not {"content", "path", "prompt", "raw", "response"} & set(keys(evidence))


def test_check_detects_output_drift(tmp_path: Path):
    stale = tmp_path / "stale.json"
    stale.write_text("{}\n", encoding="utf-8")

    result = _run("--check", "--expected", str(stale))

    assert result.returncode == 1
    assert "example output drift" in result.stderr


def test_write_can_generate_a_fresh_expected_file(tmp_path: Path):
    output = tmp_path / "generated.json"

    written = _run("--write", "--expected", str(output))
    checked = _run("--check", "--expected", str(output))

    assert written.returncode == 0, written.stderr
    assert checked.returncode == 0, checked.stderr
    assert json.loads(output.read_text(encoding="utf-8")) == json.loads(written.stdout)
    assert EXPECTED.is_file()
