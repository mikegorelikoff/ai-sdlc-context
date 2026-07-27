from pathlib import Path

from context_guard import cli
from context_guard.policy_config import REPO_CONFIG_RELATIVE


def test_init_creates_default_policy(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["init"]) == 0
    target = tmp_path / REPO_CONFIG_RELATIVE
    assert target.is_file()
    content = target.read_text(encoding="utf-8")
    assert "version: 2" in content
    assert "mode:" in content
    assert "skills:" in content
    assert "rules: []" in content


def test_init_does_not_overwrite_existing_policy(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    target = tmp_path / REPO_CONFIG_RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("mode: enforce\ncustom: true\n", encoding="utf-8")

    assert cli.main(["init"]) == 0
    assert "custom: true" in target.read_text(encoding="utf-8")
    assert "already exists" in capsys.readouterr().err
