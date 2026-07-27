from __future__ import annotations

import json
import stat
from datetime import datetime, timezone
from pathlib import Path

import pytest

from context_guard import receipts


def _receipt(run_id: str, timestamp: str = "2026-07-27T12:00:00+00:00", **overrides):
    payload = {
        "schema": receipts.SCHEMA,
        "run_id": run_id,
        "timestamp": timestamp,
        "provider": "codex",
        "provider_version": "0.144.1",
        "surface": "cli",
        "status": "valid",
        "completed": True,
        "referenced": False,
        "policy_fingerprint": "policy-digest",
        "inventory_fingerprint": "inventory-digest",
        "identity_digests": ["skill-digest"],
        "reason_codes": ["exact-irrelevant"],
        "classifications": ["irrelevant"],
        "requested_action": "reduce",
        "actual_action": "reduce",
        "restoration_status": "not-required",
    }
    payload.update(overrides)
    return payload


def test_write_and_inspect_receipt_is_private_and_deterministic(tmp_path: Path):
    target = receipts.write_receipt(tmp_path, _receipt("run-001"))

    assert target == tmp_path / ".context-guard" / "receipts" / "records" / "run-001.json"
    assert stat.S_IMODE(target.stat().st_mode) == 0o600
    assert stat.S_IMODE(target.parent.stat().st_mode) == 0o700
    assert stat.S_IMODE(target.parent.parent.stat().st_mode) == 0o700
    assert receipts.inspect_receipt(tmp_path, "run-001") == _receipt("run-001")
    assert target.read_text(encoding="utf-8").endswith("\n")


@pytest.mark.parametrize("forbidden", ["prompt", "response", "source", "secret", "environment"])
def test_unknown_or_prohibited_fields_are_rejected_before_write(tmp_path: Path, forbidden: str):
    payload = _receipt("unsafe")
    payload[forbidden] = "must never persist"

    with pytest.raises(receipts.ReceiptValidationError, match="unknown fields"):
        receipts.write_receipt(tmp_path, payload)

    assert not (tmp_path / ".context-guard" / "receipts" / "records" / "unsafe.json").exists()
    assert "must never persist" not in "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in tmp_path.rglob("*")
        if path.is_file()
    )


def test_receipt_store_rejects_preexisting_symlinked_private_root(tmp_path: Path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (tmp_path / ".context-guard").symlink_to(outside, target_is_directory=True)

    with pytest.raises(receipts.ReceiptValidationError, match="symlink"):
        receipts.write_receipt(tmp_path, _receipt("symlinked"))

    assert not (outside / "receipts").exists()


def test_existing_receipt_is_never_overwritten(tmp_path: Path):
    target = receipts.write_receipt(tmp_path, _receipt("same"))
    original = target.read_bytes()

    with pytest.raises(receipts.ReceiptExistsError):
        receipts.write_receipt(tmp_path, _receipt("same", status="invalid"))

    assert target.read_bytes() == original


def test_writer_lock_contention_fails_without_a_partial_record(tmp_path: Path):
    with receipts.writer_lock(tmp_path):
        with pytest.raises(receipts.ReceiptBusyError):
            receipts.write_receipt(tmp_path, _receipt("blocked"))

    records = tmp_path / ".context-guard" / "receipts" / "records"
    assert list(records.glob("*.json")) == []
    assert list(records.glob("*.tmp")) == []


@pytest.mark.parametrize("run_id", ["../escape", "/absolute", "a/b", "", ".hidden"])
def test_traversal_like_run_ids_are_rejected(tmp_path: Path, run_id: str):
    with pytest.raises(receipts.ReceiptValidationError):
        receipts.inspect_receipt(tmp_path, run_id)
    with pytest.raises(receipts.ReceiptValidationError):
        receipts.delete_receipt(tmp_path, run_id)


def test_delete_removes_only_exact_receipt(tmp_path: Path):
    receipts.write_receipt(tmp_path, _receipt("keep"))
    receipts.write_receipt(tmp_path, _receipt("delete"))

    assert receipts.delete_receipt(tmp_path, "delete") is True
    assert receipts.delete_receipt(tmp_path, "delete") is False
    assert receipts.inspect_receipt(tmp_path, "keep")["run_id"] == "keep"


def test_inspection_quarantines_original_corrupt_bytes(tmp_path: Path):
    target = receipts.write_receipt(tmp_path, _receipt("corrupt"))
    raw = b'{"schema":"wrong","run_id":"corrupt"}\n'
    target.write_bytes(raw)

    with pytest.raises(receipts.ReceiptCorruptError) as error:
        receipts.inspect_receipt(tmp_path, "corrupt")

    assert not target.exists()
    assert error.value.quarantine_path.read_bytes() == raw
    assert stat.S_IMODE(error.value.quarantine_path.stat().st_mode) == 0o600
    with pytest.raises(receipts.ReceiptNotFoundError):
        receipts.inspect_receipt(tmp_path, "corrupt")


def test_prune_deletes_only_old_completed_unreferenced_and_quarantines_corrupt(tmp_path: Path):
    receipts.write_receipt(tmp_path, _receipt("old", "2026-06-01T00:00:00+00:00"))
    receipts.write_receipt(
        tmp_path,
        _receipt("active", "2026-06-01T00:00:00+00:00", completed=False),
    )
    receipts.write_receipt(
        tmp_path,
        _receipt("referenced", "2026-06-01T00:00:00+00:00", referenced=True),
    )
    receipts.write_receipt(tmp_path, _receipt("recent", "2026-07-20T00:00:00+00:00"))
    corrupt = receipts.write_receipt(tmp_path, _receipt("broken", "2026-06-01T00:00:00+00:00"))
    corrupt_raw = b"not-json"
    corrupt.write_bytes(corrupt_raw)

    result = receipts.prune_receipts(
        tmp_path,
        now=datetime(2026, 7, 27, tzinfo=timezone.utc),
    )

    assert result.deleted == ("old",)
    assert result.retained == ("active", "recent", "referenced")
    assert result.quarantined == ("broken.json",)
    assert {item["run_id"] for item in map(json.loads, [
        path.read_text(encoding="utf-8")
        for path in (tmp_path / ".context-guard" / "receipts" / "records").glob("*.json")
    ])} == {"active", "referenced", "recent"}
    assert (tmp_path / ".context-guard" / "receipts" / "quarantine" / "broken.json").read_bytes() == corrupt_raw


def test_timestamp_must_be_timezone_aware_and_retention_positive(tmp_path: Path):
    with pytest.raises(receipts.ReceiptValidationError, match="timezone"):
        receipts.write_receipt(tmp_path, _receipt("naive", "2026-07-27T12:00:00"))
    with pytest.raises(receipts.ReceiptValidationError, match="positive integer"):
        receipts.prune_receipts(tmp_path, retention_days=0)
