"""Executes a command and captures its complete raw output."""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class RawCapture:
    command: list[str]
    stdout: bytes
    stderr: bytes
    exit_code: int
    duration_seconds: float
    commit: str | None
    timestamp: str
    native_report_path: str | None = None
    launch_error: str | None = None


def _current_commit(cwd: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def run(command: list[str], cwd: Path, native_report_path: str | None = None) -> RawCapture:
    """Execute `command` as a subprocess (never via a shell) and capture its output."""
    commit = _current_commit(cwd)
    timestamp = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            shell=False,
        )
        duration = time.perf_counter() - start
        return RawCapture(
            command=command,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode,
            duration_seconds=duration,
            commit=commit,
            timestamp=timestamp,
            native_report_path=native_report_path,
        )
    except OSError as exc:
        duration = time.perf_counter() - start
        return RawCapture(
            command=command,
            stdout=b"",
            stderr=b"",
            exit_code=-1,
            duration_seconds=duration,
            commit=commit,
            timestamp=timestamp,
            native_report_path=native_report_path,
            launch_error=str(exc),
        )
