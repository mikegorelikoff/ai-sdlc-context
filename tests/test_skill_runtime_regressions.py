"""Keep contributor skills covered despite hidden directories and hyphenated names."""
from pathlib import Path
import subprocess
import sys
import unittest


class ContributorSkillTests(unittest.TestCase):
    def test_skill_local_regressions(self):
        root = Path(__file__).resolve().parents[1]
        skills = root / '.claude/skills'
        paths = sorted(skills.glob('*/tests/test*.py'))
        # Shared chat and determinism tests already have normal-suite bridges.
        paths = [path for path in paths if not (
            path.parent.parent.name == 'ai-sdlc-shared-runtime'
            and path.name in {'test_chat_output.py', 'test_determinism.py'}
        )]
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(path=path.relative_to(root).as_posix()):
                result = subprocess.run([sys.executable, str(path)], cwd=root,
                                        capture_output=True, text=True, timeout=120)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
