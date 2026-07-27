from __future__ import annotations

import json
import stat
from pathlib import Path

import pytest

from context_guard import claude_profile, receipts


def _apply(
    root: Path,
    settings: Path,
    run_id: str,
    *,
    classifications=None,
    **kwargs,
):
    return claude_profile.apply_profile(
        root,
        settings,
        run_id=run_id,
        version="2.1.218",
        surface="cli",
        classifications=classifications
        or {"unused": "irrelevant", "needed": "required", "unknown": "uncertain"},
        inventory_fingerprint="inventory-fingerprint",
        **kwargs,
    )


def test_plan_only_reduces_exact_irrelevant_and_respects_explicit_invocation():
    planned = claude_profile.plan_overrides(
        {
            "safe": "safety-critical",
            "needed": "required",
            "unused": "irrelevant",
            "manual": "irrelevant",
            "unknown": "uncertain",
        },
        explicit_invocations={"manual"},
    )
    assert planned == {"unused": "user-invocable-only"}


def test_apply_preserves_unrelated_settings_and_records_private_state(tmp_path: Path):
    settings = tmp_path / "home" / ".claude" / "settings.local.json"
    settings.parent.mkdir(parents=True)
    baseline = b'{\n  "model": "sonnet",\n  "permissions": {"allow": ["Read"]}\n}\n'
    settings.write_bytes(baseline)

    result = _apply(tmp_path, settings, "apply-1")

    assert result.status == "reduced"
    assert result.fresh_session_required is True
    actual = json.loads(settings.read_text(encoding="utf-8"))
    assert actual["model"] == "sonnet"
    assert actual["permissions"] == {"allow": ["Read"]}
    assert actual["skillOverrides"] == {"unused": "user-invocable-only"}
    status = claude_profile.profile_status(tmp_path, settings)
    assert status["leased"] is True
    assert status["state_present"] is True
    profile_root = next((tmp_path / ".context-guard" / "profiles" / "claude").iterdir())
    assert stat.S_IMODE(profile_root.stat().st_mode) == 0o700
    assert stat.S_IMODE((profile_root / "state.json").stat().st_mode) == 0o600
    state = json.loads((profile_root / "state.json").read_text(encoding="utf-8"))
    assert "baseline_bytes" in state
    receipt = receipts.inspect_receipt(tmp_path, "apply-1")
    assert receipt["status"] == "reduced"
    assert "sonnet" not in json.dumps(receipt)
    assert str(settings) not in json.dumps(receipt)


def test_bypass_and_unsupported_version_never_mutate(tmp_path: Path):
    settings = tmp_path / "settings.json"
    settings.write_text('{"model":"keep"}\n', encoding="utf-8")
    baseline = settings.read_bytes()

    bypass = _apply(tmp_path, settings, "bypass", bypass=True)
    unsupported = claude_profile.apply_profile(
        tmp_path,
        settings,
        run_id="unsupported",
        version="2.1.217",
        surface="cli",
        classifications={"unused": "irrelevant"},
    )

    assert bypass.reason_code == "bypass"
    assert unsupported.reason_code == "unsupported-version"
    assert settings.read_bytes() == baseline
    assert claude_profile.profile_status(tmp_path, settings)["leased"] is False


def test_missing_stable_inventory_evidence_never_mutates(tmp_path: Path):
    settings = tmp_path / "settings.json"
    result = claude_profile.apply_profile(
        tmp_path,
        settings,
        run_id="missing-inventory",
        version="2.1.218",
        surface="cli",
        classifications={"unused": "irrelevant"},
    )

    assert result.status == "full-load"
    assert result.reason_code == "missing-inventory-fingerprint"
    assert not settings.exists()


def test_live_lease_contention_uses_full_load_without_mutation(tmp_path: Path):
    settings = tmp_path / "settings.json"
    settings.write_text("{}\n", encoding="utf-8")
    first = _apply(tmp_path, settings, "owner")
    guarded = settings.read_bytes()

    second = _apply(tmp_path, settings, "contender")

    assert first.status == "reduced"
    assert second.status == "full-load"
    assert second.reason_code == "lease-contention"
    assert settings.read_bytes() == guarded
    assert receipts.inspect_receipt(tmp_path, "contender")["reason_codes"] == ["lease-contention"]


def test_verification_mismatch_preserves_external_edit_and_disables_profile(tmp_path: Path):
    settings = tmp_path / "settings.json"
    settings.write_text('{"model":"baseline"}\n', encoding="utf-8")

    def alter(path: Path):
        path.write_text('{"model":"external-edit"}\n', encoding="utf-8")

    result = _apply(tmp_path, settings, "mismatch", verify_hook=alter)

    assert result.status == "full-load"
    assert result.reason_code == "actual-state-mismatch"
    assert json.loads(settings.read_text(encoding="utf-8")) == {"model": "external-edit"}
    assert claude_profile.profile_status(tmp_path, settings)["disabled"] is True


