import json
from pathlib import Path

from context_guard import cli


def test_inventory_cli_returns_minimized_supported_result(tmp_path: Path, capsys):
    skill = tmp_path / ".agents" / "skills" / "sample" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        "---\nname: sample\ndescription: do not emit me\n---\nsecret body\n",
        encoding="utf-8",
    )

    assert (
        cli.main(
            [
                "inventory",
                "--provider",
                "codex",
                "--version",
                "0.144.1",
                "--surface",
                "cli",
                "--home",
                str(tmp_path),
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    result = json.loads(output)
    assert result["status"] == "supported"
    assert result["records"][0]["name"] == "sample"
    assert "secret body" not in output
    assert "do not emit me" not in output


def test_inventory_cli_returns_nonzero_for_unsupported(tmp_path: Path, capsys):
    assert (
        cli.main(
            [
                "inventory",
                "--provider",
                "claude",
                "--version",
                "2.1.217",
                "--surface",
                "cli",
                "--home",
                str(tmp_path),
            ]
        )
        == 1
    )

    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "unsupported"
    assert result["records"] == []
    assert result["fingerprint"] is None
