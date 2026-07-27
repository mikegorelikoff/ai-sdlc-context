#!/usr/bin/env python3
"""Validate built-site structure and shared responsive presentation hooks."""

from __future__ import annotations

import sys
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SITE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "site"
if not SITE.is_absolute():
    SITE = ROOT / SITE


def main() -> int:
    errors: list[str] = []
    pages = sorted(SITE.rglob("*.html"))
    home = SITE / "index.html"
    start = SITE / "start-here/index.html"
    css = SITE / "assets/stylesheets/ai-sdlc.css"

    for path in (home, start, css):
        if not path.is_file():
            errors.append(f"missing rendered target: {path.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    html = home.read_text(encoding="utf-8")
    stylesheet = css.read_text(encoding="utf-8")
    required_home = [
        'name="viewport"',
        'data-md-color-scheme="default"',
        'data-md-color-scheme="slate"',
        'class="product-hero"',
        'class="product-hero__actions"',
        'class="workflow"',
        'class="path-cards"',
        'class="scope-panel"',
        'class="product-family"',
        "Get started",
        "See how it works",
    ]
    errors.extend(f"rendered Home missing {token}" for token in required_home if token not in html)

    labels = ["Home", "Start here", "How it works", "Guides", "Reference", "Project"]
    tab_block = re.search(r'<ul class="md-tabs__list">(.*?)</ul>', html, re.DOTALL)
    rendered_labels = []
    if tab_block:
        for link in re.findall(
            r'<a[^>]*class="md-tabs__link"[^>]*>(.*?)</a>',
            tab_block.group(1),
            re.DOTALL,
        ):
            rendered_labels.append(" ".join(re.sub(r"<[^>]+>", "", link).split()))
    if rendered_labels != labels:
        errors.append("rendered top navigation labels are missing or out of order")

    required_css = [
        "--ai-sdlc-header",
        "--ai-sdlc-cyan",
        "--ai-sdlc-indigo",
        ":focus-visible",
        "@media (max-width: 44.984375em)",
        "@media (prefers-reduced-motion: reduce)",
        ".product-hero",
        ".workflow-step",
        ".path-cards",
        ".scope-panel",
        ".product-family",
        ".status-badge",
    ]
    errors.extend(f"shared stylesheet missing {token}" for token in required_css if token not in stylesheet)
    if "@import url(" in stylesheet or "fonts.googleapis.com" in stylesheet:
        errors.append("shared stylesheet uses an external font")

    h1_count = html.count("<h1")
    if h1_count != 1:
        errors.append(f"rendered Home expected one H1, found {h1_count}")
    if len(pages) < 10:
        errors.append(f"rendered site contains only {len(pages)} HTML pages")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    longest = max(pages, key=lambda path: path.stat().st_size)
    print(
        f"Rendered site valid: {len(pages)} HTML pages; "
        f"longest page {longest.relative_to(SITE)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
