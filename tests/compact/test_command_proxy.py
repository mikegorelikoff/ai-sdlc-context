import sys
from pathlib import Path

from context_guard.compact import artifact_store, command_proxy, ledger


def test_rewrite_supports_common_commands_and_skips_compound_commands():
    assert command_proxy.rewrite("git status") == "context-guard run -- git status"
    assert command_proxy.rewrite("pytest -q") == "context-guard run -- pytest -q"
    assert command_proxy.rewrite("rg needle src") == "context-guard run -- rg needle src"
    assert command_proxy.rewrite("git status && git diff") is None
    assert command_proxy.rewrite("git push") is None


def test_rewrite_supports_broad_read_build_test_and_infrastructure_families():
    commands = (
        "gh pr list",
        "fd '*.py' src",
        "cargo clippy",
        "go vet ./...",
        "pnpm run build",
        "uv pip list",
        "docker compose logs api",
        "kubectl get pods",
        "terraform plan",
        "pulumi preview",
        "aws ec2 describe-instances",
        "golangci-lint run",
        "python3 -m pytest -q",
        "uv run ruff check .",
        "poetry run pytest",
        "bundle exec rspec",
        "swift test",
        "podman ps",
        "oc get pods",
        "helm template app chart",
        "terragrunt plan",
        "az group list",
        "gcloud compute instances list",
        "journalctl -n 50",
        "systemctl status sshd",
        "brew outdated",
        "dotnet test Solution.sln",
        "dotnet format --verify-no-changes",
        "./mvnw verify",
        "./gradlew dependencies",
        "javac Main.java",
        "node --test",
        "bun run build",
        "deno lint",
        "go test ./...",
        "go vet ./...",
        "gofmt -d .",
        "staticcheck ./...",
        "govulncheck ./...",
    )
    for command in commands:
        assert command_proxy.rewrite(command) == f"context-guard run -- {command}"

    for command in ("terraform apply", "pulumi up", "npm install", "gh pr create"):
        assert command_proxy.rewrite(command) is None


def test_proxy_compacts_repeated_output_preserves_exit_and_stores_full(tmp_path: Path):
    script = "print('same\\n' * 20, end='')"

    result = command_proxy.run(tmp_path, [sys.executable, "-c", script])

    assert result.exit_code == 0
    assert "repeated 19 times" in result.output
    full = artifact_store.read_full(tmp_path, result.artifact_id)
    assert full["files"]["stdout.txt"].count(b"same") == 20
    assert ledger.summarize(tmp_path)["invocations"] == 1


def test_proxy_preserves_failure_exit_code(tmp_path: Path):
    result = command_proxy.run(
        tmp_path,
        [sys.executable, "-c", "import sys; print('ERROR boom'); sys.exit(7)"],
    )

    assert result.exit_code == 7
    assert "ERROR boom" in result.output
