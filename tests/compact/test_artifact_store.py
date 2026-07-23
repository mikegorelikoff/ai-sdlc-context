from pathlib import Path

import pytest

from context_guard.compact import artifact_store


def test_allocate_returns_sequential_ids(tmp_path: Path):
    first = artifact_store.allocate(tmp_path, "test")
    artifact_store.write(tmp_path, "test", first, {"stdout.txt": b"a"})
    second = artifact_store.allocate(tmp_path, "test")
    assert first == "test-001"
    assert second == "test-002"


def test_write_and_read_full_round_trip(tmp_path: Path):
    artifact_id = artifact_store.allocate(tmp_path, "test")
    artifact_store.write(tmp_path, "test", artifact_id, {"stdout.txt": b"hello", "stderr.txt": b""})
    full = artifact_store.read_full(tmp_path, artifact_id)
    assert full["files"]["stdout.txt"] == b"hello"


def test_read_fragment_with_inline_content(tmp_path: Path):
    artifact_id = artifact_store.allocate(tmp_path, "test")
    artifact_store.write(
        tmp_path, "test", artifact_id, {"stdout.txt": b"x"}, fragments={"failure-1": {"content": "exact text"}}
    )
    assert artifact_store.read_fragment(tmp_path, artifact_id, "failure-1") == "exact text"


def test_read_fragment_with_byte_range(tmp_path: Path):
    artifact_id = artifact_store.allocate(tmp_path, "test")
    artifact_store.write(
        tmp_path,
        "test",
        artifact_id,
        {"stdout.txt": b"0123456789"},
        fragments={"slice-1": {"file": "stdout.txt", "start": 2, "end": 5}},
    )
    assert artifact_store.read_fragment(tmp_path, artifact_id, "slice-1") == "234"


def test_unknown_artifact_id_raises(tmp_path: Path):
    with pytest.raises(artifact_store.ArtifactNotFoundError):
        artifact_store.read_full(tmp_path, "test-999")


def test_unknown_fragment_id_raises(tmp_path: Path):
    artifact_id = artifact_store.allocate(tmp_path, "test")
    artifact_store.write(tmp_path, "test", artifact_id, {"stdout.txt": b"x"}, fragments={})
    with pytest.raises(artifact_store.FragmentNotFoundError):
        artifact_store.read_fragment(tmp_path, artifact_id, "missing")


def test_reference_and_fragment_reference_format():
    assert artifact_store.reference("test-018") == "artifact:test-018"
    assert artifact_store.fragment_reference("test-018", "failure-1") == "artifact:test-018#failure-1"
