import json
import sys
from pathlib import Path

from context_guard import cli
from context_guard.compact import artifact_store, ledger

FIXTURES = Path(__file__).parent.parent / "fixtures" / "compact"


def test_passing_run_produces_correct_totals(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    script = FIXTURES / "fake_pytest_pass.py"
    assert cli.main(["test", "--", sys.executable, str(script)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "passed"
    assert result["tests"] == {"collected": 5, "passed": 5, "failed": 0}
    assert result["failures"] == []
    assert result["artifact"].startswith("artifact:test-")


def test_failing_run_identifies_correct_failure(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    script = FIXTURES / "fake_pytest_fail.py"
    assert cli.main(["test", "--", sys.executable, str(script)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "failed"
    assert result["tests"] == {"collected": 6, "passed": 5, "failed": 1}
    assert len(result["failures"]) == 1
    failure = result["failures"][0]
    assert failure["name"] == "test_duplicate_callback"
    assert failure["file"] == "test_x.py"
    assert "AssertionError" in failure["diagnostic"]
    assert failure["evidence"].startswith(result["artifact"] + "#")


def test_unrecognized_output_uses_safe_fallback(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    script = FIXTURES / "fake_unrecognized.py"
    assert cli.main(["test", "--", sys.executable, str(script)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["failures"] == []
    assert result["tests"] is None
    assert any("not recognized" in note for note in result["notes"])
    assert result["artifact"].startswith("artifact:")


def test_nonexistent_command_returns_structured_result(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["test", "--", "this-command-does-not-exist-xyz"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "error"
    assert any("failed to launch" in note for note in result["notes"])


def test_run_appends_ledger_row(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    script = FIXTURES / "fake_pytest_pass.py"
    cli.main(["test", "--", sys.executable, str(script)])
    result = json.loads(capsys.readouterr().out)
    rows = ledger.all_rows(tmp_path)
    assert len(rows) == 1
    assert result["artifact"].endswith(rows[0]["artifact_id"])


def test_artifact_and_ledger_contain_no_environment_values(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.setenv("CONTEXT_GUARD_TEST_SECRET", "super-secret-value-123")
    monkeypatch.chdir(tmp_path)
    script = FIXTURES / "fake_pytest_pass.py"
    cli.main(["test", "--", sys.executable, str(script)])
    result = json.loads(capsys.readouterr().out)
    artifact_id = result["artifact"].split(":", 1)[1]
    full = artifact_store.read_full(tmp_path, artifact_id)
    for content in full["files"].values():
        assert b"super-secret-value-123" not in content
    for row in ledger.all_rows(tmp_path):
        assert "super-secret-value-123" not in json.dumps(row)


def test_commit_recorded_inside_git_repo(tmp_path: Path, monkeypatch, capsys):
    import subprocess

    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "-c", "user.email=a@b.c", "-c", "user.name=a", "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-q", "-m", "x"],
        cwd=tmp_path,
        check=True,
    )
    monkeypatch.chdir(tmp_path)
    script = FIXTURES / "fake_pytest_pass.py"
    cli.main(["test", "--", sys.executable, str(script)])
    result = json.loads(capsys.readouterr().out)
    artifact_id = result["artifact"].split(":", 1)[1]
    full = artifact_store.read_full(tmp_path, artifact_id)
    meta = json.loads(full["files"]["meta.json"])
    assert meta["commit"] is not None
    assert len(meta["commit"]) == 40


def test_commit_absent_outside_git_repo(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    script = FIXTURES / "fake_pytest_pass.py"
    cli.main(["test", "--", sys.executable, str(script)])
    result = json.loads(capsys.readouterr().out)
    artifact_id = result["artifact"].split(":", 1)[1]
    full = artifact_store.read_full(tmp_path, artifact_id)
    meta = json.loads(full["files"]["meta.json"])
    assert meta["commit"] is None
