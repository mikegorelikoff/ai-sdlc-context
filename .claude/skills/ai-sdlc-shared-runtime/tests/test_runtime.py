"""Exercise the actual packaged helpers from an isolated skill-only installation."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SKILLS = Path(__file__).resolve().parents[2]


class InstalledRuntimeTests(unittest.TestCase):
    def test_sdd_scaffold_is_independent_of_removed_shared_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ('ai-sdlc-shared-runtime', 'ai-sdlc-sdd'):
                shutil.copytree(SKILLS/name, root/'skills'/name, ignore=shutil.ignore_patterns('__pycache__'))
            script = root/'skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py'
            command = [sys.executable, str(script), str(root/'specs/001-fixture'), '--artifact', 'requirements', '--section', 'Goal', '--quick-flow']
            result = subprocess.run(command, input='Preserve explicit fixture evidence.\n', cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            artifact = root/'specs/001-fixture/requirements.md'
            self.assertIn('Preserve explicit fixture evidence.', artifact.read_text(encoding='utf-8'))
            self.assertFalse((root/'skills/_shared').exists())
            before = artifact.read_bytes()
            repeated = subprocess.run(command, input='Preserve explicit fixture evidence.\n', cwd=root, capture_output=True, text=True)
            self.assertEqual(repeated.returncode, 0, repeated.stdout + repeated.stderr)
            self.assertEqual(before, artifact.read_bytes())

if __name__ == '__main__':
    unittest.main()
