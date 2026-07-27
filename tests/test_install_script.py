import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]
INSTALLER = ROOT / "install.sh"


def test_installer_has_valid_bash_syntax():
    subprocess.run(["bash", "-n", str(INSTALLER)], check=True)


def test_installer_declares_one_line_defaults_and_both_providers():
    text = INSTALLER.read_text(encoding="utf-8")

    assert "https://github.com/mikegorelikoff/ai-sdlc-context/archive/refs/heads/main.zip" in text
    assert '"$context_guard_bin_dir/context-guard" install claude' in text
    assert '"$context_guard_bin_dir/context-guard" install codex' in text
    assert "sudo" not in text


def test_installer_fails_clearly_without_python(tmp_path: Path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    os.symlink("/bin/bash", fake_bin / "bash")
    os.symlink("/usr/bin/curl", fake_bin / "curl")

    result = subprocess.run(
        ["/bin/bash", str(INSTALLER)],
        env={"PATH": str(fake_bin), "HOME": str(tmp_path)},
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Python 3.10 or newer is required" in result.stderr


def test_readme_is_the_complete_user_document():
    text = (ROOT / "README.md").read_text(encoding="utf-8")

    for heading in (
        "## Requirements",
        "## Install",
        "## Verify",
        "## The one policy",
        "## Use",
        "## Reproducible examples",
        "## Update",
        "## Uninstall",
    ):
        assert heading in text
    assert "curl -fsSL https://raw.githubusercontent.com/" in text
    assert not (ROOT / "docs").exists()
    assert not (ROOT / "mkdocs.yml").exists()
