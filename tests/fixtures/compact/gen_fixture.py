"""Generates test_generated.py: many passing tests plus one deliberate failure.

Not part of the pytest collection itself; run manually to regenerate the fixture.
"""
import pathlib

N = 500
lines = ["import pytest", ""]
for i in range(N):
    lines.append(f"def test_pass_{i}():")
    lines.append(f"    assert {i} == {i}")
    lines.append("")

lines.append("def test_duplicate_callback():")
lines.append('    assert 1 == 2, "Expected one event, found two"')
lines.append("")

pathlib.Path(__file__).parent.joinpath("test_generated.py").write_text("\n".join(lines), encoding="utf-8")
