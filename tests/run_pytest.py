"""Repository-local entrypoint for bounded validation runners."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


if __name__ == "__main__":
    raise SystemExit(pytest.main(sys.argv[1:]))
