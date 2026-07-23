from context_guard import events
from context_guard.policies import commands
from context_guard.policy_config import Policy


def _policy():
    return Policy(
        mode="enforce",
        commands={"require_bounds": ["docker logs", "docker compose logs", "kubectl logs", "git log"]},
    )


def _command_event(command: str) -> events.Event:
    return events.Event(provider="claude-code", event_name="PreToolUse", operation_kind=events.SHELL_COMMAND, command=command)


def test_unbounded_docker_compose_logs_blocked():
    decision = commands.evaluate(_command_event("docker compose logs api"), _policy())
    assert decision.status == "block"
    assert any("--tail" in s for s in decision.suggestions)


def test_bounded_docker_compose_logs_allowed():
    decision = commands.evaluate(_command_event("docker compose logs --tail 200 api"), _policy())
    assert decision is None


def test_unbounded_kubectl_logs_blocked():
    decision = commands.evaluate(_command_event("kubectl logs my-pod"), _policy())
    assert decision.status == "block"


def test_bounded_kubectl_logs_allowed():
    decision = commands.evaluate(_command_event("kubectl logs --since 10m my-pod"), _policy())
    assert decision is None


def test_unbounded_git_log_blocked():
    decision = commands.evaluate(_command_event("git log -p"), _policy())
    assert decision.status == "block"


def test_bounded_git_log_allowed():
    decision = commands.evaluate(_command_event("git log -n 20"), _policy())
    assert decision is None


def test_unrelated_command_ignored():
    decision = commands.evaluate(_command_event("npm install"), _policy())
    assert decision is None


def test_non_shell_command_event_ignored():
    event = events.Event(provider="claude-code", event_name="PreToolUse", operation_kind=events.FILE_READ, path="a.txt")
    assert commands.evaluate(event, _policy()) is None
