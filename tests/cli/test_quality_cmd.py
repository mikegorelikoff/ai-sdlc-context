from __future__ import annotations

import json
from pathlib import Path

from context_guard import cli, quality


def _manifest(kind: str, fixture_id: str):
    return {
        "schema": quality.MANIFEST_SCHEMA,
        "fixture_id": fixture_id,
        "fixture_kind": kind,
        "provider": "codex",
        "provider_version": "0.144.1",
        "model": "test-model",
        "repository_fingerprint": "repo",
        "task_fingerprint": "task",
        "baseline_profile_fingerprint": "baseline-profile",
        "guarded_profile_fingerprint": "guarded-profile",
        "required_instruction_ids": ["REQ-1"],
    }


def _attempt(role: str, fixture_id: str = "fixture-skill"):
    return {
        "schema": quality.ATTEMPT_SCHEMA,
        "attempt_id": f"attempt-{role}",
        "pair_id": "cli-pair",
        "role": role,
        "fixture_id": fixture_id,
        "provider": "codex",
        "provider_version": "0.144.1",
        "model": "test-model",
        "repository_fingerprint": "repo",
        "task_fingerprint": "task",
        "profile_fingerprint": f"{role}-profile",
        "fresh_session": True,
        "completion_passed": True,
        "observed_instruction_ids": ["REQ-1"],
        "explicit_skill_invoked": True,
        "restoration_passed": True,
        "receipt_ref": f"receipt-{role}",
        "receipt_valid": True,
        "privacy_passed": True,
    }


def _write(path: Path, value: object) -> Path:
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_quality_cli_validates_suite_and_controls_authorization(
    tmp_path: Path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    manifests = [
        _write(tmp_path / "read.json", _manifest("read-only-analysis", "fixture-read")),
        _write(tmp_path / "test.json", _manifest("test-only-change", "fixture-test")),
        _write(
            tmp_path / "skill.json",
            _manifest("explicit-ai-sdlc-skill", "fixture-skill"),
        ),
    ]
    baseline = _write(tmp_path / "baseline.json", _attempt("baseline"))
    guarded = _write(tmp_path / "guarded.json", _attempt("guarded"))

    assert cli.main(["quality", "validate-suite", *map(str, manifests)]) == 0
    assert json.loads(capsys.readouterr().out)["valid"] is True
    assert (
        cli.main(
            [
                "quality",
                "evaluate",
                "--manifest",
                str(manifests[-1]),
                "--baseline",
                str(baseline),
                "--guarded",
                str(guarded),
                "--run-id",
                "cli-quality",
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["measurement_allowed"] is True
    assert cli.main(["quality", "authorize", "cli-pair"]) == 0
    assert json.loads(capsys.readouterr().out)["allowed"] is True
    assert (
        cli.main(
            [
                "quality",
                "invalidate",
                "cli-pair",
                "--run-id",
                "cli-invalidate",
                "--reason",
                "qa-revoked",
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["allowed"] is False
    assert cli.main(["quality", "authorize", "cli-pair"]) == 1
    assert json.loads(capsys.readouterr().out)["reason_code"] == "qa-revoked"


def test_quality_cli_rejects_unknown_content_without_ledger(
    tmp_path: Path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    manifest = _manifest("explicit-ai-sdlc-skill", "fixture-skill")
    manifest["prompt"] = "raw task"
    path = _write(tmp_path / "unsafe.json", manifest)

    assert cli.main(["quality", "validate-suite", str(path)]) == 1
    assert "unknown fields" in capsys.readouterr().err
    assert not (tmp_path / ".context-guard" / "quality" / "ledger.jsonl").exists()
