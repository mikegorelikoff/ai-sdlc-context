"""Context Guard CLI entrypoint."""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 compatibility
    import tomli as tomllib

from context_guard import decisions, engine, events
from context_guard import inventory as skill_inventory
from context_guard import receipts
from context_guard import claude_profile
from context_guard import claude_measurement
from context_guard import codex_profile
from context_guard import codex_measurement
from context_guard import quality
from context_guard.adapters import claude_code, codex
from context_guard.audit import jsonl
from context_guard.policy_config import (
    Policy,
    PolicyError,
    load as load_policy,
    skill_rule_conflicts,
)
from context_guard.policies import sessions
from context_guard.compact import artifact_store
from context_guard.compact import command_proxy
from context_guard.compact import ledger as compact_ledger
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

    rewritten = None
    if (
        args.provider == "claude"
        and event.event_name == "PreToolUse"
        and event.command
        and decision.status != decisions.BLOCK
    ):
        rewritten = command_proxy.rewrite(event.command)
    output = (
        claude_code.render_rewrite(event, rewritten)
        if rewritten is not None
        else adapter.render(decision)
    )
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
        print(
            f"Policy resolution: OK (version={policy.version}, mode={policy.mode}, "
            f"skill_rules={len(policy.skill_rules)}, conflicts={len(skill_rule_conflicts(policy))})"
        )
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
    summary["compact_runtime"] = compact_ledger.summarize(_repo_root())
    print(json.dumps(summary, indent=2))
    return 0


def cmd_inventory(args: argparse.Namespace) -> int:
    home = args.home or Path.home()
    result = skill_inventory.read_inventory(
        home,
        provider=args.provider,
        version=args.version,
        surface=args.surface,
    )
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0 if result.status == "supported" else 1


def cmd_receipt_inspect(args: argparse.Namespace) -> int:
    try:
        result = receipts.inspect_receipt(_repo_root(), args.run_id)
    except receipts.ReceiptError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


def cmd_receipt_delete(args: argparse.Namespace) -> int:
    try:
        deleted = receipts.delete_receipt(_repo_root(), args.run_id)
    except receipts.ReceiptError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps({"deleted": deleted, "run_id": args.run_id}, sort_keys=True))
    return 0 if deleted else 1


def cmd_receipt_prune(args: argparse.Namespace) -> int:
    try:
        result = receipts.prune_receipts(_repo_root(), retention_days=args.days)
    except receipts.ReceiptError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0


