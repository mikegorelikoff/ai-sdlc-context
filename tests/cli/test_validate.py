from pathlib import Path

from context_guard import cli


def test_validate_reports_the_single_packaged_policy(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert cli.main(["validate"]) == 0

    output = capsys.readouterr().out
    assert "Policy valid" in output
    assert "packaged:" in output


def test_validate_ignores_repository_policy_files(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    repo_config = tmp_path / ".context-guard" / "policy.yaml"
    repo_config.parent.mkdir(parents=True)
    repo_config.write_text("mode: [unclosed\n", encoding="utf-8")

    assert cli.main(["validate"]) == 0

    output = capsys.readouterr().out
    assert "Policy valid" in output
    assert str(repo_config) not in output
