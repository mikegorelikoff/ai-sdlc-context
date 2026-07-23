from pathlib import Path

from context_guard.compact.benchmark import run_ctx01

FIXTURE = Path(__file__).parent.parent / "fixtures" / "compact" / "test_generated.py"


def test_ctx01_quality_gate(tmp_path: Path):
    assert FIXTURE.is_file(), "run tests/fixtures/compact/gen_fixture.py to regenerate the fixture"

    metrics = run_ctx01(tmp_path, FIXTURE)

    assert metrics["compact_output_bytes"] < metrics["baseline_output_bytes"]
    assert metrics["required_evidence_found"] is True
    assert metrics["full_artifact_available"] is True
    assert metrics["compression_ratio"] < 1.0
