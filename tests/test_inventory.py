from pathlib import Path

from context_guard.inventory import preflight, read_inventory


def _skill(home: Path, provider_dir: str, directory: str, name: str, body: str) -> Path:
    path = home / provider_dir / "skills" / directory / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nname: {name}\ndescription: fixture\n---\n{body}\n",
        encoding="utf-8",
    )
    return path


def test_preflight_support_matrix():
    assert preflight("claude", "2.1.218", "cli").status == "supported"
    assert preflight("codex", "0.144.1", "cli").status == "supported"
    assert preflight("codex", "0.144.1", "app-server").status == "supported"
    assert preflight("claude", "2.1.217", "cli").reason_code == "unsupported-version"
    assert preflight("codex", "0.144.0", "cli").reason_code == "unsupported-version"
    assert preflight("claude", "2.1.218", "desktop").reason_code == "unsupported-surface"
    assert preflight("codex", "not-semver", "cli").reason_code == "invalid-version"


def test_unchanged_inventory_is_stable_and_sorted(tmp_path: Path):
    _skill(tmp_path, ".claude", "zeta", "zeta", "z body")
    _skill(tmp_path, ".claude", "alpha", "alpha", "a body")

    first = read_inventory(
        tmp_path, provider="claude", version="2.1.218", surface="cli"
    )
    second = read_inventory(
        tmp_path, provider="claude", version="2.1.218", surface="cli"
    )

    assert first.status == "supported"
    assert first.fingerprint == second.fingerprint
    assert first.records == second.records
    assert [record.name for record in first.records] == ["alpha", "zeta"]
    assert all(len(record.metadata_digest) == 64 for record in first.records)
    assert all(len(record.body_digest) == 64 for record in first.records)


def test_codex_inventory_uses_codex_authoritative_root(tmp_path: Path):
    _skill(tmp_path, ".claude", "claude-only", "claude-only", "claude")
    codex_path = _skill(tmp_path, ".agents", "codex-only", "codex-only", "codex")
    _skill(tmp_path, ".codex", "stale", "stale", "stale")

    result = read_inventory(
        tmp_path, provider="codex", version="0.144.1", surface="app-server"
    )

    assert [record.name for record in result.records] == ["codex-only"]
    assert result.records[0].locator == str(codex_path.resolve())
    assert all(record.name != "stale" for record in result.records)
    assert result.records[0].identity.startswith("codex:user:codex-only:")


def test_duplicate_name_is_uncertain_and_returns_no_records(tmp_path: Path):
    _skill(tmp_path, ".agents", "one", "duplicate", "one")
    _skill(tmp_path, ".agents", "two", "duplicate", "two")

    result = read_inventory(
        tmp_path, provider="codex", version="0.144.1", surface="cli"
    )

    assert result.status == "uncertain"
    assert result.reason_code == "duplicate-skill-name"
    assert result.records == ()
    assert result.fingerprint is None


def test_missing_name_is_uncertain(tmp_path: Path):
    path = tmp_path / ".claude" / "skills" / "bad" / "SKILL.md"
    path.parent.mkdir(parents=True)
    path.write_text("---\ndescription: no name\n---\nbody\n", encoding="utf-8")

    result = read_inventory(
        tmp_path, provider="claude", version="2.1.218", surface="cli"
    )

    assert result.status == "uncertain"
    assert result.reason_code == "missing-skill-name"
    assert result.records == ()


def test_change_between_reads_is_stale(tmp_path: Path):
    path = _skill(tmp_path, ".claude", "changing", "changing", "first")

    def mutate() -> None:
        path.write_text(
            "---\nname: changing\ndescription: fixture\n---\nsecond\n",
            encoding="utf-8",
        )

    result = read_inventory(
        tmp_path,
        provider="claude",
        version="2.1.218",
        surface="cli",
        between_reads=mutate,
    )

    assert result.status == "uncertain"
    assert result.reason_code == "stale-inventory"
    assert result.records == ()
    assert result.fingerprint is None


def test_unsupported_preflight_does_not_read_inventory(tmp_path: Path):
    _skill(tmp_path, ".claude", "one", "one", "body")

    result = read_inventory(
        tmp_path, provider="claude", version="1.0.0", surface="cli"
    )

    assert result.status == "unsupported"
    assert result.reason_code == "unsupported-version"
    assert result.records == ()
    assert result.fingerprint is None
