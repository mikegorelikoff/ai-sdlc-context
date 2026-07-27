from __future__ import annotations

import json
from pathlib import Path

from context_guard import cli, inventory


def test_codex_profile_cli_apply_status_restore(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    home = tmp_path / "home"
    skill = home / ".agents" / "skills" / "unused" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("---\nname: unused\n---\nbody\n", encoding="utf-8")
    fingerprint = inventory.read_inventory(
        home, provider="codex", version="0.144.1", surface="cli"
    ).fingerprint

    assert cli.main(
        [
            "codex-profile", "apply", "--home", str(home),
            "--profile", "guarded", "--run-id", "apply",
            "--version", "0.144.1", "--inventory-fingerprint", str(fingerprint),
            "--classification", "unused=irrelevant",
            "--skill", f"unused={skill}",
        ]
    ) == 0
    applied = json.loads(capsys.readouterr().out)
    assert applied["status"] == "reduced"
    assert applied["fresh_process_required"] is True

    assert cli.main(
        ["codex-profile", "status", "--home", str(home), "--profile", "guarded"]
    ) == 0
    assert json.loads(capsys.readouterr().out)["selector"] == ["--profile", "guarded"]

    assert cli.main(
        [
            "codex-profile", "restore", "--home", str(home),
            "--profile", "guarded", "--run-id", "restore",
            "--version", "0.144.1",
        ]
    ) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "restored"
    assert not (home / ".codex" / "guarded.config.toml").exists()


def test_codex_profile_cli_falls_back_for_non_inventory_skill_path(
    tmp_path: Path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    home = tmp_path / "home"
    skill = home / ".agents" / "skills" / "unused" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("---\nname: unused\n---\nbody\n", encoding="utf-8")
    fingerprint = inventory.read_inventory(
        home, provider="codex", version="0.144.1", surface="cli"
    ).fingerprint
    assert cli.main(
        [
            "codex-profile", "apply", "--home", str(home),
            "--profile", "guarded", "--run-id", "bad",
            "--version", "0.144.1", "--inventory-fingerprint", str(fingerprint),
            "--classification", "unused=irrelevant",
            "--skill", "unused=relative/SKILL.md",
        ]
    ) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "full-load"
    assert result["reason_code"] == "inventory-correlation-mismatch"
