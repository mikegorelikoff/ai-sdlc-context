#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf 'Context Guard install failed: %s\n' "$1" >&2
  exit 1
}

run_privileged() {
  if [[ "$(id -u)" -eq 0 ]]; then
    "$@"
  elif command -v sudo >/dev/null 2>&1; then
    sudo "$@"
  else
    fail "installing system dependencies requires root access or sudo"
  fi
}

select_python() {
  local candidate
  for candidate in python3 python3.14 python3.13 python3.12 python3.11 python3.10; do
    if command -v "$candidate" >/dev/null 2>&1 &&
      "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' \
        >/dev/null 2>&1; then
      context_guard_python="$(command -v "$candidate")"
      return 0
    fi
  done
  return 1
}

install_python_dependencies() {
  printf 'Python 3.10+ with venv was not found; installing system dependencies.\n'
  if command -v brew >/dev/null 2>&1; then
    brew install python
  elif command -v apt-get >/dev/null 2>&1; then
    run_privileged apt-get update
    run_privileged apt-get install -y python3 python3-venv
  elif command -v dnf >/dev/null 2>&1; then
    run_privileged dnf install -y python3
  elif command -v yum >/dev/null 2>&1; then
    run_privileged yum install -y python3
  elif command -v apk >/dev/null 2>&1; then
    run_privileged apk add python3 py3-pip
  elif command -v pacman >/dev/null 2>&1; then
    run_privileged pacman -Sy --noconfirm python python-pip
  elif command -v zypper >/dev/null 2>&1; then
    run_privileged zypper --non-interactive install python3 python3-pip
  else
    fail "Python 3.10 or newer with venv is required; install it manually"
  fi
}

if ! select_python; then
  install_python_dependencies
  select_python ||
    fail "the installed Python is older than 3.10 or is unavailable"
fi

context_guard_install_root="${CONTEXT_GUARD_INSTALL_ROOT:-${HOME}/.local/share/context-guard}"
context_guard_bin_dir="${CONTEXT_GUARD_BIN_DIR:-${HOME}/.local/bin}"
context_guard_config_root="${CONTEXT_GUARD_CONFIG_ROOT:-${HOME}}"
context_guard_package="${CONTEXT_GUARD_PACKAGE:-https://github.com/mikegorelikoff/ai-sdlc-context/archive/refs/heads/main.zip}"
context_guard_venv="${context_guard_install_root}/venv"

mkdir -p "$context_guard_install_root" "$context_guard_bin_dir" "$context_guard_config_root"
if ! "$context_guard_python" -m venv "$context_guard_venv"; then
  install_python_dependencies
  "$context_guard_python" -m venv "$context_guard_venv" ||
    fail "Python venv support could not be installed"
fi

"$context_guard_venv/bin/python" -m pip install \
  --disable-pip-version-check \
  --upgrade \
  "$context_guard_package"

ln -sfn "$context_guard_venv/bin/context-guard" "$context_guard_bin_dir/context-guard"

(
  cd "$context_guard_config_root"
  "$context_guard_bin_dir/context-guard" install claude
  "$context_guard_bin_dir/context-guard" install codex
  "$context_guard_bin_dir/context-guard" validate
)

printf '\nContext Guard installed.\n'
printf 'Command: %s\n' "$context_guard_bin_dir/context-guard"
printf 'Claude config: %s\n' "$context_guard_config_root/.claude/settings.json"
printf 'Codex config: %s\n' "$context_guard_config_root/.codex/config.toml"
if [[ ":${PATH}:" != *":${context_guard_bin_dir}:"* ]]; then
  printf 'Add this directory to PATH: %s\n' "$context_guard_bin_dir"
fi
