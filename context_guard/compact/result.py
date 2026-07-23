"""The bounded compact result returned to the agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

STATUS_PASSED = "passed"
STATUS_FAILED = "failed"
STATUS_ERROR = "error"
STATUS_UNPARSED = "unparsed"


@dataclass
class Failure:
    name: str
    file: str
    line: int
    diagnostic: str
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "file": self.file,
            "line": self.line,
            "diagnostic": self.diagnostic,
            "evidence": self.evidence,
        }


@dataclass
class CompactResult:
    status: str
    artifact: str
    tests: dict[str, int] | None = None
    failures: list[Failure] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "tests": self.tests,
            "failures": [f.to_dict() for f in self.failures],
            "artifact": self.artifact,
            "notes": self.notes,
        }
