"""Local filesystem artifact store: the durable full-evidence record behind every compact result."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ARTIFACTS_DIR = Path(".context-guard") / "artifacts"


class ArtifactNotFoundError(LookupError):
    pass


class FragmentNotFoundError(LookupError):
    pass


@dataclass
class StoredArtifact:
    artifact_id: str
    kind: str
    files: dict[str, bytes]
    meta: dict[str, Any]


def _kind_dir(repo_root: Path, kind: str) -> Path:
    return repo_root / ARTIFACTS_DIR / kind


def _artifact_dir(repo_root: Path, kind: str, artifact_id: str) -> Path:
    return _kind_dir(repo_root, kind) / artifact_id


def reference(artifact_id: str) -> str:
    return f"artifact:{artifact_id}"


def fragment_reference(artifact_id: str, fragment_id: str) -> str:
    return f"artifact:{artifact_id}#{fragment_id}"


def allocate(repo_root: Path, kind: str) -> str:
    """Allocate the next sequential artifact id for `kind`, e.g. "test-018"."""
    kind_dir = _kind_dir(repo_root, kind)
    kind_dir.mkdir(parents=True, exist_ok=True)
    existing = [p.name for p in kind_dir.iterdir() if p.is_dir()]
    max_seq = 0
    prefix = f"{kind}-"
    for name in existing:
        if name.startswith(prefix):
            try:
                max_seq = max(max_seq, int(name[len(prefix):]))
            except ValueError:
                continue
    return f"{prefix}{max_seq + 1:03d}"


def write(
    repo_root: Path,
    kind: str,
    artifact_id: str,
    files: dict[str, bytes],
    fragments: dict[str, dict[str, Any]] | None = None,
) -> None:
    """Write the given files (and optional fragment index) into the artifact directory."""
    directory = _artifact_dir(repo_root, kind, artifact_id)
    directory.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (directory / name).write_bytes(content)
    if fragments is not None:
        (directory / "fragments.json").write_text(json.dumps(fragments), encoding="utf-8")


def _find_artifact_dir(repo_root: Path, artifact_id: str) -> Path:
    kind = artifact_id.rsplit("-", 1)[0]
    directory = _artifact_dir(repo_root, kind, artifact_id)
    if not directory.is_dir():
        raise ArtifactNotFoundError(artifact_id)
    return directory


def read_full(repo_root: Path, artifact_id: str) -> dict[str, Any]:
    """Return every stored file's content plus meta.json for the given artifact id."""
    directory = _find_artifact_dir(repo_root, artifact_id)
    files: dict[str, bytes] = {}
    for path in directory.iterdir():
        if path.is_file():
            files[path.name] = path.read_bytes()
    meta = {}
    if "meta.json" in files:
        meta = json.loads(files["meta.json"].decode("utf-8"))
    return {"files": files, "meta": meta}


def read_fragment(repo_root: Path, artifact_id: str, fragment_id: str) -> str:
    """Return the exact fragment text referenced by `fragment_id` for the given artifact.

    A fragment spec is either {"content": str} (the extracted text, stored inline
    because the parser already isolated it precisely) or {"file", "start", "end"}
    (a byte range within a stored file, used for whole-file previews).
    """
    directory = _find_artifact_dir(repo_root, artifact_id)
    fragments_path = directory / "fragments.json"
    if not fragments_path.is_file():
        raise FragmentNotFoundError(fragment_id)
    fragments = json.loads(fragments_path.read_text(encoding="utf-8"))
    if fragment_id not in fragments:
        raise FragmentNotFoundError(fragment_id)
    spec = fragments[fragment_id]
    if "content" in spec:
        return spec["content"]
    source_path = directory / spec["file"]
    if not source_path.is_file():
        raise FragmentNotFoundError(fragment_id)
    content = source_path.read_bytes()
    start = spec.get("start", 0)
    end = spec.get("end", len(content))
    return content[start:end].decode("utf-8", errors="replace")
