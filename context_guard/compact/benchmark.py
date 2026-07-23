"""CTX-01 (Noisy test suite) reproducible local benchmark.

Runs the same fixture test suite twice — once as a raw baseline invocation,
once through Compact Runtime — and reports the PRFAQ's directly-measured
Metrics Collected fields for CTX-01. Does not estimate or publish any
provider-billed token/cost figure.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

from context_guard.compact import artifact_store
from context_guard.compact.pipeline import run_compact_test

KNOWN_FAILING_TEST = "test_duplicate_callback"


def run_ctx01(repo_root: Path, fixture_path: Path) -> dict[str, Any]:
    baseline = subprocess.run(
        [sys.executable, "-m", "pytest", str(fixture_path)],
        cwd=repo_root,
        capture_output=True,
    )
    baseline_bytes = len(baseline.stdout) + len(baseline.stderr)
    baseline_lines = baseline.stdout.count(b"\n") + baseline.stderr.count(b"\n")

    result, artifact_id = run_compact_test(repo_root, [sys.executable, "-m", "pytest", str(fixture_path)])
    compact_json = __import__("json").dumps(result.to_dict())
    compact_bytes = len(compact_json.encode("utf-8"))
    compact_lines = compact_json.count("\n") + 1

    required_evidence_found = any(f.name == KNOWN_FAILING_TEST for f in result.failures)

    full_artifact_available = True
    try:
        artifact_store.read_full(repo_root, artifact_id)
    except (artifact_store.ArtifactNotFoundError, artifact_store.FragmentNotFoundError):
        full_artifact_available = False

    compression_ratio = compact_bytes / baseline_bytes if baseline_bytes else None

    return {
        "baseline_output_bytes": baseline_bytes,
        "compact_output_bytes": compact_bytes,
        "baseline_output_lines": baseline_lines,
        "compact_output_lines": compact_lines,
        "compression_ratio": compression_ratio,
        "required_evidence_found": required_evidence_found,
        "full_artifact_available": full_artifact_available,
    }


if __name__ == "__main__":
    import json

    fixture = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("tests/fixtures/compact/test_generated.py")
    metrics = run_ctx01(Path.cwd(), fixture)
    print(json.dumps(metrics, indent=2))
