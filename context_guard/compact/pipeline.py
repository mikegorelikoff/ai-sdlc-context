"""Shared execute -> artifact -> parse -> compact-result pipeline.

Used by both the `context-guard test` CLI subcommand and the CTX-01 benchmark
so the two never drift out of sync.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from context_guard.compact import artifact_store, ledger
from context_guard.compact import runner as compact_runner
from context_guard.compact.parsers import fallback as fallback_parser
from context_guard.compact.parsers import pytest_junitxml, pytest_text
from context_guard.compact.result import CompactResult


def run_compact_test(repo_root: Path, command: list[str]) -> tuple[CompactResult, str]:
    """Run `command`, store the full result, parse it, and record a ledger row.

    Returns (compact_result, artifact_id).
    """
    use_junitxml = command[0].rsplit("/", 1)[-1] == "pytest"
    junit_path = None
    run_command = command
    if use_junitxml:
        tmp_dir = tempfile.mkdtemp(prefix="context-guard-junit-")
        junit_path = str(Path(tmp_dir) / "junit.xml")
        run_command = command + [f"--junitxml={junit_path}"]

    raw = compact_runner.run(run_command, repo_root, native_report_path=junit_path)

    artifact_id = artifact_store.allocate(repo_root, "test")
    files = {
        "stdout.txt": raw.stdout,
        "stderr.txt": raw.stderr,
        "meta.json": json.dumps(
            {
                "command": command,
                "exit_code": raw.exit_code,
                "duration_seconds": raw.duration_seconds,
                "commit": raw.commit,
                "timestamp": raw.timestamp,
                "launch_error": raw.launch_error,
            }
        ).encode("utf-8"),
    }
    junit_bytes = None
    if junit_path and Path(junit_path).is_file():
        junit_bytes = Path(junit_path).read_bytes()
        files["junit.xml"] = junit_bytes

    parsed = None
    if junit_bytes:
        parsed = pytest_junitxml.parse(junit_bytes)
    if parsed is None:
        parsed = pytest_text.parse(raw.stdout)
    if parsed is None:
        parsed = fallback_parser.parse(raw.exit_code, raw.stdout, raw.stderr, raw.launch_error)

    result, fragments = parsed
    artifact_ref = artifact_store.reference(artifact_id)
    result.artifact = artifact_ref
    for failure in result.failures:
        failure.evidence = artifact_store.fragment_reference(artifact_id, failure.evidence)

    artifact_store.write(repo_root, "test", artifact_id, files, fragments=fragments)

    ledger.record(
        repo_root,
        command=" ".join(command),
        commit=raw.commit,
        artifact_kind="test",
        artifact_id=artifact_id,
        status=result.status,
        summary={"tests": result.tests, "failed_count": len(result.failures)},
        timestamp=raw.timestamp,
    )

    return result, artifact_id
