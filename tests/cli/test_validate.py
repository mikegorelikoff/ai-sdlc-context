from pathlib import Path

from context_guard import cli


def test_validate_passes_with_no_repo_config(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["validate"]) == 0
    assert "Policy valid" in capsys.readouterr().out


def test_validate_fails_on_invalid_policy(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    repo_config = tmp_path / ".context-guard" / "policy.yaml"
    repo_config.parent.mkdir(parents=True, exist_ok=True)
    repo_config.write_text("mode: not-a-real-mode\n", encoding="utf-8")

    assert cli.main(["validate"]) == 1
    assert "Invalid policy configuration" in capsys.readouterr().err


def test_validate_fails_on_malformed_yaml(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    repo_config = tmp_path / ".context-guard" / "policy.yaml"
    repo_config.parent.mkdir(parents=True, exist_ok=True)
    repo_config.write_text("mode: [unclosed\n", encoding="utf-8")

    assert cli.main(["validate"]) == 1
