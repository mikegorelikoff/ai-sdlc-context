from pathlib import Path

from context_guard import cli


def test_doctor_reports_python_and_policy_status(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["doctor"]) == 0
    output = capsys.readouterr().out
    assert "Python:" in output
    assert "Policy resolution: OK" in output
    assert "Claude Code hooks installed: False" in output
    assert "Codex hooks installed: False" in output


def test_doctor_detects_installed_hooks(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    cli.main(["install", "claude"])
    cli.main(["install", "codex"])
    assert cli.main(["doctor"]) == 0
    output = capsys.readouterr().out
    assert "Claude Code hooks installed: True" in output
    assert "Codex hooks installed: True" in output
