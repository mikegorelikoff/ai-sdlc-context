from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_docs import DOCS, EXPECTED_NAV, _top_nav, validate  # noqa: E402


class DocumentationContractTests(unittest.TestCase):
    def test_repository_documentation_contract(self) -> None:
        self.assertEqual(validate(), [])

    def test_exact_shared_navigation(self) -> None:
        config = (DOCS.parent / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertEqual(_top_nav(config), EXPECTED_NAV)

    def test_removed_sessions_command_is_not_published_as_usage(self) -> None:
        readme = (DOCS.parent / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("context-guard sessions", readme)


if __name__ == "__main__":
    unittest.main()
