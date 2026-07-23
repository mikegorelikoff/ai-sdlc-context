"""Deterministic text-based fallback parser for pytest's default console output."""

from __future__ import annotations

import re

from context_guard.compact.result import CompactResult, Failure, STATUS_FAILED, STATUS_PASSED

_SUMMARY_RE = re.compile(
    r"=+\s*(?:(\d+) failed,?\s*)?(?:(\d+) passed,?\s*)?(?:(\d+) error(?:s)?,?\s*)?.*?\s*in\s+[\d.]+s\s*=+"
)
_FAILED_LINE_RE = re.compile(r"^FAILED\s+(?P<file>[^:]+)::(?P<name>\S+)(?:\s+-\s+(?P<diagnostic>.*))?$")


def parse(stdout: bytes) -> tuple[CompactResult, dict] | None:
    """Parse pytest's default text summary. Returns None when no summary line is recognized."""
    stdout_text = stdout.decode("utf-8", errors="replace")
    summary_match = _SUMMARY_RE.search(stdout_text)
    if not summary_match:
        return None

    failed_count = int(summary_match.group(1) or 0)
    passed_count = int(summary_match.group(2) or 0)
    error_count = int(summary_match.group(3) or 0)
    collected = failed_count + passed_count + error_count

    failures: list[Failure] = []
    fragments: dict = {}
    fragment_index = 1

    for line in stdout_text.splitlines():
        match = _FAILED_LINE_RE.match(line.strip())
        if not match:
            continue
        fragment_id = f"failure-{fragment_index}"
        fragment_index += 1
        line_bytes = line.encode("utf-8")
        start = stdout.find(line_bytes)
        end = start + len(line_bytes) if start != -1 else len(stdout)
        fragments[fragment_id] = {"file": "stdout.txt", "start": start if start != -1 else 0, "end": end}
        failures.append(
            Failure(
                name=match.group("name"),
                file=match.group("file"),
                line=0,
                diagnostic=(match.group("diagnostic") or "test failed").strip(),
                evidence=fragment_id,
            )
        )

    status = STATUS_FAILED if failed_count or error_count else STATUS_PASSED
    notes = []
    if (failed_count or error_count) and not failures:
        notes.append("summary reported failures but no FAILED lines were found; totals may be approximate")

    result = CompactResult(
        status=status,
        artifact="",
        tests={"collected": collected, "passed": passed_count, "failed": failed_count + error_count},
        failures=failures,
        notes=notes,
    )
    return result, fragments
