from __future__ import annotations

import json
from pathlib import Path

from context_guard import cli, quality


def _common() -> list[str]:
    return [
        "--run-id", "cli-run", "--quality-pair", "quality-pair",
        "--fixture-kind", "read-only-analysis", "--role", "baseline",
        "--version", "0.144.1", "--model", "gpt-test",
        "--thread-id", "thread-1",
    ]


def test_codex_exact_and_ledger_cli(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        quality.QualityLedger,
        "authorize_measurement",
        lambda self, pair_id, **kwargs: quality.Authorization(pair_id, True, "pass"),
    )
    source = tmp_path / "exec.jsonl"
    source.write_text(
        json.dumps({"type": "thread.started", "thread_id": "thread-1"})
        + "\n"
        + json.dumps(
            {"type": "turn.completed", "usage": {"cached_input_tokens": 77}}
        )
        + "\n",
        encoding="utf-8",
    )

    assert cli.main(["codex-measurement", "exact", str(source), *_common()]) == 0
    assert json.loads(capsys.readouterr().out)["cached_input_tokens"] == 77
    assert cli.main(["codex-measurement", "ledger"]) == 0
    records = json.loads(capsys.readouterr().out)
    assert records[0]["event"] == "run"
    assert str(source) not in json.dumps(records)


def test_codex_cumulative_cli_rejects_counter_reset(
    tmp_path: Path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        quality.QualityLedger,
        "authorize_measurement",
        lambda self, pair_id, **kwargs: quality.Authorization(pair_id, True, "pass"),
    )
    assert cli.main(
        [
            "codex-measurement", "cumulative", *_common(),
            "--start-boundary", "before", "--end-boundary", "after",
            "--start-cached-input", "100", "--end-cached-input", "50",
        ]
    ) == 1
    assert "non-monotonic" in capsys.readouterr().err
