from pathlib import Path

from context_guard import cli


def test_test_command_runs_bundled_fixtures(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    result = cli.main(["test"])
    output = capsys.readouterr().out
    assert result == 0
    assert "fixtures passed" in output
    assert "FAIL" not in output
