"""Layered policy configuration loading and merging.

Precedence (later wins, field-by-field): built-in defaults -> user config ->
repo config -> environment overrides.
"""

from __future__ import annotations

import copy
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULTS_PATH = Path(__file__).parent / "defaults" / "policy.yaml"
USER_CONFIG_PATH = Path.home() / ".config" / "context-guard" / "policy.yaml"
REPO_CONFIG_RELATIVE = Path(".context-guard") / "policy.yaml"

_VALID_MODES = {"observe", "warn", "enforce"}


@dataclass
class Policy:
    mode: str = "observe"
    files: dict[str, Any] = field(default_factory=dict)
    commands: dict[str, Any] = field(default_factory=dict)
    search: dict[str, Any] = field(default_factory=dict)
    fail_closed_rules: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)

    def mode_for(self, group: str) -> str:
        """Return the effective mode for a rule group, falling back to the global mode."""
        group_cfg = getattr(self, group, {}) or {}
        return group_cfg.get("mode", self.mode)


class PolicyError(ValueError):
    """Raised when a policy YAML layer is structurally invalid."""


def _read_yaml_layer(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PolicyError(f"could not read policy file {path}: {exc}") from exc
    try:
        data = yaml.safe_load(text) or {}
    except yaml.YAMLError as exc:
        raise PolicyError(f"invalid YAML in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise PolicyError(f"policy file {path} must contain a mapping at the top level")
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


def _env_overrides() -> dict[str, Any]:
    overrides: dict[str, Any] = {}
    mode = os.environ.get("CONTEXT_GUARD_MODE")
    if mode:
        overrides["mode"] = mode
    return overrides


def validate_policy_dict(data: dict[str, Any]) -> list[str]:
    """Return a list of schema errors for a merged policy dict, empty when valid."""
    errors: list[str] = []
    mode = data.get("mode", "observe")
    if mode not in _VALID_MODES:
        errors.append(f"mode must be one of {sorted(_VALID_MODES)}, got {mode!r}")

    files = data.get("files", {})
    if not isinstance(files, dict):
        errors.append("files must be a mapping")
    else:
        for key in ("max_full_read_bytes", "require_range_above_bytes"):
            if key in files and not isinstance(files[key], int):
                errors.append(f"files.{key} must be an integer")
        if "deny" in files and not isinstance(files["deny"], list):
            errors.append("files.deny must be a list")

    commands = data.get("commands", {})
    if not isinstance(commands, dict):
        errors.append("commands must be a mapping")
    elif "require_bounds" in commands and not isinstance(commands["require_bounds"], list):
        errors.append("commands.require_bounds must be a list")

    search = data.get("search", {})
    if not isinstance(search, dict):
        errors.append("search must be a mapping")
    else:
        if "require_path_scope" in search and not isinstance(search["require_path_scope"], bool):
            errors.append("search.require_path_scope must be a boolean")
        if "maximum_results" in search and not isinstance(search["maximum_results"], int):
            errors.append("search.maximum_results must be an integer")

    fail_closed = data.get("fail_closed_rules", [])
    if not isinstance(fail_closed, list):
        errors.append("fail_closed_rules must be a list")

    return errors


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
        merged = _merge(merged, layer_data)

    env = _env_overrides()
    if env:
        sources.append("env")
        merged = _merge(merged, env)

    errors = validate_policy_dict(merged)
    if errors:
        raise PolicyError("; ".join(errors))

    return Policy(
        mode=merged.get("mode", "observe"),
        files=merged.get("files", {}),
        commands=merged.get("commands", {}),
        search=merged.get("search", {}),
        fail_closed_rules=list(merged.get("fail_closed_rules", [])),
        sources=sources,
    )
