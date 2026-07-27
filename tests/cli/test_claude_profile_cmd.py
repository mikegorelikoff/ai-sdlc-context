from __future__ import annotations

import json
from pathlib import Path

from context_guard import cli


def test_claude_profile_cli_apply_status_restore(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    settings = tmp_path / "home" / ".claude" / "settings.local.json"
    settings.parent.mkdir(parents=True)
    baseline = b'{"model":"sonnet"}\n'
    settings.write_bytes(baseline)

    assert cli.main(
        [
            "claude-profile",
            "apply",
            str(settings),
            "--run-id",
            "cli-apply",
            "--version",
            "2.1.218",
            "--inventory-fingerprint",
            "inventory-fingerprint",
            "--classification",
            "unused=irrelevant",
            "--classification",
            "required=required",
        ]
    ) == 0
    applied = json.loads(capsys.readouterr().out)
    assert applied["status"] == "reduced"
    assert applied["fresh_session_required"] is True

    assert cli.main(["claude-profile", "status", str(settings)]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["leased"] is True
    assert status["disabled"] is False

    assert cli.main(
        [
            "claude-profile",
            "restore",
            str(settings),
            "--run-id",
            "cli-restore",
            "--version",
            "2.1.218",
        ]
    ) == 0
    restored = json.loads(capsys.readouterr().out)
    assert restored["status"] == "restored"
    assert settings.read_bytes() == baseline


def test_claude_profile_cli_rejects_bad_classification_syntax(
    tmp_path: Path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    settings = tmp_path / "settings.json"

    assert cli.main(
        [
            "claude-profile",
            "apply",
            str(settings),
            "--run-id",
            "bad-cli",
            "--version",
            "2.1.218",
            "--inventory-fingerprint",
            "inventory-fingerprint",
            "--classification",
            "not-valid",
        ]
    ) == 1
    assert "NAME=CLASSIFICATION" in capsys.readouterr().err
    assert not settings.exists()