def test_success_receipt_failure_rolls_back_profile(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    settings = tmp_path / "settings.json"
    baseline = b'{"model":"baseline"}\n'
    settings.write_bytes(baseline)

    def fail_receipt(_root, _payload):
        raise receipts.ReceiptBusyError("injected")

    monkeypatch.setattr(receipts, "write_receipt", fail_receipt)
    with pytest.raises(receipts.ReceiptBusyError):
        _apply(tmp_path, settings, "receipt-failure")

    assert settings.read_bytes() == baseline
    assert claude_profile.profile_status(tmp_path, settings)["leased"] is False


def test_restore_is_exact_and_idempotent(tmp_path: Path):
    settings = tmp_path / "settings.json"
    baseline = b'{"model":"exact","skillOverrides":{"existing":"name-only"}}\n'
    settings.write_bytes(baseline)
    _apply(tmp_path, settings, "apply-exact")

    restored = claude_profile.restore_profile(
        tmp_path, settings, run_id="restore-exact", version="2.1.218"
    )
    repeated = claude_profile.restore_profile(
        tmp_path, settings, run_id="restore-again", version="2.1.218"
    )

    assert restored.status == "restored"
    assert settings.read_bytes() == baseline
    assert repeated.reason_code == "already-restored"
    assert claude_profile.profile_status(tmp_path, settings)["leased"] is False


def test_restore_refuses_to_overwrite_user_edit_and_disables(tmp_path: Path):
    settings = tmp_path / "settings.json"
    settings.write_text('{"model":"baseline"}\n', encoding="utf-8")
    _apply(tmp_path, settings, "apply-edit")
    settings.write_text('{"model":"user-edit"}\n', encoding="utf-8")

    result = claude_profile.restore_profile(
        tmp_path, settings, run_id="restore-edit", version="2.1.218"
    )

    assert result.status == "full-load"
    assert result.reason_code == "user-edit-detected"
    assert result.recovery_action
    assert json.loads(settings.read_text(encoding="utf-8")) == {"model": "user-edit"}
    assert claude_profile.profile_status(tmp_path, settings)["disabled"] is True


def test_dead_owner_recovery_restores_unchanged_applied_state(tmp_path: Path):
    settings = tmp_path / "settings.json"
    baseline = b'{"model":"baseline"}\n'
    settings.write_bytes(baseline)
    _apply(tmp_path, settings, "dead-owner", pid=99999999)

    recovered = claude_profile.recover_profile(
        tmp_path,
        settings,
        run_id="recover-dead",
        version="2.1.218",
        liveness=lambda _pid: False,
    )

    assert recovered.status == "restored"
    assert settings.read_bytes() == baseline
    assert claude_profile.profile_status(tmp_path, settings)["leased"] is False


def test_dead_owner_recovery_preserves_edit_and_disables(tmp_path: Path):
    settings = tmp_path / "settings.json"
    _apply(tmp_path, settings, "dead-edited", pid=99999999)
    settings.write_text('{"model":"user-edit"}\n', encoding="utf-8")

    recovered = claude_profile.recover_profile(
        tmp_path,
        settings,
        run_id="recover-dead-edit",
        version="2.1.218",
        liveness=lambda _pid: False,
    )

    assert recovered.status == "full-load"
    assert recovered.reason_code == "user-edit-detected"
    assert json.loads(settings.read_text(encoding="utf-8")) == {"model": "user-edit"}
    assert claude_profile.profile_status(tmp_path, settings)["disabled"] is True


def test_recovery_does_not_touch_live_owner(tmp_path: Path):
    settings = tmp_path / "settings.json"
    settings.write_text("{}\n", encoding="utf-8")
    _apply(tmp_path, settings, "live-owner")
    guarded = settings.read_bytes()

    result = claude_profile.recover_profile(
        tmp_path,
        settings,
        run_id="recover-live",
        version="2.1.218",
        liveness=lambda _pid: True,
    )

    assert result.reason_code == "lease-owner-alive"
    assert settings.read_bytes() == guarded


def test_restore_returns_settings_to_prior_absence(tmp_path: Path):
    settings = tmp_path / "new" / "settings.local.json"
    _apply(tmp_path, settings, "apply-absent")
    assert settings.is_file()

    restored = claude_profile.restore_profile(
        tmp_path, settings, run_id="restore-absent", version="2.1.218"
    )

    assert restored.status == "restored"
    assert not settings.exists()


def test_baseline_override_conflict_falls_back_without_mutation(tmp_path: Path):
    settings = tmp_path / "settings.json"
    baseline = b'{"skillOverrides":{"unused":"off"},"model":"keep"}\n'
    settings.write_bytes(baseline)

    result = _apply(tmp_path, settings, "conflict")

    assert result.status == "full-load"
    assert result.reason_code == "baseline-override-conflict"
    assert settings.read_bytes() == baseline
    assert claude_profile.profile_status(tmp_path, settings)["leased"] is False


@pytest.mark.parametrize("classification", ["required", "safety-critical", "uncertain"])
def test_conservative_only_plan_does_not_create_profile(tmp_path: Path, classification: str):
    settings = tmp_path / "settings.json"
    result = _apply(
        tmp_path,
        settings,
        f"none-{classification}",
        classifications={"skill": classification},
    )
    assert result.reason_code == "no-eligible-skills"
    assert not settings.exists()
