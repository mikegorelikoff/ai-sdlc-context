from pathlib import Path

import pytest

from context_guard import policy_config
from context_guard.policy_config import PolicyError, classify_skill, skill_rule_conflicts


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_v2_exact_irrelevant_match(monkeypatch, tmp_path: Path):
    user = tmp_path / "user.yaml"
    repo = tmp_path / "repo"
    _write(
        user,
        """
version: 2
skills:
  rules:
    - id: unused-test-skill
      provider: any
      skill: test.unused
      outcome: irrelevant
      reason_code: task-does-not-use-skill
""",
    )
    monkeypatch.setattr(policy_config, "USER_CONFIG_PATH", user)

    policy = policy_config.load(repo)

    assert policy.version == 2
    assert classify_skill(policy, provider="claude", skill="test.unused").outcome == "irrelevant"
    assert classify_skill(policy, provider="claude", skill="test.unused-extra").outcome == "required"


def test_same_id_later_layer_replaces_whole_rule(monkeypatch, tmp_path: Path):
    user = tmp_path / "user.yaml"
    repo = tmp_path / "repo"
    _write(
        user,
        """
version: 2
skills:
  rules:
    - id: shared
      provider: claude
      skill: test.skill
      outcome: irrelevant
      task_ids: [TASK-1]
      reason_code: user-rule
""",
    )
    _write(
        repo / policy_config.REPO_CONFIG_RELATIVE,
        """
version: 2
skills:
  rules:
    - id: shared
      provider: any
      skill: test.skill
      outcome: required
""",
    )
    monkeypatch.setattr(policy_config, "USER_CONFIG_PATH", user)

    policy = policy_config.load(repo)

    assert len(policy.skill_rules) == 1
    assert policy.skill_rules[0].task_ids == ()
    assert policy.skill_rules[0].reason_code is None
    assert classify_skill(policy, provider="codex", skill="test.skill").outcome == "required"


def test_disabled_rule_does_not_classify(monkeypatch, tmp_path: Path):
    user = tmp_path / "user.yaml"
    _write(
        user,
        """
version: 2
skills:
  rules:
    - id: disabled
      enabled: false
      provider: any
      skill: test.skill
      outcome: irrelevant
""",
    )
    monkeypatch.setattr(policy_config, "USER_CONFIG_PATH", user)

    result = classify_skill(policy_config.load(tmp_path), provider="codex", skill="test.skill")

    assert result.outcome == "required"
    assert result.rule_ids == ()


def test_required_precedes_irrelevant(monkeypatch, tmp_path: Path):
    user = tmp_path / "user.yaml"
    _write(
        user,
        """
version: 2
skills:
  rules:
    - id: broad
      provider: any
      skill: test.skill
      outcome: irrelevant
    - id: codex-required
      provider: codex
      skill: test.skill
      outcome: required
""",
    )
    monkeypatch.setattr(policy_config, "USER_CONFIG_PATH", user)

    policy = policy_config.load(tmp_path)

    assert classify_skill(policy, provider="claude", skill="test.skill").outcome == "irrelevant"
    assert classify_skill(policy, provider="codex", skill="test.skill").outcome == "required"
    assert skill_rule_conflicts(policy) == (("broad", "codex-required"),)


@pytest.mark.parametrize(
    ("content", "code", "path"),
    [
        ("version: 3\n", "POLICY_UNSUPPORTED_VERSION", "version"),
        (
            "version: 2\nskills:\n  rules:\n    - id: x\n      provider: any\n      skill: x\n"
            "      outcome: maybe\n",
            "POLICY_INVALID_VALUE",
            "skills.rules[0].outcome",
        ),
        (
            "version: 2\nskills:\n  rules:\n    - id: x\n      provider: any\n      skill: x\n"
            "      outcome: required\n      surprise: true\n",
            "POLICY_UNKNOWN_FIELD",
            "skills.rules[0].surprise",
        ),
        (
            "version: 2\nskills:\n  rules:\n    - id: x\n      provider: any\n      skill: x\n"
            "      outcome: required\n    - id: x\n      provider: any\n      skill: y\n"
            "      outcome: irrelevant\n",
            "POLICY_DUPLICATE_RULE_ID",
            "skills.rules[1].id",
        ),
    ],
)
def test_v2_validation_has_stable_code_and_path(
    monkeypatch, tmp_path: Path, content: str, code: str, path: str
):
    user = tmp_path / "user.yaml"
    _write(user, content)
    monkeypatch.setattr(policy_config, "USER_CONFIG_PATH", user)

    with pytest.raises(PolicyError) as error:
        policy_config.load(tmp_path)

    assert code in str(error.value)
    assert path in str(error.value)


def test_v1_policy_remains_compatible(monkeypatch, tmp_path: Path):
    user = tmp_path / "missing-user.yaml"
    monkeypatch.setattr(policy_config, "USER_CONFIG_PATH", user)
    _write(
        tmp_path / policy_config.REPO_CONFIG_RELATIVE,
        "version: 1\nmode: enforce\nfiles:\n  max_full_read_bytes: 123\n",
    )

    policy = policy_config.load(tmp_path)

    assert policy.version == 1
    assert policy.mode == "enforce"
    assert policy.files["max_full_read_bytes"] == 123
    assert policy.skill_rules == ()
