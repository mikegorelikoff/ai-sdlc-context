"""Command rewrite and compact-output proxy for common developer commands."""

from __future__ import annotations

import json
import shlex
from dataclasses import dataclass
from pathlib import Path

from context_guard.compact import artifact_store, ledger
from context_guard.compact import runner as compact_runner

_SHELL_OPERATORS = {"&&", "||", ";", "|", "|&", "&", ">", ">>", "<"}
_TEST_BASES = {
    "pytest",
    "jest",
    "vitest",
    "rspec",
    "playwright",
    "cypress",
    "mocha",
    "ava",
    "phpunit",
}
_SEARCH_BASES = {"rg", "grep", "find", "fd", "ag", "ack"}
_FILE_BASES = {
    "ls",
    "tree",
    "cat",
    "head",
    "tail",
    "wc",
    "du",
    "df",
    "ps",
    "file",
    "stat",
    "jq",
    "yq",
}
_LINT_BASES = {
    "ruff",
    "mypy",
    "tsc",
    "eslint",
    "biome",
    "prettier",
    "rubocop",
    "golangci-lint",
}
_GIT_READS = {
    "status",
    "log",
    "diff",
    "show",
    "branch",
    "remote",
    "tag",
    "blame",
    "ls-files",
    "rev-parse",
}
_GH_READS = {"pr", "issue", "run", "workflow", "release", "repo"}
_BUILD_BASES = {"make", "cmake", "ninja", "xcodebuild"}
_DOTNET_ACTIONS = {"test", "build", "format", "list", "msbuild"}
_JAVA_ACTIONS = {"test", "build", "check", "compile", "package", "verify", "dependencies"}
_GO_ACTIONS = {"test", "vet", "list", "build", "version", "env"}


@dataclass(frozen=True)
class ProxyResult:
    output: str
    exit_code: int
    artifact_id: str


def _tokens(command: str) -> list[str] | None:
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None
    if not tokens or any(token in _SHELL_OPERATORS for token in tokens):
        return None
    return tokens


