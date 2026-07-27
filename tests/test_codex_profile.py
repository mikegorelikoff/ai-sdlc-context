from __future__ import annotations

import json
from pathlib import Path

import pytest

from context_guard import codex_profile, inventory, receipts


def _apply(repo: Path, home: Path, run_id: str, **overrides):
    for name in ("unused", "needed"):
        skill = home / ".agents" / "skills" / name / "SKILL.md"
        skill.parent.mkdir(parents=True, exist_ok=True)
        skill.write_text(f"---\nname: {name}\n---\nbody\n", encoding="utf-8")
    fingerprint = inventory.read_inventory(
        home, provider="codex", version="0.144.1", surface="cli"
    ).fingerprint
    values = {
        "profile": "context-guard",
        "run_id": run_id,
        "version": "0.144.1",
        "surface": "cli",
        "classifications": {"unused": "irrelevant", "needed": "required"},
        "skill_paths": {
            "unused": home / ".agents" / "skills" / "unused" / "SKILL.md",
            "needed": home / ".agents" / "skills" / "needed" / "SKILL.md",
        },
        "inventory_fingerprint": fingerprint,
    }
    values.update(overrides)
    return codex_profile.apply_profile(repo, home, **values)


def test_plan_disables_only_irrelevant_non_explicit_absolute_paths(tmp_path: Path):
    paths = {
        "a": tmp_path / ".agents" / "skills" / "a" / "SKILL.md",
        "b": tmp_path / ".agents" / "skills" / "b" / "SKILL.md",
        "c": tmp_path / ".agents" / "skills" / "c" / "SKILL.md",
    }
    result = codex_profile.plan_disabled_paths(
        {"a": "irrelevant", "b": "required", "c": "irrelevant"},
        paths,
        explicit_invocations=["c"],
    )
    assert result == (paths["a"],)


def test_apply_writes_only_sorted_disable_entries_and_sanitized_receipt(tmp_path: Path):
    home = tmp_path / "home"
    result = _apply(tmp_path, home, "apply")
    profile = home / ".codex" / "context-guard.config.toml"

    assert result.status == "reduced"
    assert result.fresh_process_required is True
    assert result.disabled_count == 1
    assert profile.read_text(encoding="utf-8") == (
        "[[skills.config]]\n"
        f'path = "{home / ".agents" / "skills" / "unused" / "SKILL.md"}"\n'
        "enabled = false\n"
    )
    assert not (home / ".codex" / "config.toml").exists()
    serialized = json.dumps(receipts.inspect_receipt(tmp_path, "apply"))
    assert str(home) not in serialized
    status = codex_profile.profile_status(tmp_path, home, "context-guard")
    assert status["selector"] == ["--profile", "context-guard"]
    assert status["leased"] is True


def test_apply_requires_supported_preflight_and_inventory(tmp_path: Path):
    home = tmp_path / "home"
    unsupported = _apply(tmp_path, home, "old", version="0.144.0")
    missing = _apply(tmp_path, home, "missing", inventory_fingerprint=None)

    assert unsupported.reason_code == "unsupported-version"
    assert missing.reason_code == "missing-inventory-fingerprint"
    assert not (home / ".codex" / "context-guard.config.toml").exists()


def test_apply_rejects_stale_fingerprint_and_non_inventory_path(tmp_path: Path):
    home = tmp_path / "home"
    stale = _apply(tmp_path, home, "stale", inventory_fingerprint="stale")
    outside = _apply(
        tmp_path,
        home,
        "outside",
        skill_paths={
            "unused": tmp_path / "outside" / "SKILL.md",
            "needed": home / ".agents" / "skills" / "needed" / "SKILL.md",
        },
    )
    assert stale.reason_code == "inventory-fingerprint-mismatch"
    assert outside.reason_code == "inventory-correlation-mismatch"
    assert not (home / ".codex" / "context-guard.config.toml").exists()


def test_live_contention_does_not_mutate(tmp_path: Path):
    home = tmp_path / "home"
    first = _apply(tmp_path, home, "owner")
    path = home / ".codex" / "context-guard.config.toml"
    guarded = path.read_bytes()
    second = _apply(tmp_path, home, "contender")

    assert first.status == "reduced"
    assert second.reason_code == "lease-contention"
    assert path.read_bytes() == guarded


def test_restore_is_byte_exact_and_idempotent(tmp_path: Path):
    home = tmp_path / "home"
    path = home / ".codex" / "context-guard.config.toml"
    path.parent.mkdir(parents=True)
    baseline = b'model = "gpt-test"\n'
    path.write_bytes(baseline)
    _apply(tmp_path, home, "apply-existing")

    restored = codex_profile.restore_profile(
        tmp_path, home, profile="context-guard", run_id="restore",
        version="0.144.1"
    )
    repeated = codex_profile.restore_profile(
        tmp_path, home, profile="context-guard", run_id="repeat",
        version="0.144.1"
    )
    assert restored.status == "restored"
    assert path.read_bytes() == baseline
    assert repeated.reason_code == "already-restored"


def test_restore_preserves_user_edit_and_disables(tmp_path: Path):
    home = tmp_path / "home"
    _apply(tmp_path, home, "apply-edit")
    path = home / ".codex" / "context-guard.config.toml"
    path.write_text('model = "user-edit"\n', encoding="utf-8")

    result = codex_profile.restore_profile(
        tmp_path, home, profile="context-guard", run_id="restore-edit",
        version="0.144.1"
    )
    assert result.reason_code == "user-edit-detected"
    assert path.read_text(encoding="utf-8") == 'model = "user-edit"\n'
    assert codex_profile.profile_status(
        tmp_path, home, "context-guard"
    )["disabled"] is True


def test_dead_owner_recovery_restores_unchanged_state(tmp_path: Path):
    home = tmp_path / "home"
    _apply(tmp_path, home, "dead", pid=99_999_999)
    path = home / ".codex" / "context-guard.config.toml"

    result = codex_profile.recover_profile(
        tmp_path, home, profile="context-guard", run_id="recover",
        version="0.144.1", liveness=lambda _pid: False
    )
    assert result.status == "restored"
    assert not path.exists()


def test_verification_mismatch_preserves_external_edit(tmp_path: Path):
    home = tmp_path / "home"

    def edit(path: Path) -> None:
        path.write_text('model = "external"\n', encoding="utf-8")

    result = _apply(tmp_path, home, "mismatch", verify_hook=edit)
    path = home / ".codex" / "context-guard.config.toml"
    assert result.reason_code == "actual-state-mismatch"
    assert path.read_text(encoding="utf-8") == 'model = "external"\n'
    assert codex_profile.profile_status(
        tmp_path, home, "context-guard"
    )["disabled"] is True


def test_profile_rejects_symlinked_private_state_root(tmp_path: Path):
    home = tmp_path / "home"
    outside = tmp_path / "outside"
    outside.mkdir()
    (tmp_path / ".context-guard").symlink_to(outside, target_is_directory=True)

    with pytest.raises(codex_profile.CodexProfileError, match="unsafe private"):
        _apply(tmp_path, home, "symlinked")

    assert not (outside / "profiles").exists()
