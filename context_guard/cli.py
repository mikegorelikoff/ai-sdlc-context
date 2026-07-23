"""Context Guard CLI entrypoint."""

from __future__ import annotations

import argparse
import dataclasses
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from context_guard import decisions, engine, events
from context_guard.adapters import claude_code, codex
from context_guard.audit import jsonl
from context_guard.policy_config import DEFAULTS_PATH, REPO_CONFIG_RELATIVE, Policy, PolicyError, load as load_policy
from context_guard.policies import sessions
from context_guard.compact import artifact_store
from context_guard.compact import pipeline as compact_pipeline

_ADAPTERS = {"claude": claude_code, "codex": codex}

CLAUDE_SETTINGS_PATH = Path(".claude") / "settings.json"
CODEX_CONFIG_PATH = Path(".codex") / "config.toml"

_CLAUDE_HOOK_EVENTS = [
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
    "SessionStart",
    "PreCompact",
    "Stop",
]
_CODEX_HOOK_EVENTS = ["PreToolUse", "PostToolUse", "PreCompact", "PostCompact", "SessionStart", "Stop"]

_MARKER = "context-guard"


def _repo_root() -> Path:
    return Path.cwd()


def cmd_hook(args: argparse.Namespace) -> int:
    adapter = _ADAPTERS[args.provider]
    raw_stdin = sys.stdin.read()
    repo_root = _repo_root()
    try:
        payload = json.loads(raw_stdin) if raw_stdin.strip() else {}
        event = adapter.parse(payload)
    except Exception:  # noqa: BLE001 - fail open on any parse error
        print(json.dumps({}))
        _write_audit(repo_root, "unknown", "unknown", "unknown", "allow", "internal-error", "low")
        return 0

    if event.operation_kind == events.SESSION_LIFECYCLE:
        _handle_lifecycle(repo_root, event)
        print(json.dumps({}))
        return 0

    try:
        policy = load_policy(repo_root)
    except PolicyError:
        policy = Policy()

    has_range = adapter.has_bounded_range(event)
    decision = engine.evaluate(event, policy, has_range=has_range)

    if event.operation_kind == events.FILE_READ and event.path and event.session_id:
        sessions.record_read(repo_root, event.session_id, event.path)
        if decision.status == decisions.BLOCK or decision.would_have == decisions.BLOCK:
            sessions.record_prevented(repo_root, event.session_id, bytes_estimate=1)

    output = adapter.render(decision)
    print(json.dumps(output))

    _write_audit(
        repo_root,
        event.provider,
        event.event_name,
        event.operation_kind,
        decision.status,
        decision.rule_id,
        decision.estimated_risk,
        raw=event.command or event.path,
    )
    return 0


def _handle_lifecycle(repo_root: Path, event: events.Event) -> None:
    if event.event_name == "SessionStart":
        sessions.handle_session_start(repo_root, event.session_id, event.raw.get("timestamp", ""))
    elif event.event_name in ("PreCompact", "PostCompact"):
        sessions.handle_compaction(repo_root, event.session_id, event.raw.get("timestamp", ""))
    elif event.event_name == "Stop":
        sessions.handle_stop(repo_root, event.session_id)


