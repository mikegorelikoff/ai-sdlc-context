"""Load and validate Context Guard's single packaged policy."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULTS_PATH = Path(__file__).parent / "defaults" / "policy.yaml"

_VALID_MODES = {"observe", "warn", "enforce"}
_VALID_POLICY_VERSIONS = {2}
_VALID_PROVIDERS = {"claude", "codex", "any"}
_VALID_OUTCOMES = {"safety-critical", "required", "irrelevant"}
_OUTCOME_PRECEDENCE = {"irrelevant": 0, "required": 1, "safety-critical": 2}
_SKILL_RULE_FIELDS = {
    "id",
    "enabled",
    "provider",
    "skill",
    "outcome",
    "task_ids",
    "repositories",
    "reason_code",
}


@dataclass(frozen=True)
class SkillRule:
    id: str
    provider: str
    skill: str
    outcome: str
    enabled: bool = True
    task_ids: tuple[str, ...] = ()
    repositories: tuple[str, ...] = ()
    reason_code: str | None = None


@dataclass(frozen=True)
class RelevanceResult:
    outcome: str
    reason_code: str
    rule_ids: tuple[str, ...] = ()


@dataclass
class Policy:
    version: int = 2
    mode: str = "observe"
    files: dict[str, Any] = field(default_factory=dict)
    commands: dict[str, Any] = field(default_factory=dict)
    search: dict[str, Any] = field(default_factory=dict)
    fail_closed_rules: list[str] = field(default_factory=list)
    skill_rules: tuple[SkillRule, ...] = ()
    sources: list[str] = field(default_factory=list)

    def mode_for(self, group: str) -> str:
        """Return the effective mode for a rule group, falling back to the global mode."""
        group_cfg = getattr(self, group, {}) or {}
        return group_cfg.get("mode", self.mode)


class PolicyError(ValueError):
    """Raised when the packaged policy is missing or invalid."""


def _read_yaml_layer(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PolicyError(
            f"POLICY_READ_ERROR at {path}: could not read file; check permissions ({exc})"
        ) from exc
    try:
        data = yaml.safe_load(text) or {}
    except yaml.YAMLError as exc:
        raise PolicyError(
            f"POLICY_INVALID_YAML at {path}: fix the YAML syntax ({exc})"
        ) from exc
    if not isinstance(data, dict):
        raise PolicyError(
            f"POLICY_INVALID_TYPE at {path}: policy must contain a top-level mapping"
        )
    return data


def validate_policy_dict(data: dict[str, Any], source: str = "<policy>") -> list[str]:
    """Return a list of schema errors for a merged policy dict, empty when valid."""
    errors: list[str] = []
    version = data.get("version", 1)
    if not isinstance(version, int) or isinstance(version, bool):
        errors.append(f"POLICY_INVALID_TYPE at {source}:version: version must be an integer")
    elif version not in _VALID_POLICY_VERSIONS:
        errors.append(
            f"POLICY_UNSUPPORTED_VERSION at {source}:version: use version 2"
        )

    mode = data.get("mode", "observe")
    if mode not in _VALID_MODES:
        errors.append(
            f"POLICY_INVALID_VALUE at {source}:mode: must be one of {sorted(_VALID_MODES)}"
        )

    files = data.get("files", {})
    if not isinstance(files, dict):
        errors.append(f"POLICY_INVALID_TYPE at {source}:files: must be a mapping")
    else:
        for key in ("max_full_read_bytes", "require_range_above_bytes"):
            if key in files and not isinstance(files[key], int):
                errors.append(
                    f"POLICY_INVALID_TYPE at {source}:files.{key}: must be an integer"
                )
        if "deny" in files and not isinstance(files["deny"], list):
            errors.append(
                f"POLICY_INVALID_TYPE at {source}:files.deny: must be a list"
            )

    commands = data.get("commands", {})
    if not isinstance(commands, dict):
        errors.append(f"POLICY_INVALID_TYPE at {source}:commands: must be a mapping")
    elif "require_bounds" in commands and not isinstance(commands["require_bounds"], list):
        errors.append(
            f"POLICY_INVALID_TYPE at {source}:commands.require_bounds: must be a list"
        )

    search = data.get("search", {})
    if not isinstance(search, dict):
        errors.append(f"POLICY_INVALID_TYPE at {source}:search: must be a mapping")
    else:
        if "require_path_scope" in search and not isinstance(search["require_path_scope"], bool):
            errors.append(
                f"POLICY_INVALID_TYPE at {source}:search.require_path_scope: must be a boolean"
            )
        if "maximum_results" in search and not isinstance(search["maximum_results"], int):
            errors.append(
                f"POLICY_INVALID_TYPE at {source}:search.maximum_results: must be an integer"
            )

    fail_closed = data.get("fail_closed_rules", [])
    if not isinstance(fail_closed, list):
        errors.append(
            f"POLICY_INVALID_TYPE at {source}:fail_closed_rules: must be a list"
        )

    skills = data.get("skills")
    if skills is not None:
        if version != 2:
            errors.append(
                f"POLICY_REQUIRES_V2 at {source}:skills: set version: 2 to use skills.rules"
            )
        if not isinstance(skills, dict):
            errors.append(f"POLICY_INVALID_TYPE at {source}:skills: must be a mapping")
        else:
            unknown_skill_fields = set(skills) - {"rules"}
            for key in sorted(unknown_skill_fields):
                errors.append(
                    f"POLICY_UNKNOWN_FIELD at {source}:skills.{key}: remove the unknown field"
                )
            rules = skills.get("rules", [])
            if not isinstance(rules, list):
                errors.append(
                    f"POLICY_INVALID_TYPE at {source}:skills.rules: must be a list"
                )
            else:
                seen: set[str] = set()
                for index, rule in enumerate(rules):
                    path = f"{source}:skills.rules[{index}]"
                    if not isinstance(rule, dict):
                        errors.append(f"POLICY_INVALID_TYPE at {path}: must be a mapping")
                        continue
                    for key in sorted(set(rule) - _SKILL_RULE_FIELDS):
                        errors.append(
                            f"POLICY_UNKNOWN_FIELD at {path}.{key}: remove the unknown field"
                        )
                    rule_id = rule.get("id")
                    if not isinstance(rule_id, str) or not rule_id:
                        errors.append(
                            f"POLICY_REQUIRED_FIELD at {path}.id: provide a non-empty string"
                        )
                    elif rule_id in seen:
                        errors.append(
                            f"POLICY_DUPLICATE_RULE_ID at {path}.id: use a unique id within this layer"
                        )
                    else:
                        seen.add(rule_id)
                    _validate_enum(errors, rule, "provider", _VALID_PROVIDERS, path)
                    _validate_string(errors, rule, "skill", path, required=True)
                    _validate_enum(errors, rule, "outcome", _VALID_OUTCOMES, path)
                    if "enabled" in rule and not isinstance(rule["enabled"], bool):
                        errors.append(
                            f"POLICY_INVALID_TYPE at {path}.enabled: must be a boolean"
                        )
                    for key in ("task_ids", "repositories"):
                        if key in rule and (
                            not isinstance(rule[key], list)
                            or not all(isinstance(item, str) and item for item in rule[key])
                        ):
                            errors.append(
                                f"POLICY_INVALID_TYPE at {path}.{key}: must be a list of non-empty strings"
                            )
                    _validate_string(errors, rule, "reason_code", path, required=False)

    return errors


def _validate_enum(
    errors: list[str],
    rule: dict[str, Any],
    key: str,
    allowed: set[str],
    path: str,
) -> None:
    value = rule.get(key)
    if value not in allowed:
        errors.append(
            f"POLICY_INVALID_VALUE at {path}.{key}: must be one of {sorted(allowed)}"
        )


def _validate_string(
    errors: list[str],
    rule: dict[str, Any],
    key: str,
    path: str,
    *,
    required: bool,
) -> None:
    if key not in rule and not required:
        return
    value = rule.get(key)
    if not isinstance(value, str) or not value:
        errors.append(
            f"POLICY_REQUIRED_FIELD at {path}.{key}: provide a non-empty string"
        )


def _skill_rules(data: dict[str, Any]) -> tuple[SkillRule, ...]:
    rules = data.get("skills", {}).get("rules", [])
    return tuple(
        SkillRule(
            id=rule["id"],
            enabled=rule.get("enabled", True),
            provider=rule["provider"],
            skill=rule["skill"],
            outcome=rule["outcome"],
            task_ids=tuple(rule.get("task_ids", [])),
            repositories=tuple(rule.get("repositories", [])),
            reason_code=rule.get("reason_code"),
        )
        for rule in rules
    )


def classify_skill(
    policy: Policy,
    *,
    provider: str,
    skill: str,
    task_id: str | None = None,
    repository: str | None = None,
) -> RelevanceResult:
    """Classify an exact authoritative skill identity using conservative precedence."""
    matches = [
        rule
        for rule in policy.skill_rules
        if rule.enabled
        and rule.skill == skill
        and rule.provider in ("any", provider)
        and (not rule.task_ids or task_id in rule.task_ids)
        and (not rule.repositories or repository in rule.repositories)
    ]
    if not matches:
        return RelevanceResult("required", "no-exact-irrelevant-match")
    outcome = max((rule.outcome for rule in matches), key=_OUTCOME_PRECEDENCE.__getitem__)
    selected = tuple(rule.id for rule in matches if rule.outcome == outcome)
    reason = next(
        (rule.reason_code for rule in matches if rule.outcome == outcome and rule.reason_code),
        f"policy-{outcome}",
    )
    return RelevanceResult(outcome, reason, selected)


def skill_rule_conflicts(policy: Policy) -> tuple[tuple[str, str], ...]:
    """Return potentially conflicting enabled rule-id pairs without exposing content."""
    conflicts: list[tuple[str, str]] = []
    enabled = [rule for rule in policy.skill_rules if rule.enabled]
    for index, left in enumerate(enabled):
        for right in enabled[index + 1 :]:
            providers_overlap = (
                left.provider == right.provider
                or left.provider == "any"
                or right.provider == "any"
            )
            if (
                left.skill == right.skill
                and providers_overlap
                and left.outcome != right.outcome
            ):
                conflicts.append((left.id, right.id))
    return tuple(conflicts)


def load(repo_root: Path | None = None) -> Policy:
    """Load the single packaged policy; ``repo_root`` is ignored for API compatibility."""
    del repo_root
    data = _read_yaml_layer(DEFAULTS_PATH)
    errors = validate_policy_dict(data, str(DEFAULTS_PATH))
    if errors:
        raise PolicyError("; ".join(errors))

    return Policy(
        version=data["version"],
        mode=data.get("mode", "observe"),
        files=data.get("files", {}),
        commands=data.get("commands", {}),
        search=data.get("search", {}),
        fail_closed_rules=list(data.get("fail_closed_rules", [])),
        skill_rules=_skill_rules(data),
        sources=[f"packaged:{DEFAULTS_PATH}"],
    )
