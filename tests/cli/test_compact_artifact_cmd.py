import json
import sys
from pathlib import Path

from context_guard import cli

FIXTURES = Path(__file__).parent.parent / "fixtures" / "compact"


def _run_failing(tmp_path: Path, monkeypatch, capsys) -> dict:
    monkeypatch.chdir(tmp_path)
    script = FIXTURES / "fake_pytest_fail.py"
    cli.main(["test", "--", sys.executable, str(script)])
    return json.loads(capsys.readouterr().out)


def test_show_fragment_returns_exact_failure_text(tmp_path: Path, monkeypatch, capsys):
    result = _run_failing(tmp_path, monkeypatch, capsys)
    artifact_id = result["artifact"].split(":", 1)[1]
    fragment_id = result["failures"][0]["evidence"].split("#", 1)[1]

    assert cli.main(["artifact", "show", artifact_id, "--fragment", fragment_id]) == 0
    output = capsys.readouterr().out
    assert "FAILED test_x.py::test_duplicate_callback" in output


def test_show_without_fragment_returns_full_capture(tmp_path: Path, monkeypatch, capsys):
    result = _run_failing(tmp_path, monkeypatch, capsys)
    artifact_id = result["artifact"].split(":", 1)[1]

    assert cli.main(["artifact", "show", artifact_id]) == 0
    output = capsys.readouterr().out
    assert "collected 6 items" in output
    assert "short test summary info" in output


def test_show_unknown_artifact_id_errors(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["artifact", "show", "test-999"]) == 1
    assert "Not found" in capsys.readouterr().err


def test_show_unknown_fragment_id_errors(tmp_path: Path, monkeypatch, capsys):
    result = _run_failing(tmp_path, monkeypatch, capsys)
    artifact_id = result["artifact"].split(":", 1)[1]
    assert cli.main(["artifact", "show", artifact_id, "--fragment", "no-such-fragment"]) == 1
    assert "Not found" in capsys.readouterr().err
