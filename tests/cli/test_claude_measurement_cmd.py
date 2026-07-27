from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from context_guard import claude_measurement as measurement
from context_guard import cli, quality


def test_claude_measurement_extract_and_ledger_cli(
    tmp_path: Path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        quality.QualityLedger,
        "authorize_measurement",
        lambda self, pair_id, **kwargs: quality.Authorization(pair_id, True, "pass"),
    )
    source = tmp_path / "session.jsonl"
    row = {
        "type": "assistant",
        "sessionId": "session-1",
        "requestId": "request-1",
        "message": {
            "id": "message-1",
            "model": "claude-test",
            "usage": {
                "cache_creation_input_tokens": 100,
                "cache_read_input_tokens": 200,
            },
        },
    }
    source.write_text(json.dumps(row) + "\n", encoding="utf-8")

    result = cli.main(
        [
            "claude-measurement",
            "extract",
            str(source),
            "--run-id",
            "cli-run",
            "--quality-pair",
            "quality-pair",
            "--fixture-kind",
            "read-only-analysis",
            "--role",
            "baseline",
            "--version",
            "2.1.218",
            "--model",
            "claude-test",
            "--session-id",
            "session-1",
        ]
    )

    assert result == 0
    assert json.loads(capsys.readouterr().out)["cache_tokens"] == 300
    assert cli.main(["claude-measurement", "ledger"]) == 0
    records = json.loads(capsys.readouterr().out)
    assert records[0]["event"] == "run"
    assert str(source) not in json.dumps(records)


def test_claude_measurement_pair_cli_rejects_unknown_input(
    tmp_path: Path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    baseline = tmp_path / "baseline.json"
    guarded = tmp_path / "guarded.json"
    baseline.write_text(json.dumps({"schema": measurement.RUN_SCHEMA, "prompt": "raw"}))
    guarded.write_text("{}")

    assert (
        cli.main(
            [
                "claude-measurement",
                "pair",
                "--baseline",
                str(baseline),
                "--guarded",
                str(guarded),
                "--pair-id",
                "pair",
                "--execution-order",
                "baseline-first",
            ]
        )
        == 1
    )
    assert "unknown fields" in capsys.readouterr().err


def test_claude_measurement_qualify_cli_records_passing_distribution(
    tmp_path: Path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        quality.QualityLedger,
        "authorize_measurement",
        lambda self, pair_id, **kwargs: quality.Authorization(pair_id, True, "pass"),
    )
    paths = []
    kinds = sorted(measurement.FIXTURE_KINDS)
    for index in range(15):
        reduction = Fraction(2, 5)
        pair = measurement.ClaudePairMeasurement(
            measurement.PAIR_SCHEMA,
            f"pair-{index}",
            f"quality-{index}",
            kinds[index // 5],
            "2.1.218",
            "claude-test",
            "baseline-first" if index % 2 == 0 else "guarded-first",
            f"baseline-{index}",
            f"guarded-{index}",
            100,
            60,
            reduction.numerator,
            reduction.denominator,
        )
        path = tmp_path / f"pair-{index}.json"
        path.write_text(json.dumps(pair.to_dict()), encoding="utf-8")
        paths.append(path)

    assert (
        cli.main(
            [
                "claude-measurement",
                "qualify",
                *map(str, paths),
                "--qualification-id",
                "cli-qualification",
            ]
        )
        == 0
    )
    result = json.loads(capsys.readouterr().out)
    assert result["passed"] is True
    assert result["provider_median_numerator"] == 2
    assert result["provider_median_denominator"] == 5
