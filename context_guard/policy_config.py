"""Layered policy configuration loading and merging.

Precedence (later wins, field-by-field): built-in defaults -> user config ->
repo config -> environment overrides.
"""

from __future__ import annotations

import copy
import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULTS_PATH = Path(__file__).parent / "defaults" / "policy.yaml"
USER_CONFIG_PATH = Path.home() / ".config" / "context-guard" / "policy.yaml"
REPO_CONFIG_RELATIVE = Path(".context-guard") / "policy.yaml"

_VALID_MODES = {"observe", "warn", "enforce"}
_VALID_POLICY_VERSIONS = {1, 2}
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
    version: int = 1
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
    """Raised when a policy YAML layer is structurally invalid."""


def new_v2_policy_data() -> dict[str, Any]:
    """Return new-install policy data without changing the built-in v1 defaults."""
    data = _read_yaml_layer(DEFAULTS_PATH)
    data["version"] = 2
    data["skills"] = {"rules": []}
    return data


def write_new_v2_policy(path: Path) -> None:
    """Create a v2 policy without overwriting an existing path."""
    data = new_v2_policy_data()
    errors = validate_policy_dict(data, str(path))
    if errors:
        raise PolicyError("; ".join(errors))
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            yaml.safe_dump(data, stream, sort_keys=False)
    except FileExistsError as exc:
        raise PolicyError(
            f"POLICY_ALREADY_EXISTS at {path}: keep the existing file or migrate it explicitly"
        ) from exc


def migrate_policy_file(path: Path) -> Path | None:
    """Explicitly migrate a v1 policy with a non-overwritten backup and atomic replace."""
    data = _read_yaml_layer(path)
    errors = validate_policy_dict(data, str(path))
    if errors:
        raise PolicyError("; ".join(errors))
    if data.get("version", 1) == 2:
        return None

    migrated = copy.deepcopy(data)
    migrated["version"] = 2
    migrated["skills"] = {"rules": []}
    errors = validate_policy_dict(migrated, str(path))
    if errors:
        raise PolicyError("; ".join(errors))

    original = path.read_bytes()
    backup = path.with_suffix(path.suffix + ".v1.bak")
    backup_temp: Path | None = None
    target_temp: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent, prefix=f".{path.name}.backup-", delete=False
        ) as stream:
            backup_temp = Path(stream.name)
            stream.write(original)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(backup_temp, backup)
        except FileExistsError as exc:
            raise PolicyError(
                f"POLICY_BACKUP_EXISTS at {backup}: remove or archive it before migration"
            ) from exc
        finally:
            backup_temp.unlink(missing_ok=True)
            backup_temp = None

        rendered = yaml.safe_dump(migrated, sort_keys=False)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.migrate-",
            delete=False,
        ) as stream:
            target_temp = Path(stream.name)
            stream.write(rendered)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(target_temp, path.stat().st_mode & 0o777)
        candidate = _read_yaml_layer(target_temp)
        candidate_errors = validate_policy_dict(candidate, str(path))
        if candidate_errors:
            raise PolicyError("; ".join(candidate_errors))
        os.replace(target_temp, path)
        target_temp = None
        return backup
    finally:
        if backup_temp is not None:
            backup_temp.unlink(missing_ok=True)
        if target_temp is not None:
            target_temp.unlink(missing_ok=True)


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


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Merge one policy layer over another, field-by-field, dict-recursive."""
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result


def _merge_policy_layer(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Merge a policy layer, replacing same-id skill rules as whole objects."""
    base_without_skills = {key: value for key, value in base.items() if key != "skills"}
    override_without_skills = {key: value for key, value in override.items() if key != "skills"}
    result = _merge(base_without_skills, override_without_skills)

    ordered: dict[str, dict[str, Any]] = {}
    for source in (base, override):
        skills = source.get("skills", {})
        if not isinstance(skills, dict):
            continue
        rules = skills.get("rules", [])
        if not isinstance(rules, list):
            continue
        for rule in rules:
            if isinstance(rule, dict) and isinstance(rule.get("id"), str):
                ordered[rule["id"]] = copy.deepcopy(rule)
    if ordered or "skills" in base or "skills" in override:
        result["skills"] = {"rules": list(ordered.values())}
    return result


def _env_overrides() -> dict[str, Any]:
    overrides: dict[str, Any] = {}
    mode = os.environ.get("CONTEXT_GUARD_MODE")
    if mode:
        overrides["mode"] = mode
    return overrides


def validate_policy_dict(data: dict[str, Any], source: str = "<policy>") -> list[str]:
    """Return a list of schema errors for a merged policy dict, empty when valid."""
    errors: list[str] = []
    version = data.get("version", 1)
    if not isinstance(version, int) or isinstance(version, bool):
        errors.append(f"POLICY_INVALID_TYPE at {source}:version: version must be an integer")
    elif version not in _VALID_POLICY_VERSIONS:
        errors.append(
            f"POLICY_UNSUPPORTED_VERSION at {source}:version: use version 1 or 2"
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
    """Load and merge all policy layers into a validated Policy object.

    Raises PolicyError when any layer is structurally invalid or the merged
    result fails schema validation.
    """
    repo_root = repo_root or Path.cwd()
    layers: list[tuple[str, Path]] = [
        ("defaults", DEFAULTS_PATH),
        ("user", USER_CONFIG_PATH),
        ("repo", repo_root / REPO_CONFIG_RELATIVE),
    ]

    merged: dict[str, Any] = {}
    sources: list[str] = []
    for name, path in layers:
        layer_data = _read_yaml_layer(path)
        if layer_data:
            sources.append(f"{name}:{path}")
        layer_errors = validate_policy_dict(layer_data, str(path))
        # Partial override layers inherit version from earlier layers.
        layer_errors = [
            error
            for error in layer_errors
            if not ("POLICY_REQUIRES_V2" in error and "version" not in layer_data)
        ]
        if layer_errors:
            raise PolicyError("; ".join(layer_errors))
        merged = _merge_policy_layer(merged, layer_data)

    env = _env_overrides()
    if env:
        sources.append("env")
        merged = _merge_policy_layer(merged, env)

    errors = validate_policy_dict(merged, "effective")
    if errors:
        raise PolicyError("; ".join(errors))

    return Policy(
        version=merged.get("version", 1),
        mode=merged.get("mode", "observe"),
        files=merged.get("files", {}),
        commands=merged.get("commands", {}),
        search=merged.get("search", {}),
        fail_closed_rules=list(merged.get("fail_closed_rules", [])),
        skill_rules=_skill_rules(merged),
        sources=sources,
    )
