from pathlib import Path

import pytest
import yaml

from context_guard import policy_config
from context_guard.policy_config import PolicyError, classify_skill, skill_rule_conflicts


def test_load_uses_exactly_one_packaged_policy(tmp_path: Path, monkeypatch):
    (tmp_path / ".context-guard").mkdir()
    (tmp_path / ".context-guard" / "policy.yaml").write_text(
        "version: 2\nmode: enforce\nskills:\n  rules: []\n",
        encoding="utf-8",
    )
    user_policy = tmp_path / ".config" / "context-guard" / "policy.yaml"
    user_policy.parent.mkdir(parents=True)
    user_policy.write_text(
        "version: 2\nmode: warn\nskills:\n  rules: []\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("CONTEXT_GUARD_MODE", "enforce")
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    policy = policy_config.load(tmp_path)

    packaged = yaml.safe_load(policy_config.DEFAULTS_PATH.read_text(encoding="utf-8"))
    assert policy.version == 2
    assert policy.mode == packaged["mode"] == "observe"
    assert policy.files == packaged["files"]
    assert policy.sources == [f"packaged:{policy_config.DEFAULTS_PATH}"]


def test_packaged_policy_has_one_empty_skill_rule_set():
    policy = policy_config.load()

    assert policy.skill_rules == ()
    assert classify_skill(policy, provider="claude", skill="test.unused").outcome == "required"
    assert skill_rule_conflicts(policy) == ()


@pytest.mark.parametrize(
    ("content", "code", "path"),
    [
        ("version: 1\n", "POLICY_UNSUPPORTED_VERSION", "version"),
        ("version: 3\n", "POLICY_UNSUPPORTED_VERSION", "version"),
        (
            "version: 2\nskills:\n  rules:\n    - id: x\n      provider: any\n"
            "      skill: x\n      outcome: maybe\n",
            "POLICY_INVALID_VALUE",
            "skills.rules[0].outcome",
        ),
        (
            "version: 2\nskills:\n  rules:\n    - id: x\n      provider: any\n"
            "      skill: x\n      outcome: required\n      surprise: true\n",
            "POLICY_UNKNOWN_FIELD",
            "skills.rules[0].surprise",
        ),
    ],
)
def test_policy_validation_has_stable_code_and_path(
    tmp_path: Path, monkeypatch, content: str, code: str, path: str
):
    candidate = tmp_path / "policy.yaml"
    candidate.write_text(content, encoding="utf-8")
    monkeypatch.setattr(policy_config, "DEFAULTS_PATH", candidate)

    with pytest.raises(PolicyError) as error:
        policy_config.load(tmp_path)

    assert code in str(error.value)
    assert path in str(error.value)


def test_cli_exposes_no_policy_creation_or_migration(capsys):
    from context_guard import cli

    with pytest.raises(SystemExit) as init_exit:
        cli.main(["init"])
    with pytest.raises(SystemExit) as migrate_exit:
        cli.main(["migrate-policy"])

    assert init_exit.value.code == 2
    assert migrate_exit.value.code == 2
    error = capsys.readouterr().err
    assert "invalid choice" in error