def _write_audit(
    repo_root: Path,
    provider: str,
    event_name: str,
    operation: str,
    decision_status: str,
    rule_id: str | None,
    estimated_risk: str,
    raw: str | None = None,
) -> None:
    record = jsonl.build_record(
        provider=provider,
        event_name=event_name,
        operation=operation,
        decision_status=decision_status,
        rule_id=rule_id,
        estimated_risk=estimated_risk,
        repository=repo_root.name,
        raw_command_or_path=raw,
    )
    jsonl.append(jsonl.default_log_path(repo_root), record)


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        policy = load_policy(_repo_root())
    except PolicyError as exc:
        print(f"Invalid policy configuration: {exc}", file=sys.stderr)
        return 1
    print(f"Policy valid. Effective mode: {policy.mode}. Sources: {policy.sources or ['defaults only']}")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    repo_root = _repo_root()
    print(f"Python: {sys.version.split()[0]}")
    try:
        policy = load_policy(repo_root)
        print(f"Policy resolution: OK (mode={policy.mode})")
        for source in policy.sources or ["defaults only"]:
            print(f"  - {source}")
    except PolicyError as exc:
        print(f"Policy resolution: FAILED ({exc})")

    claude_path = repo_root / CLAUDE_SETTINGS_PATH
    codex_path = repo_root / CODEX_CONFIG_PATH
    print(f"Claude Code hooks installed: {claude_path.is_file() and _MARKER in claude_path.read_text(encoding='utf-8')}")
    print(f"Codex hooks installed: {codex_path.is_file() and _MARKER in codex_path.read_text(encoding='utf-8')}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    summary = jsonl.summarize(jsonl.default_log_path(_repo_root()))
    print(json.dumps(summary, indent=2))
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    repo_root = _repo_root()
    target = repo_root / REPO_CONFIG_RELATIVE
    if target.is_file():
        print(f"Policy already exists at {target}; not overwriting.", file=sys.stderr)
        return 0
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(DEFAULTS_PATH, target)
    print(f"Created default policy at {target}")
    return 0


def cmd_selftest(args: argparse.Namespace) -> int:
    fixtures_dir = Path(__file__).parent.parent / "tests" / "fixtures"
    manifest_path = fixtures_dir / "manifest.json"
    if not manifest_path.is_file():
        print("No fixture manifest found; nothing to test.", file=sys.stderr)
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    # Fixtures assert a fixed expected decision regardless of the ambient
    # repository policy mode, so evaluation is forced to `enforce` here.
    policy = dataclasses.replace(load_policy(_repo_root()), mode="enforce")
    failures = 0
    for case in manifest:
        adapter = _ADAPTERS[case["provider"]]
        event = adapter.parse(case["payload"])
        decision = engine.evaluate(event, policy, has_range=adapter.has_bounded_range(event))
        ok = decision.status == case["expected_decision"]
        status = "PASS" if ok else "FAIL"
        if not ok:
            failures += 1
        print(f"[{status}] {case['name']}: expected={case['expected_decision']} actual={decision.status}")

    print(f"{len(manifest) - failures}/{len(manifest)} fixtures passed")
    return 1 if failures else 0


def cmd_compact_test(args: argparse.Namespace) -> int:
    repo_root = _repo_root()
    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        print("context-guard test -- <command> requires a command to run", file=sys.stderr)
        return 2

    result, _artifact_id = compact_pipeline.run_compact_test(repo_root, command)
    print(json.dumps(result.to_dict()))
    return 0


def cmd_artifact_show(args: argparse.Namespace) -> int:
    repo_root = _repo_root()
    try:
        if args.fragment:
            content = artifact_store.read_fragment(repo_root, args.artifact_id, args.fragment)
            print(content)
        else:
            full = artifact_store.read_full(repo_root, args.artifact_id)
            for name, content in full["files"].items():
                if name in ("stdout.txt", "stderr.txt", "junit.xml"):
                    print(f"--- {name} ---")
                    print(content.decode("utf-8", errors="replace"))
    except (artifact_store.ArtifactNotFoundError, artifact_store.FragmentNotFoundError) as exc:
        print(f"Not found: {exc}", file=sys.stderr)
        return 1
    return 0


def _install(provider: str) -> int:
    repo_root = _repo_root()
    if provider == "claude":
        return _install_claude(repo_root)
    return _install_codex(repo_root)


def _install_claude(repo_root: Path) -> int:
    path = repo_root / CLAUDE_SETTINGS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    settings: dict[str, Any] = {}
    if path.is_file():
        try:
            settings = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            settings = {}

    hooks = settings.setdefault("hooks", {})
    for event_name in _CLAUDE_HOOK_EVENTS:
        entries = hooks.setdefault(event_name, [])
        command = f"context-guard hook claude"
        already_present = any(
            isinstance(entry, dict)
            and any(_MARKER in h.get("command", "") for h in entry.get("hooks", []) if isinstance(h, dict))
            for entry in entries
        )
        if not already_present:
            entries.append({"matcher": "*", "hooks": [{"type": "command", "command": command}]})

    path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    print(f"Installed Claude Code hooks into {path}")
    return 0


def _install_codex(repo_root: Path) -> int:
    path = repo_root / CODEX_CONFIG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.is_file() else ""
    if _MARKER in existing:
        print(f"Codex hooks already installed in {path}")
        return 0

    lines = [existing.rstrip("\n")] if existing.strip() else []
    lines.append("")
    lines.append("[hooks]")
    for event_name in _CODEX_HOOK_EVENTS:
        lines.append(f'{event_name} = "context-guard hook codex"  # {_MARKER}')
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(f"Installed Codex hooks into {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="context-guard")
    sub = parser.add_subparsers(dest="command", required=True)

    hook_parser = sub.add_parser("hook")
    hook_parser.add_argument("provider", choices=list(_ADAPTERS))
    hook_parser.set_defaults(func=cmd_hook)

    install_parser = sub.add_parser("install")
    install_parser.add_argument("provider", choices=list(_ADAPTERS))
    install_parser.set_defaults(func=lambda a: _install(a.provider))

    sub.add_parser("validate").set_defaults(func=cmd_validate)
    sub.add_parser("selftest").set_defaults(func=cmd_selftest)
    sub.add_parser("doctor").set_defaults(func=cmd_doctor)
    sub.add_parser("report").set_defaults(func=cmd_report)
    sub.add_parser("init").set_defaults(func=cmd_init)

    test_parser = sub.add_parser("test")
    test_parser.add_argument("command", nargs=argparse.REMAINDER)
    test_parser.set_defaults(func=cmd_compact_test)

    artifact_parser = sub.add_parser("artifact")
    artifact_sub = artifact_parser.add_subparsers(dest="artifact_command", required=True)
    show_parser = artifact_sub.add_parser("show")
    show_parser.add_argument("artifact_id")
    show_parser.add_argument("--fragment", default=None)
    show_parser.set_defaults(func=cmd_artifact_show)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
