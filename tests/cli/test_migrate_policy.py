from pathlib import Path

import yaml

from context_guard import cli
from context_guard.policy_config import REPO_CONFIG_RELATIVE


def _policy_path(root: Path) -> Path:
    path = root / REPO_CONFIG_RELATIVE
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def test_migrate_v1_creates_backup_and_valid_v2(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    target = _policy_path(tmp_path)
    original = b"version: 1\nmode: enforce\n"
    target.write_bytes(original)

    assert cli.main(["migrate-policy"]) == 0

    backup = target.with_suffix(target.suffix + ".v1.bak")
    assert backup.read_bytes() == original
    migrated = yaml.safe_load(target.read_text(encoding="utf-8"))
    assert migrated["version"] == 2
    assert migrated["mode"] == "enforce"
    assert migrated["skills"] == {"rules": []}
    assert "backup:" in capsys.readouterr().out


def test_migrate_v2_is_noop(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    target = _policy_path(tmp_path)
    original = b"version: 2\nmode: observe\nskills:\n  rules: []\n"
    target.write_bytes(original)

    assert cli.main(["migrate-policy"]) == 0

    assert target.read_bytes() == original
    assert not target.with_suffix(target.suffix + ".v1.bak").exists()
    assert "no changes made" in capsys.readouterr().out


def test_migrate_invalid_v1_does_not_create_backup(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    target = _policy_path(tmp_path)
    original = b"version: 1\nmode: invalid\n"
    target.write_bytes(original)

    assert cli.main(["migrate-policy"]) == 1

    assert target.read_bytes() == original
    assert not target.with_suffix(target.suffix + ".v1.bak").exists()
    assert "POLICY_INVALID_VALUE" in capsys.readouterr().err


def test_migrate_refuses_existing_backup_without_changes(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    target = _policy_path(tmp_path)
    original = b"version: 1\nmode: warn\n"
    target.write_bytes(original)
    backup = target.with_suffix(target.suffix + ".v1.bak")
    backup.write_bytes(b"keep-me")

    assert cli.main(["migrate-policy"]) == 1

    assert target.read_bytes() == original
    assert backup.read_bytes() == b"keep-me"
    assert "POLICY_BACKUP_EXISTS" in capsys.readouterr().err


def test_migrate_requires_repository_policy(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert cli.main(["migrate-policy"]) == 1

    assert "No repository policy found" in capsys.readouterr().err
