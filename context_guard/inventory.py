"""Read-only provider preflight and authoritative local skill inventory."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

import yaml

_VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
_SUPPORTED = {
    "claude": {
        "minimum": (2, 1, 218),
        "surfaces": {"cli"},
        "relative_root": Path(".claude") / "skills",
    },
    "codex": {
        "minimum": (0, 144, 1),
        "surfaces": {"cli", "app-server"},
        "relative_root": Path(".agents") / "skills",
    },
}


@dataclass(frozen=True)
class PreflightResult:
    provider: str
    version: str
    surface: str
    status: str
    reason_code: str


@dataclass(frozen=True)
class SkillRecord:
    provider: str
    scope: str
    name: str
    locator: str
    metadata_digest: str
    body_digest: str
    identity: str


@dataclass(frozen=True)
class InventoryResult:
    provider: str
    version: str
    surface: str
    status: str
    reason_code: str
    records: tuple[SkillRecord, ...] = ()
    fingerprint: str | None = None

    def to_dict(self) -> dict[str, object]:
        value = asdict(self)
        value["records"] = [asdict(record) for record in self.records]
        return value


class InventoryError(ValueError):
    """Internal inventory evidence was missing, ambiguous, or unreadable."""

    def __init__(self, reason_code: str):
        super().__init__(reason_code)
        self.reason_code = reason_code


def preflight(provider: str, version: str, surface: str) -> PreflightResult:
    contract = _SUPPORTED.get(provider)
    if contract is None:
        return PreflightResult(provider, version, surface, "unsupported", "unsupported-provider")
    match = _VERSION.fullmatch(version)
    if match is None:
        return PreflightResult(provider, version, surface, "unsupported", "invalid-version")
    parsed = tuple(int(part) for part in match.groups())
    if parsed < contract["minimum"]:
        return PreflightResult(provider, version, surface, "unsupported", "unsupported-version")
    if surface not in contract["surfaces"]:
        return PreflightResult(provider, version, surface, "unsupported", "unsupported-surface")
    return PreflightResult(provider, version, surface, "supported", "supported")


def read_inventory(
    home: Path,
    *,
    provider: str,
    version: str,
    surface: str,
    between_reads: Callable[[], None] | None = None,
) -> InventoryResult:
    """Preflight and read the authoritative inventory twice for stability."""
    eligibility = preflight(provider, version, surface)
    if eligibility.status != "supported":
        return InventoryResult(
            provider, version, surface, "unsupported", eligibility.reason_code
        )

    root = home / _SUPPORTED[provider]["relative_root"]
    try:
        first = _scan(root, provider)
        if between_reads is not None:
            between_reads()
        second = _scan(root, provider)
    except InventoryError as exc:
        return InventoryResult(provider, version, surface, "uncertain", exc.reason_code)

    if first != second:
        return InventoryResult(provider, version, surface, "uncertain", "stale-inventory")
    fingerprint = _fingerprint(first)
    return InventoryResult(
        provider,
        version,
        surface,
        "supported",
        "stable-inventory",
        first,
        fingerprint,
    )


def _scan(root: Path, provider: str) -> tuple[SkillRecord, ...]:
    if not root.exists():
        return ()
    if not root.is_dir():
        raise InventoryError("invalid-inventory-root")
    try:
        files = sorted(
            root.glob("*/SKILL.md"),
            key=lambda item: str(item.resolve()),
        )
    except OSError as exc:
        raise InventoryError("inventory-list-error") from exc

    records: list[SkillRecord] = []
    names: set[str] = set()
    for path in files:
        record = _read_skill(path, provider)
        if record.name in names:
            raise InventoryError("duplicate-skill-name")
        names.add(record.name)
        records.append(record)
    return tuple(records)


def _read_skill(path: Path, provider: str) -> SkillRecord:
    try:
        raw = path.read_bytes()
        locator = str(path.resolve(strict=True))
    except OSError as exc:
        raise InventoryError("skill-read-error") from exc

    if not raw.startswith(b"---\n"):
        raise InventoryError("missing-skill-frontmatter")
    boundary = raw.find(b"\n---\n", 4)
    if boundary < 0:
        raise InventoryError("invalid-skill-frontmatter")
    metadata_bytes = raw[4:boundary]
    body = raw[boundary + len(b"\n---\n") :]
    try:
        metadata = yaml.safe_load(metadata_bytes.decode("utf-8")) or {}
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise InventoryError("invalid-skill-frontmatter") from exc
    if not isinstance(metadata, dict):
        raise InventoryError("invalid-skill-frontmatter")
    name = metadata.get("name")
    if not isinstance(name, str) or not name.strip():
        raise InventoryError("missing-skill-name")
    normalized_name = name.strip()
    metadata_canonical = json.dumps(
        metadata, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    metadata_digest = hashlib.sha256(metadata_canonical).hexdigest()
    body_digest = hashlib.sha256(body).hexdigest()
    identity = f"{provider}:user:{normalized_name}:{locator}"
    return SkillRecord(
        provider=provider,
        scope="user",
        name=normalized_name,
        locator=locator,
        metadata_digest=metadata_digest,
        body_digest=body_digest,
        identity=identity,
    )


def _fingerprint(records: tuple[SkillRecord, ...]) -> str:
    evidence = [
        {
            "provider": record.provider,
            "scope": record.scope,
            "name": record.name,
            "locator": record.locator,
            "metadata_digest": record.metadata_digest,
            "body_digest": record.body_digest,
            "identity": record.identity,
        }
        for record in records
    ]
    canonical = json.dumps(
        evidence, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()