def supports(command: list[str]) -> bool:
    if not command:
        return False
    base = Path(command[0]).name
    if base == "context-guard":
        return False
    if base in _TEST_BASES | _SEARCH_BASES | _FILE_BASES | _LINT_BASES | _BUILD_BASES:
        return True
    if base == "git":
        return len(command) > 1 and command[1] in _GIT_READS
    if base in {"docker", "podman", "kubectl", "oc"}:
        if base in {"docker", "podman"}:
            return len(command) > 1 and (
                command[1] in {"ps", "images", "logs", "stats"}
                or command[1:3] == ["compose", "ps"]
                or command[1:3] == ["compose", "logs"]
            )
        return len(command) > 1 and command[1] in {"get", "describe", "logs", "top"}
    if base == "gh":
        return len(command) > 2 and command[1] in _GH_READS and command[2] in {
            "list",
            "view",
            "status",
            "checks",
        }
    if base == "cargo":
        return len(command) > 1 and command[1] in {
            "test",
            "check",
            "clippy",
            "build",
            "tree",
            "metadata",
        }
    if base == "go":
        return len(command) > 1 and command[1] in _GO_ACTIONS
    if base in {"gofmt", "staticcheck", "govulncheck"}:
        return base != "gofmt" or any(flag in command[1:] for flag in ("-d", "-l"))
    if base == "python" or base.startswith("python3"):
        return len(command) > 2 and command[1:3] in (
            ["-m", "pytest"],
            ["-m", "unittest"],
            ["-m", "mypy"],
        )
    if base in {"npm", "pnpm", "yarn"}:
        return len(command) > 1 and (
            command[1] == "test"
            or (command[1:3] == ["run", "test"])
            or command[1] in {"list", "outdated"}
            or (command[1] == "run" and len(command) > 2 and command[2] in {
                "build",
                "check",
                "lint",
                "test",
                "typecheck",
            })
        )
    if base == "npx":
        return len(command) > 1 and Path(command[1]).name in {
            "jest",
            "vitest",
            "playwright",
            "eslint",
            "tsc",
            "ruff",
            "mypy",
            "biome",
        }
    if base == "bun":
        return len(command) > 1 and command[1] in {
            "test",
            "build",
            "lint",
            "x",
            "run",
        }
    if base == "deno":
        return len(command) > 1 and command[1] in {"test", "check", "lint", "info"}
    if base == "node":
        return len(command) > 1 and command[1] in {"--test", "--check"}
    if base in {"pip", "pip3"}:
        return len(command) > 1 and command[1] in {"list", "show", "check"}
    if base == "uv":
        return len(command) > 1 and (
            command[1] == "tree"
            or command[1:3] in (["pip", "list"], ["pip", "show"], ["pip", "check"])
            or (
                command[1] == "run"
                and len(command) > 2
                and Path(command[2]).name
                in _TEST_BASES | _LINT_BASES | _BUILD_BASES
            )
        )
    if base == "poetry":
        return len(command) > 1 and (
            command[1] in {"show", "check"}
            or (
                command[1] == "run"
                and len(command) > 2
                and Path(command[2]).name in _TEST_BASES | _LINT_BASES
            )
        )
    if base in {"bundle", "bundler"}:
        return len(command) > 1 and (
            command[1] in {"list", "outdated", "check"}
            or command[1:3] == ["exec", "rspec"]
        )
    if base == "rake":
        return len(command) > 1 and command[1] == "test"
    if base == "swift":
        return len(command) > 1 and command[1] in {"test", "build", "package"}
    if base == "dotnet":
        return len(command) > 1 and command[1] in _DOTNET_ACTIONS
    if base in {"msbuild", "csc"}:
        return True
    if base in {"mvn", "mvnw", "gradle", "gradlew", "sbt"}:
        return len(command) > 1 and any(
            action in _JAVA_ACTIONS for action in command[1:] if not action.startswith("-")
        )
    if base in {"javac", "javadoc"}:
        return True
    if base == "terraform":
        return len(command) > 1 and command[1] in {"plan", "show", "validate", "output"}
    if base == "terragrunt":
        return len(command) > 1 and command[1] in {"plan", "show", "validate", "output"}
    if base == "pulumi":
        return len(command) > 1 and command[1] in {"preview", "stack"}
    if base == "helm":
        return len(command) > 1 and command[1] in {
            "list",
            "status",
            "get",
            "template",
            "lint",
        }
    if base == "aws":
        return len(command) > 2 and any(
            command[2].startswith(prefix)
            for prefix in ("describe-", "get-", "list-")
        )
    if base in {"az", "gcloud"}:
        return any(
            token in {"list", "show", "describe", "get", "status"}
            for token in command[1:4]
        )
    if base == "journalctl":
        return True
    if base == "systemctl":
        return len(command) > 1 and command[1] in {
            "status",
            "show",
            "list-units",
            "list-unit-files",
        }
    if base == "brew":
        return len(command) > 1 and command[1] in {"list", "outdated", "info", "deps"}
    if base == "apt":
        return len(command) > 1 and command[1] in {"list", "show"}
    if base == "dpkg":
        return len(command) > 1 and command[1] in {"-l", "--list", "-s", "--status"}
    return False


def rewrite(command: str) -> str | None:
    """Return a safe transparent rewrite for one simple supported shell command."""
    tokens = _tokens(command)
    if tokens is None or not supports(tokens):
        return None
    return f"context-guard run -- {command}"


def _truncate(line: str, limit: int = 300) -> str:
    return line if len(line) <= limit else line[: limit - 1] + "…"


def _deduplicate(lines: list[str]) -> list[str]:
    result: list[str] = []
    previous: str | None = None
    repeated = 0
    for line in lines:
        if line == previous:
            repeated += 1
            continue
        if repeated:
            result.append(f"[previous line repeated {repeated} times]")
        result.append(line)
        previous = line
        repeated = 0
    if repeated:
        result.append(f"[previous line repeated {repeated} times]")
    return result


