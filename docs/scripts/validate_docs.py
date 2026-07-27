#!/usr/bin/env python3
"""Validate the shared documentation contract without extra dependencies."""

from __future__ import annotations

import re
import sys
from fnmatch import fnmatch
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
CONFIG = ROOT / "mkdocs.yml"
EXPECTED_SITE_NAME = "Context Guard"
EXPECTED_NAV = ["Home", "Start here", "How it works", "Guides", "Reference", "Project"]
README_HEADINGS = [
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
]
GUIDE_HEADINGS = [
    "## Goal",
    "## When to use it",
    "## Prerequisites",
    "## Procedure",
    "## Verify",
    "## Troubleshooting",
    "## Next step",
]


def _nav_paths(text: str) -> list[str]:
    nav = text.split("\nnav:\n", 1)[-1]
    return re.findall(
        r"^\s*-\s+[^:#]+:\s+([A-Za-z0-9_./-]+\.md)\s*$",
        nav,
        re.MULTILINE,
    )


def _top_nav(text: str) -> list[str]:
    nav = text.split("\nnav:\n", 1)[-1]
    return re.findall(r"^  - ([^:]+):", nav, re.MULTILINE)


def _hidden_patterns(text: str) -> list[str]:
    match = re.search(
        r"^not_in_nav:\s*\|\s*$\n(?P<body>.*?)(?=^nav:\s*$)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return []
    return [
        line.strip()
        for line in match.group("body").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def _links(text: str) -> set[str]:
    targets = set(re.findall(r"\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)", text))
    targets.update(re.findall(r"href=['\"]([^'\"]+)['\"]", text))
    return targets


def _slug(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value).strip().lower()
    value = re.sub(r"[`*_]", "", value)
    value = re.sub(r"[^\w\- ]", "", value)
    return re.sub(r"[\s-]+", "-", value).strip("-")


def _anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    anchors = {
        _slug(match.group(1))
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)
    }
    anchors.update(re.findall(r"<a\s+(?:[^>]*?\s)?id=['\"]([^'\"]+)['\"]", text))
    return anchors


def _resolve(source: Path, target: str) -> tuple[Path | None, str]:
    parsed = urlsplit(target)
    if parsed.scheme or target.startswith(("#", "mailto:", "javascript:", "data:")):
        return None, ""
    path_text = unquote(parsed.path)
    if not path_text:
        return source, unquote(parsed.fragment)
    candidate = (source.parent / path_text).resolve()
    if path_text.endswith("/"):
        candidate /= "index.md"
    return candidate, unquote(parsed.fragment)


def validate() -> list[str]:
    errors: list[str] = []
    config = CONFIG.read_text(encoding="utf-8") if CONFIG.is_file() else ""
    required_tokens = [
        f"site_name: {EXPECTED_SITE_NAME}",
        "strict: true",
        "assets/stylesheets/ai-sdlc.css",
        "navigation.tabs",
        "navigation.tabs.sticky",
        "navigation.indexes",
        "navigation.path",
        "navigation.prune",
        "navigation.top",
        "navigation.footer",
        "toc.follow",
        "search.suggest",
        "search.highlight",
        "content.code.copy",
    ]
    errors.extend(f"mkdocs.yml: missing {token}" for token in required_tokens if token not in config)
    if _top_nav(config) != EXPECTED_NAV:
        errors.append("mkdocs.yml: top-level navigation labels or order differ from the shared contract")

    nav_paths = _nav_paths(config)
    for relative in nav_paths:
        if not (DOCS / relative).is_file():
            errors.append(f"mkdocs.yml: missing navigation file {relative}")
    duplicates = sorted({path for path in nav_paths if nav_paths.count(path) > 1})
    if duplicates:
        errors.append("mkdocs.yml: duplicate navigation pages " + ", ".join(duplicates))

    pages = sorted(DOCS.rglob("*.md"))
    public = {path.relative_to(DOCS).as_posix() for path in pages}
    hidden = {
        relative
        for relative in public
        if any(fnmatch(relative, pattern) for pattern in _hidden_patterns(config))
    }
    unaccounted = sorted(public - set(nav_paths) - hidden)
    if unaccounted:
        errors.append("mkdocs.yml: pages are neither navigated nor not_in_nav: " + ", ".join(unaccounted))

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    positions = [readme.find(heading) for heading in README_HEADINGS]
    if any(position < 0 for position in positions):
        errors.append("README.md: required section missing")
    elif positions != sorted(positions):
        errors.append("README.md: required sections are out of order")
    if "## AI SDLC product family" not in readme:
        errors.append("README.md: product-family section missing")

    home = (DOCS / "index.md").read_text(encoding="utf-8")
    for token in (
        "[Get started](start-here/index.md)",
        "[See how it works](how-it-works/index.md)",
        "## AI SDLC product family",
        "independently installed",
    ):
        if token not in home:
            errors.append(f"docs/index.md: missing Home contract {token}")

    for path in pages:
        text = path.read_text(encoding="utf-8")
        h1_count = len(re.findall(r"^# [^#].*$", text, re.MULTILINE))
        if h1_count != 1:
            errors.append(f"{path.relative_to(ROOT)}: expected one H1, found {h1_count}")
        if path.parent == DOCS / "guides" and path.name != "index.md":
            missing = [heading for heading in GUIDE_HEADINGS if heading not in text]
            if missing:
                errors.append(f"{path.relative_to(ROOT)}: guide template missing {', '.join(missing)}")

    sources = pages + [ROOT / "README.md"]
    for source in sources:
        text = source.read_text(encoding="utf-8")
        for target in sorted(_links(text)):
            resolved, fragment = _resolve(source, target)
            if resolved is None:
                continue
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{source.relative_to(ROOT)}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{source.relative_to(ROOT)}: broken internal link {target}")
                continue
            if fragment and resolved.suffix == ".md" and fragment not in _anchors(resolved):
                errors.append(f"{source.relative_to(ROOT)}: unresolved anchor {target}")

    decision = (DOCS / "project/decision-log.md").read_text(encoding="utf-8")
    if "No existing public page moved" not in decision:
        errors.append("docs/project/decision-log.md: URL preservation decision missing")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Documentation valid: {len(list(DOCS.rglob('*.md')))} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