def _classifications(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        name, separator, classification = value.partition("=")
        if not separator or not name or not classification:
            raise claude_profile.ClaudeProfileError(
                "classifications must use NAME=CLASSIFICATION"
            )
        if name in result:
            raise claude_profile.ClaudeProfileError(f"duplicate classification for {name}")
        result[name] = classification
    return result


def _skill_paths(values: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        name, separator, path = value.partition("=")
        if not separator or not name or not path:
            raise codex_profile.CodexProfileError("skills must use NAME=ABSOLUTE_SKILL_PATH")
        if name in result:
            raise codex_profile.CodexProfileError(f"duplicate skill path for {name}")
        result[name] = Path(path)
    return result


def cmd_claude_profile_apply(args: argparse.Namespace) -> int:
    try:
        result = claude_profile.apply_profile(
            _repo_root(),
            args.settings,
            run_id=args.run_id,
            version=args.version,
            surface=args.surface,
            classifications=_classifications(args.classification),
            explicit_invocations=args.explicit,
            inventory_fingerprint=args.inventory_fingerprint,
            bypass=args.bypass,
        )
    except (claude_profile.ClaudeProfileError, receipts.ReceiptError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0 if result.status in {"reduced", "full-load"} else 1


def cmd_claude_profile_restore(args: argparse.Namespace) -> int:
    try:
        result = claude_profile.restore_profile(
            _repo_root(),
            args.settings,
            run_id=args.run_id,
            version=args.version,
            surface=args.surface,
        )
    except (claude_profile.ClaudeProfileError, receipts.ReceiptError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0 if result.status == "restored" else 1


def cmd_claude_profile_recover(args: argparse.Namespace) -> int:
    try:
        result = claude_profile.recover_profile(
            _repo_root(),
            args.settings,
            run_id=args.run_id,
            version=args.version,
            surface=args.surface,
        )
    except (claude_profile.ClaudeProfileError, receipts.ReceiptError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0 if result.status == "restored" else 1


def cmd_claude_profile_status(args: argparse.Namespace) -> int:
    print(json.dumps(claude_profile.profile_status(_repo_root(), args.settings), sort_keys=True))
    return 0


def cmd_codex_profile_apply(args: argparse.Namespace) -> int:
    try:
        result = codex_profile.apply_profile(
            _repo_root(),
            args.home,
            profile=args.profile,
            run_id=args.run_id,
            version=args.version,
            surface=args.surface,
            classifications=_classifications(args.classification),
            skill_paths=_skill_paths(args.skill),
            explicit_invocations=args.explicit,
            inventory_fingerprint=args.inventory_fingerprint,
            bypass=args.bypass,
        )
    except (
        claude_profile.ClaudeProfileError,
        codex_profile.CodexProfileError,
        receipts.ReceiptError,
        OSError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0 if result.status in {"reduced", "full-load"} else 1


def cmd_codex_profile_restore(args: argparse.Namespace) -> int:
    try:
        result = codex_profile.restore_profile(
            _repo_root(), args.home, profile=args.profile, run_id=args.run_id,
            version=args.version, surface=args.surface
        )
    except (codex_profile.CodexProfileError, receipts.ReceiptError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0 if result.status == "restored" else 1


def cmd_codex_profile_recover(args: argparse.Namespace) -> int:
    try:
        result = codex_profile.recover_profile(
            _repo_root(), args.home, profile=args.profile, run_id=args.run_id,
            version=args.version, surface=args.surface
        )
    except (codex_profile.CodexProfileError, receipts.ReceiptError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0 if result.status == "restored" else 1


def cmd_codex_profile_status(args: argparse.Namespace) -> int:
    try:
        result = codex_profile.profile_status(_repo_root(), args.home, args.profile)
    except codex_profile.CodexProfileError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


def _json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise quality.QualityError(f"{path} must contain a JSON object")
    return value


def cmd_quality_validate_suite(args: argparse.Namespace) -> int:
    try:
        manifests = [
            quality.QualityManifest.from_dict(_json_object(path)) for path in args.manifests
        ]
        validated = quality.validate_suite(manifests)
    except (OSError, json.JSONDecodeError, quality.QualityError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "valid": True,
                "fixtures": [manifest.fixture_id for manifest in validated],
                "manifest_fingerprints": [manifest.fingerprint for manifest in validated],
            },
            sort_keys=True,
        )
    )
    return 0


def cmd_quality_evaluate(args: argparse.Namespace) -> int:
    try:
        manifest = quality.QualityManifest.from_dict(_json_object(args.manifest))
        baseline = quality.AttemptEvidence.from_dict(_json_object(args.baseline))
        guarded = quality.AttemptEvidence.from_dict(_json_object(args.guarded))
        evaluation = quality.QualityLedger(_repo_root()).record_evaluation(
            manifest, baseline, guarded, run_id=args.run_id
        )
    except (OSError, json.JSONDecodeError, quality.QualityError, receipts.ReceiptError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(evaluation.to_dict(), sort_keys=True))
    return 0 if evaluation.valid else 1


def cmd_quality_authorize(args: argparse.Namespace) -> int:
    try:
        authorization = quality.QualityLedger(_repo_root()).authorize(args.pair_id)
    except quality.QualityError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(authorization.to_dict(), sort_keys=True))
    return 0 if authorization.allowed else 1


def cmd_quality_invalidate(args: argparse.Namespace) -> int:
    try:
        authorization = quality.QualityLedger(_repo_root()).invalidate(
            args.pair_id, run_id=args.run_id, reason_code=args.reason
        )
    except (quality.QualityError, receipts.ReceiptError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(authorization.to_dict(), sort_keys=True))
    return 0


def cmd_claude_measurement_extract(args: argparse.Namespace) -> int:
    try:
        result = claude_measurement.extract_run(
            _repo_root(),
            args.source,
            run_id=args.run_id,
            quality_pair_id=args.quality_pair,
            fixture_kind=args.fixture_kind,
            role=args.role,
            provider_version=args.version,
            model=args.model,
            session_id=args.session_id,
        )
        claude_measurement.MeasurementLedger(_repo_root()).record_run(result)
    except (
        claude_measurement.ClaudeMeasurementError,
        quality.QualityError,
        receipts.ReceiptError,
        OSError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0


def cmd_claude_measurement_pair(args: argparse.Namespace) -> int:
    try:
        baseline = claude_measurement.ClaudeRunMeasurement.from_dict(
            _json_object(args.baseline)
        )
        guarded = claude_measurement.ClaudeRunMeasurement.from_dict(
            _json_object(args.guarded)
        )
        result = claude_measurement.compare_pair(
            _repo_root(),
            baseline,
            guarded,
            pair_id=args.pair_id,
            execution_order=args.execution_order,
        )
        claude_measurement.MeasurementLedger(_repo_root()).record_pair(result)
    except (
        json.JSONDecodeError,
        quality.QualityError,
        claude_measurement.ClaudeMeasurementError,
        receipts.ReceiptError,
        OSError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0


def cmd_claude_measurement_qualify(args: argparse.Namespace) -> int:
    try:
        pairs = [
            claude_measurement.ClaudePairMeasurement.from_dict(_json_object(path))
            for path in args.pairs
        ]
        result = claude_measurement.qualify(
            _repo_root(), pairs, qualification_id=args.qualification_id
        )
        claude_measurement.MeasurementLedger(_repo_root()).record_qualification(result)
    except (
        json.JSONDecodeError,
        quality.QualityError,
        claude_measurement.ClaudeMeasurementError,
        receipts.ReceiptError,
        OSError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0 if result.passed else 1


def cmd_claude_measurement_ledger(args: argparse.Namespace) -> int:
    try:
        records = claude_measurement.MeasurementLedger(_repo_root()).records()
    except claude_measurement.ClaudeMeasurementError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(list(records), sort_keys=True))
    return 0


def _record_codex_run(result: codex_measurement.CodexRunMeasurement) -> int:
    codex_measurement.MeasurementLedger(_repo_root()).record_run(result)
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0


def cmd_codex_measurement_exact(args: argparse.Namespace) -> int:
    try:
        result = codex_measurement.extract_exact_run(
            _repo_root(), args.source, run_id=args.run_id,
            quality_pair_id=args.quality_pair, fixture_kind=args.fixture_kind,
            role=args.role, provider_version=args.version, model=args.model,
            thread_id=args.thread_id
        )
        return _record_codex_run(result)
    except (
        codex_measurement.CodexMeasurementError,
        quality.QualityError,
        receipts.ReceiptError,
        OSError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 1


def cmd_codex_measurement_cumulative(args: argparse.Namespace) -> int:
    try:
        result = codex_measurement.measure_cumulative_run(
            _repo_root(), run_id=args.run_id, quality_pair_id=args.quality_pair,
            fixture_kind=args.fixture_kind, role=args.role,
            provider_version=args.version, model=args.model,
            thread_id=args.thread_id, start_boundary_id=args.start_boundary,
            end_boundary_id=args.end_boundary,
            start_cached_input_tokens=args.start_cached_input,
            end_cached_input_tokens=args.end_cached_input
        )
        return _record_codex_run(result)
    except (
        codex_measurement.CodexMeasurementError,
        quality.QualityError,
        receipts.ReceiptError,
        OSError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 1


def cmd_codex_measurement_pair(args: argparse.Namespace) -> int:
    try:
        baseline = codex_measurement.CodexRunMeasurement.from_dict(
            _json_object(args.baseline)
        )
        guarded = codex_measurement.CodexRunMeasurement.from_dict(
            _json_object(args.guarded)
        )
        result = codex_measurement.compare_pair(
            _repo_root(), baseline, guarded, pair_id=args.pair_id,
            execution_order=args.execution_order
        )
        codex_measurement.MeasurementLedger(_repo_root()).record_pair(result)
    except (
        json.JSONDecodeError,
        codex_measurement.CodexMeasurementError,
        quality.QualityError,
        receipts.ReceiptError,
        OSError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0


def cmd_codex_measurement_qualify(args: argparse.Namespace) -> int:
    try:
        pairs = [
            codex_measurement.CodexPairMeasurement.from_dict(_json_object(path))
            for path in args.pairs
        ]
        result = codex_measurement.qualify(
            _repo_root(), pairs, qualification_id=args.qualification_id
        )
        codex_measurement.MeasurementLedger(_repo_root()).record_qualification(result)
    except (
        json.JSONDecodeError,
        codex_measurement.CodexMeasurementError,
        quality.QualityError,
        receipts.ReceiptError,
        OSError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), sort_keys=True))
    return 0 if result.passed else 1


def cmd_codex_measurement_ledger(args: argparse.Namespace) -> int:
    try:
        records = codex_measurement.MeasurementLedger(_repo_root()).records()
    except codex_measurement.CodexMeasurementError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(list(records), sort_keys=True))
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


def cmd_compact_run(args: argparse.Namespace) -> int:
    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        print("context-guard run -- <command> requires a command to run", file=sys.stderr)
        return 2
    result = command_proxy.run(_repo_root(), command)
    print(result.output)
    return result.exit_code


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

    # Migrate the flat assignments emitted by Context Guard 0.1.1. Codex
    # expects each event and command to be represented by nested array tables.
    for event_name in _CODEX_HOOK_EVENTS:
        legacy_assignment = re.compile(
            rf"(?m)^[ \t]*{re.escape(event_name)}[ \t]*="
            rf"[^\n]*{re.escape(_MARKER)}[^\n]*(?:\n|$)"
        )
        existing = legacy_assignment.sub("", existing)

    missing_events = [
        event_name
        for event_name in _CODEX_HOOK_EVENTS
        if not _codex_hook_is_installed(existing, event_name)
    ]
    if not missing_events:
        print(f"Codex hooks already installed in {path}")
        return 0

    lines = [existing.rstrip("\n")] if existing.strip() else []
    for event_name in missing_events:
        lines.extend(
            [
                "",
                f"[[hooks.{event_name}]]",
                "",
                f"[[hooks.{event_name}.hooks]]",
                'type = "command"',
                f'command = "context-guard hook codex"  # {_MARKER}',
            ]
        )
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(f"Installed Codex hooks into {path}")
    return 0


def _codex_hook_is_installed(config: str, event_name: str) -> bool:
    try:
        parsed = tomllib.loads(config)
    except tomllib.TOMLDecodeError:
        return False

    entries = parsed.get("hooks", {}).get(event_name, [])
    if not isinstance(entries, list):
        return False
    return any(
        isinstance(entry, dict)
        and any(
            isinstance(hook, dict)
            and hook.get("type") == "command"
            and hook.get("command") == "context-guard hook codex"
            for hook in entry.get("hooks", [])
        )
        for entry in entries
    )


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
    sub.add_parser("gain").set_defaults(func=cmd_report)

    inventory_parser = sub.add_parser("inventory")
    inventory_parser.add_argument("--provider", required=True, choices=["claude", "codex"])
    inventory_parser.add_argument("--version", required=True)
    inventory_parser.add_argument("--surface", required=True)
    inventory_parser.add_argument("--home", type=Path)
    inventory_parser.set_defaults(func=cmd_inventory)

    receipt_parser = sub.add_parser("receipt")
    receipt_sub = receipt_parser.add_subparsers(dest="receipt_command", required=True)
    receipt_inspect = receipt_sub.add_parser("inspect")
    receipt_inspect.add_argument("run_id")
    receipt_inspect.set_defaults(func=cmd_receipt_inspect)
    receipt_delete = receipt_sub.add_parser("delete")
    receipt_delete.add_argument("run_id")
    receipt_delete.set_defaults(func=cmd_receipt_delete)
    receipt_prune = receipt_sub.add_parser("prune")
    receipt_prune.add_argument("--days", type=int, default=receipts.DEFAULT_RETENTION_DAYS)
    receipt_prune.set_defaults(func=cmd_receipt_prune)

    claude_profile_parser = sub.add_parser("claude-profile")
    claude_profile_sub = claude_profile_parser.add_subparsers(
        dest="claude_profile_command", required=True
    )
    claude_apply = claude_profile_sub.add_parser("apply")
    claude_apply.add_argument("settings", type=Path)
    claude_apply.add_argument("--run-id", required=True)
    claude_apply.add_argument("--version", required=True)
    claude_apply.add_argument("--surface", default="cli")
    claude_apply.add_argument("--classification", action="append", default=[])
    claude_apply.add_argument("--explicit", action="append", default=[])
    claude_apply.add_argument("--inventory-fingerprint", required=True)
    claude_apply.add_argument("--bypass", action="store_true")
    claude_apply.set_defaults(func=cmd_claude_profile_apply)

    for name, func in (
        ("restore", cmd_claude_profile_restore),
        ("recover", cmd_claude_profile_recover),
    ):
        action = claude_profile_sub.add_parser(name)
        action.add_argument("settings", type=Path)
        action.add_argument("--run-id", required=True)
        action.add_argument("--version", required=True)
        action.add_argument("--surface", default="cli")
        action.set_defaults(func=func)

    claude_status = claude_profile_sub.add_parser("status")
    claude_status.add_argument("settings", type=Path)
    claude_status.set_defaults(func=cmd_claude_profile_status)

    codex_profile_parser = sub.add_parser("codex-profile")
    codex_profile_sub = codex_profile_parser.add_subparsers(
        dest="codex_profile_command", required=True
    )
    codex_apply = codex_profile_sub.add_parser("apply")
    codex_apply.add_argument("--home", required=True, type=Path)
    codex_apply.add_argument("--profile", required=True)
    codex_apply.add_argument("--run-id", required=True)
    codex_apply.add_argument("--version", required=True)
    codex_apply.add_argument("--surface", default="cli", choices=["cli", "app-server"])
    codex_apply.add_argument("--classification", action="append", default=[])
    codex_apply.add_argument("--skill", action="append", default=[])
    codex_apply.add_argument("--explicit", action="append", default=[])
    codex_apply.add_argument("--inventory-fingerprint", required=True)
    codex_apply.add_argument("--bypass", action="store_true")
    codex_apply.set_defaults(func=cmd_codex_profile_apply)
    for name, func in (
        ("restore", cmd_codex_profile_restore),
        ("recover", cmd_codex_profile_recover),
    ):
        action = codex_profile_sub.add_parser(name)
        action.add_argument("--home", required=True, type=Path)
        action.add_argument("--profile", required=True)
        action.add_argument("--run-id", required=True)
        action.add_argument("--version", required=True)
        action.add_argument("--surface", default="cli", choices=["cli", "app-server"])
        action.set_defaults(func=func)
    codex_status = codex_profile_sub.add_parser("status")
    codex_status.add_argument("--home", required=True, type=Path)
    codex_status.add_argument("--profile", required=True)
    codex_status.set_defaults(func=cmd_codex_profile_status)

    quality_parser = sub.add_parser("quality")
    quality_sub = quality_parser.add_subparsers(dest="quality_command", required=True)
    quality_suite = quality_sub.add_parser("validate-suite")
    quality_suite.add_argument("manifests", nargs="+", type=Path)
    quality_suite.set_defaults(func=cmd_quality_validate_suite)
    quality_evaluate = quality_sub.add_parser("evaluate")
    quality_evaluate.add_argument("--manifest", required=True, type=Path)
    quality_evaluate.add_argument("--baseline", required=True, type=Path)
    quality_evaluate.add_argument("--guarded", required=True, type=Path)
    quality_evaluate.add_argument("--run-id", required=True)
    quality_evaluate.set_defaults(func=cmd_quality_evaluate)
    quality_authorize = quality_sub.add_parser("authorize")
    quality_authorize.add_argument("pair_id")
    quality_authorize.set_defaults(func=cmd_quality_authorize)
    quality_invalidate = quality_sub.add_parser("invalidate")
    quality_invalidate.add_argument("pair_id")
    quality_invalidate.add_argument("--run-id", required=True)
    quality_invalidate.add_argument("--reason", required=True)
    quality_invalidate.set_defaults(func=cmd_quality_invalidate)

    measurement_parser = sub.add_parser("claude-measurement")
    measurement_sub = measurement_parser.add_subparsers(
        dest="claude_measurement_command", required=True
    )
    measurement_extract = measurement_sub.add_parser("extract")
    measurement_extract.add_argument("source", type=Path)
    measurement_extract.add_argument("--run-id", required=True)
    measurement_extract.add_argument("--quality-pair", required=True)
    measurement_extract.add_argument(
        "--fixture-kind", required=True, choices=sorted(claude_measurement.FIXTURE_KINDS)
    )
    measurement_extract.add_argument("--role", required=True, choices=["baseline", "guarded"])
    measurement_extract.add_argument("--version", required=True)
    measurement_extract.add_argument("--model", required=True)
    measurement_extract.add_argument("--session-id", required=True)
    measurement_extract.set_defaults(func=cmd_claude_measurement_extract)
    measurement_pair = measurement_sub.add_parser("pair")
    measurement_pair.add_argument("--baseline", required=True, type=Path)
    measurement_pair.add_argument("--guarded", required=True, type=Path)
    measurement_pair.add_argument("--pair-id", required=True)
    measurement_pair.add_argument(
        "--execution-order",
        required=True,
        choices=["baseline-first", "guarded-first"],
    )
    measurement_pair.set_defaults(func=cmd_claude_measurement_pair)
    measurement_qualify = measurement_sub.add_parser("qualify")
    measurement_qualify.add_argument("pairs", nargs="+", type=Path)
    measurement_qualify.add_argument("--qualification-id", required=True)
    measurement_qualify.set_defaults(func=cmd_claude_measurement_qualify)
    measurement_sub.add_parser("ledger").set_defaults(func=cmd_claude_measurement_ledger)

    codex_measurement_parser = sub.add_parser("codex-measurement")
    codex_measurement_sub = codex_measurement_parser.add_subparsers(
        dest="codex_measurement_command", required=True
    )

    def add_codex_measurement_context(action: argparse.ArgumentParser) -> None:
        action.add_argument("--run-id", required=True)
        action.add_argument("--quality-pair", required=True)
        action.add_argument(
            "--fixture-kind", required=True,
            choices=sorted(codex_measurement.FIXTURE_KINDS)
        )
        action.add_argument("--role", required=True, choices=["baseline", "guarded"])
        action.add_argument("--version", required=True)
        action.add_argument("--model", required=True)
        action.add_argument("--thread-id", required=True)

    codex_exact = codex_measurement_sub.add_parser("exact")
    codex_exact.add_argument("source", type=Path)
    add_codex_measurement_context(codex_exact)
    codex_exact.set_defaults(func=cmd_codex_measurement_exact)
    codex_cumulative = codex_measurement_sub.add_parser("cumulative")
    add_codex_measurement_context(codex_cumulative)
    codex_cumulative.add_argument("--start-boundary", required=True)
    codex_cumulative.add_argument("--end-boundary", required=True)
    codex_cumulative.add_argument("--start-cached-input", required=True, type=int)
    codex_cumulative.add_argument("--end-cached-input", required=True, type=int)
    codex_cumulative.set_defaults(func=cmd_codex_measurement_cumulative)
    codex_pair = codex_measurement_sub.add_parser("pair")
    codex_pair.add_argument("--baseline", required=True, type=Path)
    codex_pair.add_argument("--guarded", required=True, type=Path)
    codex_pair.add_argument("--pair-id", required=True)
    codex_pair.add_argument(
        "--execution-order", required=True,
        choices=["baseline-first", "guarded-first"]
    )
    codex_pair.set_defaults(func=cmd_codex_measurement_pair)
    codex_qualify = codex_measurement_sub.add_parser("qualify")
    codex_qualify.add_argument("pairs", nargs="+", type=Path)
    codex_qualify.add_argument("--qualification-id", required=True)
    codex_qualify.set_defaults(func=cmd_codex_measurement_qualify)
    codex_measurement_sub.add_parser("ledger").set_defaults(
        func=cmd_codex_measurement_ledger
    )

    test_parser = sub.add_parser("test")
    test_parser.add_argument("command", nargs=argparse.REMAINDER)
    test_parser.set_defaults(func=cmd_compact_test)

    run_parser = sub.add_parser("run")
    run_parser.add_argument("command", nargs=argparse.REMAINDER)
    run_parser.set_defaults(func=cmd_compact_run)

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