def _filter(command: list[str], raw: bytes, exit_code: int) -> str:
    text = raw.decode("utf-8", errors="replace")
    lines = [_truncate(line.rstrip()) for line in text.splitlines() if line.strip()]
    base = Path(command[0]).name

    if base == "git" and len(command) > 1:
        if command[1] == "status":
            noise = (
                "On branch ",
                "Your branch is ",
                "Changes not staged",
                "Changes to be committed",
                "Untracked files:",
                "no changes added",
            )
            lines = [line for line in lines if not line.startswith(noise)]
        elif command[1] == "diff":
            lines = [line for line in lines if not line.startswith(("index ", "--- ", "+++ "))]
        lines = lines[:200]
    elif base in _SEARCH_BASES:
        lines = _deduplicate(lines)[:100]
    elif base in {"docker", "kubectl"} and "logs" in command[1:3]:
        lines = _deduplicate(lines)[:120]
    elif (
        base in _TEST_BASES
        or (base == "cargo" and len(command) > 1 and command[1] == "test")
        or (base == "go" and len(command) > 1 and command[1] == "test")
        or (base == "dotnet" and len(command) > 1 and command[1] == "test")
        or (
            base in {"mvn", "mvnw", "gradle", "gradlew", "sbt"}
            and "test" in command[1:]
        )
        or (base == "node" and "--test" in command[1:])
        or base in {"npm", "pnpm", "yarn", "npx"}
    ):
        if exit_code == 0:
            summaries = [
                line
                for line in lines
                if any(
                    marker in line.lower()
                    for marker in ("passed", "tests", "test result:", "ok", "success")
                )
            ]
            lines = summaries[-12:] or [f"ok: {' '.join(command)}"]
        else:
            failures = [
                line
                for line in lines
                if any(
                    marker in line.lower()
                    for marker in (
                        "fail",
                        "error",
                        "assert",
                        "panic",
                        "traceback",
                        "expected",
                        "received",
                    )
                )
            ]
            lines = (failures[:80] or lines[-80:])
    elif base in _LINT_BASES | _BUILD_BASES:
        lines = _deduplicate(lines)[:120]
    else:
        lines = _deduplicate(lines)[:120]

    return "\n".join(lines)


def run(repo_root: Path, command: list[str]) -> ProxyResult:
    """Execute a supported command, store raw evidence, and return compact text."""
    raw = compact_runner.run(command, repo_root)
    artifact_id = artifact_store.allocate(repo_root, "command")
    files = {
        "stdout.txt": raw.stdout,
        "stderr.txt": raw.stderr,
        "meta.json": json.dumps(
            {
                "command": command,
                "exit_code": raw.exit_code,
                "duration_seconds": raw.duration_seconds,
                "commit": raw.commit,
                "timestamp": raw.timestamp,
                "launch_error": raw.launch_error,
            }
        ).encode("utf-8"),
    }
    artifact_store.write(repo_root, "command", artifact_id, files)

    combined = raw.stdout + (b"\n" if raw.stdout and raw.stderr else b"") + raw.stderr
    compact = _filter(command, combined, raw.exit_code)
    reference = artifact_store.reference(artifact_id)
    output = f"{compact}\n[full output: {reference}]" if compact else f"[full output: {reference}]"
    raw_bytes = len(combined)
    compact_bytes = len(output.encode("utf-8"))
    ledger.record(
        repo_root,
        command=" ".join(command),
        commit=raw.commit,
        artifact_kind="command",
        artifact_id=artifact_id,
        status="passed" if raw.exit_code == 0 else "failed",
        summary={
            "raw_output_bytes": raw_bytes,
            "compact_output_bytes": compact_bytes,
            "estimated_input_tokens_saved": max(raw_bytes - compact_bytes, 0) // 4,
        },
        timestamp=raw.timestamp,
    )
    exit_code = raw.exit_code if raw.exit_code >= 0 else 127
    return ProxyResult(output, exit_code, artifact_id)
