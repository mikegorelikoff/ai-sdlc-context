from pathlib import Path
import subprocess
import sys

def test_all_contributor_skill_chat_scenarios():
    root = Path(__file__).resolve().parents[1]
    p = subprocess.run([sys.executable, str(root / ".claude/skills/ai-sdlc-shared-runtime/tests/test_chat_output.py")], cwd=root, capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
