"""Safe fallback parser: used when no framework-specific parser recognizes the output.

Never fabricates a diagnosis. Always returns a result (never None).
"""

from __future__ import annotations

from context_guard.compact.result import CompactResult, STATUS_ERROR, STATUS_UNPARSED

PREVIEW_LINES = 20


def _preview(text: str, lines: int = PREVIEW_LINES) -> str:
    split = text.splitlines()
    if len(split) <= lines * 2:
        return text
    head = split[:lines]
    tail = split[-lines:]
    return "\n".join(head) + f"\n... ({len(split) - lines * 2} lines omitted) ...\n" + "\n".join(tail)


def parse(exit_code: int, stdout: bytes, stderr: bytes, launch_error: str | None) -> tuple[CompactResult, dict]:
    """Always returns a result: exit status, bounded preview, and the (already-written) artifact reference."""
    fragments = {
        "preview-stdout": {"file": "stdout.txt", "start": 0, "end": len(stdout)},
        "preview-stderr": {"file": "stderr.txt", "start": 0, "end": len(stderr)},
    }

    if launch_error:
        notes = [f"command failed to launch: {launch_error}"]
        status = STATUS_ERROR
    else:
        notes = [
            "output format not recognized by any parser; showing exit status and a bounded preview only",
            f"stdout preview: {_preview(stdout.decode('utf-8', errors='replace'))}",
        ]
        status = STATUS_ERROR if exit_code != 0 else STATUS_UNPARSED

    result = CompactResult(
        status=status,
        artifact="",
        tests=None,
        failures=[],
        notes=notes,
    )
    return result, fragments
