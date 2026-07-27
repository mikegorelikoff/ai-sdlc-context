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


def test_readme_is_the_compact_documentation_entry_point():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    one_line_install = (
        "curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/"
        "ai-sdlc-context/main/install.sh | bash"
    )

    for heading in (
        "## Why use it?",
        "## Quick start",
        "## Expected first result",
        "## Product workflow",
        "## What it does and does not do",
        "## Documentation paths",
        "## AI SDLC product family",
        "## Security and privacy",
        "## Project status",
        "## Contributing",
        "## License",
    ):
        assert heading in text
    assert one_line_install in text
    assert one_line_install in (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
    assert one_line_install in (
        ROOT / "docs" / "start-here" / "install.md"
    ).read_text(encoding="utf-8")
    assert (ROOT / "docs" / "index.md").is_file()
    assert (ROOT / "mkdocs.yml").is_file()
