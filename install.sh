#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf 'Context Guard install failed: %s\n' "$1" >&2
  exit 1
}

command -v curl >/dev/null 2>&1 || fail "curl is required"
command -v python3 >/dev/null 2>&1 || fail "Python 3.10 or newer is required"

python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' ||
  fail "Python 3.10 or newer is required"

context_guard_install_root="${CONTEXT_GUARD_INSTALL_ROOT:-${HOME}/.local/share/context-guard}"
context_guard_bin_dir="${CONTEXT_GUARD_BIN_DIR:-${HOME}/.local/bin}"
context_guard_config_root="${CONTEXT_GUARD_CONFIG_ROOT:-${HOME}}"
context_guard_package="${CONTEXT_GUARD_PACKAGE:-https://github.com/mikegorelikoff/ai-sdlc-context/archive/refs/heads/main.zip}"
context_guard_venv="${context_guard_install_root}/venv"

mkdir -p "$context_guard_install_root" "$context_guard_bin_dir" "$context_guard_config_root"
python3 -m venv "$context_guard_venv" ||
  fail "Python venv support is required"

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
