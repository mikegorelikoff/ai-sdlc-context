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


def test_installer_can_install_missing_python_and_venv_dependencies():
    text = INSTALLER.read_text(encoding="utf-8")

    for package_manager in ("brew", "apt-get", "dnf", "yum", "apk", "pacman", "zypper"):
        assert f"command -v {package_manager}" in text
    assert "python3-venv" in text
    assert "run_privileged" in text
    assert 'sudo "$@"' in text


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
    assert "Python 3.10 or newer with venv is required" in result.stderr
    assert "install it manually" in result.stderr


def test_installer_bootstraps_python_with_apt_when_missing(tmp_path: Path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    for command in ("bash", "ln", "mkdir"):
        source = Path("/bin") / command
        if not source.exists():
            source = Path("/usr/bin") / command
        os.symlink(source, fake_bin / command)

    fake_id = fake_bin / "id"
    fake_id.write_text("#!/bin/bash\nprintf '0\\n'\n", encoding="utf-8")
    fake_id.chmod(0o755)

    python_template = tmp_path / "python-template"
    python_template.write_text(
        """#!/bin/bash
if [[ "$1" == "-m" && "$2" == "venv" ]]; then
  /bin/mkdir -p "$3/bin"
  /bin/cp "$0" "$3/bin/python"
  /bin/chmod +x "$3/bin/python"
  printf '#!/bin/bash\\nexit 0\\n' >"$3/bin/context-guard"
  /bin/chmod +x "$3/bin/context-guard"
fi
exit 0
""",
        encoding="utf-8",
    )
    python_template.chmod(0o755)

    apt_log = tmp_path / "apt.log"
    fake_apt = fake_bin / "apt-get"
    fake_apt.write_text(
        """#!/bin/bash
printf '%s\\n' "$*" >>"$FAKE_APT_LOG"
if [[ "$1" == "install" ]]; then
  /bin/cp "$FAKE_PYTHON_TEMPLATE" "$FAKE_BIN/python3"
  /bin/chmod +x "$FAKE_BIN/python3"
fi
exit 0
""",
        encoding="utf-8",
    )
    fake_apt.chmod(0o755)

    result = subprocess.run(
        ["/bin/bash", str(INSTALLER)],
        env={
            "PATH": str(fake_bin),
            "HOME": str(tmp_path),
            "FAKE_APT_LOG": str(apt_log),
            "FAKE_BIN": str(fake_bin),
            "FAKE_PYTHON_TEMPLATE": str(python_template),
            "CONTEXT_GUARD_PACKAGE": str(ROOT),
        },
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "update" in apt_log.read_text(encoding="utf-8")
    assert "install -y python3 python3-venv" in apt_log.read_text(encoding="utf-8")
    assert (tmp_path / ".local" / "bin" / "context-guard").is_symlink()


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
