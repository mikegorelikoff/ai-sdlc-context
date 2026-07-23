import io
import json
import statistics
import sys
import time
from pathlib import Path

import pytest

from context_guard import cli

FIXTURE_PAYLOAD = {
    "hook_event_name": "PreToolUse",
    "tool_name": "Bash",
    "tool_input": {"command": "docker compose logs api"},
    "session_id": "perf-session",
    "cwd": "/repo",
}


@pytest.mark.perf
def test_median_hook_evaluation_latency_under_100ms(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    durations = []
    for _ in range(100):
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(FIXTURE_PAYLOAD)))
        start = time.perf_counter()
        cli.main(["hook", "claude"])
        durations.append(time.perf_counter() - start)
        capsys.readouterr()

    median_seconds = statistics.median(durations)
    assert median_seconds < 0.1, f"median latency {median_seconds * 1000:.2f}ms exceeds 100ms budget"
