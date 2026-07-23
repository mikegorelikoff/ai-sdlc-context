import json
from pathlib import Path

from context_guard import cli


def test_install_claude_creates_settings(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["install", "claude"]) == 0
    settings_path = tmp_path / cli.CLAUDE_SETTINGS_PATH
    assert settings_path.is_file()
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    for event_name in cli._CLAUDE_HOOK_EVENTS:
        assert event_name in data["hooks"]


def test_install_claude_idempotent_and_preserves_unrelated_hooks(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    settings_path = tmp_path / cli.CLAUDE_SETTINGS_PATH
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(
        json.dumps({"hooks": {"PreToolUse": [{"matcher": "*", "hooks": [{"type": "command", "command": "unrelated-tool"}]}]}}),
        encoding="utf-8",
    )

    assert cli.main(["install", "claude"]) == 0
    first_run = settings_path.read_text(encoding="utf-8")
    assert cli.main(["install", "claude"]) == 0
    second_run = settings_path.read_text(encoding="utf-8")

    assert first_run == second_run
    data = json.loads(second_run)
    commands = [h["command"] for entry in data["hooks"]["PreToolUse"] for h in entry["hooks"]]
    assert "unrelated-tool" in commands
    assert any(cli._MARKER in c for c in commands)


def test_install_codex_creates_config(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["install", "codex"]) == 0
    config_path = tmp_path / cli.CODEX_CONFIG_PATH
    assert config_path.is_file()
    text = config_path.read_text(encoding="utf-8")
    for event_name in cli._CODEX_HOOK_EVENTS:
        assert event_name in text


def test_install_codex_idempotent(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["install", "codex"]) == 0
    first_run = (tmp_path / cli.CODEX_CONFIG_PATH).read_text(encoding="utf-8")
    assert cli.main(["install", "codex"]) == 0
    second_run = (tmp_path / cli.CODEX_CONFIG_PATH).read_text(encoding="utf-8")
    assert first_run == second_run
