"""File-read policy: deny globs, size thresholds, bounded-range detection."""

from __future__ import annotations

import fnmatch
from pathlib import Path

from context_guard import decisions, events
from context_guard.policy_config import Policy

RULE_DENY_GLOB = "files.deny_glob"
RULE_OVERSIZED_READ = "files.oversized_full_read"


def _matches_any(path: str, globs: list[str]) -> bool:
    normalized = path.replace("\\", "/")
    for pattern in globs:
        if fnmatch.fnmatch(normalized, pattern):
            return True
        # A "**/x" pattern means "zero or more leading directories", so it
        # must also match a bare root-level path with no directory prefix.
        if pattern.startswith("**/") and fnmatch.fnmatch(normalized, pattern[3:]):
            return True
    return False


def evaluate(event: events.Event, policy: Policy, has_range: bool = False) -> decisions.Decision | None:
    """Evaluate a file_read event. Returns None when this module does not apply."""
    if event.operation_kind != events.FILE_READ:
        return None
    if not event.path:
        return None

    files_cfg = policy.files
    mode = policy.mode_for("files")

    deny_globs = files_cfg.get("deny", [])
    if _matches_any(event.path, deny_globs):
        decision = decisions.block(
            f"'{event.path}' matches an excluded/generated path pattern and should not be read in full. "
            "Search for the required symbol first or request a bounded range.",
            RULE_DENY_GLOB,
            suggestions=[f"Read a bounded line range of '{event.path}' instead of the full file."],
        )
        return decisions.apply_mode(decision, mode)

    max_full_read = files_cfg.get("max_full_read_bytes")
    require_range_above = files_cfg.get("require_range_above_bytes")
    if max_full_read is None and require_range_above is None:
        return None

    try:
        size = Path(event.path).stat().st_size
    except OSError:
        # Cannot verify size; fail open for this specific check only.
        return None

    threshold = require_range_above if require_range_above is not None else max_full_read
    if size > threshold and not has_range:
        decision = decisions.block(
            f"'{event.path}' is {size} bytes, exceeding the {threshold}-byte bounded-read threshold. "
            "Request a bounded line range instead of a full read.",
            RULE_OVERSIZED_READ,
            suggestions=[f"Read '{event.path}' with an explicit line range or offset/limit."],
        )
        return decisions.apply_mode(decision, mode)

    return None
