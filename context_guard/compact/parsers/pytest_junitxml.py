"""Preferred parser: pytest's native --junitxml machine-readable report."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from context_guard.compact.result import CompactResult, Failure, STATUS_FAILED, STATUS_PASSED


def _testsuite_elements(root: ET.Element) -> list[ET.Element]:
    if root.tag == "testsuites":
        return list(root.findall("testsuite"))
    return [root]


def parse(junit_xml: bytes) -> tuple[CompactResult, dict] | None:
    """Parse a --junitxml report. Returns None when the content is not valid junitxml."""
    try:
        root = ET.fromstring(junit_xml)
    except ET.ParseError:
        return None

    if root.tag not in ("testsuite", "testsuites"):
        return None

    collected = passed = failed = 0
    failures: list[Failure] = []
    fragments: dict = {}
    fragment_index = 1

    for suite in _testsuite_elements(root):
        for testcase in suite.findall("testcase"):
            collected += 1
            problem = testcase.find("failure")
            if problem is None:
                problem = testcase.find("error")
            if problem is None:
                passed += 1
                continue

            failed += 1
            name = testcase.get("name", "unknown")
            file_ = testcase.get("file") or testcase.get("classname", "unknown")
            try:
                line = int(testcase.get("line", "0"))
            except ValueError:
                line = 0
            diagnostic = problem.get("message", "").strip() or (problem.text or "").strip().splitlines()[0:1]
            if isinstance(diagnostic, list):
                diagnostic = diagnostic[0] if diagnostic else "no diagnostic message"

            fragment_id = f"failure-{fragment_index}"
            fragment_index += 1
            # Stored inline rather than as a byte offset into junit.xml: XML
            # entity escaping means the decoded element text does not appear
            # verbatim in the raw bytes, so an offset search would be unreliable.
            fragments[fragment_id] = {"content": (problem.text or "").strip()}

            failures.append(
                Failure(
                    name=name,
                    file=file_,
                    line=line,
                    diagnostic=diagnostic,
                    evidence=fragment_id,
                )
            )

    status = STATUS_FAILED if failed else STATUS_PASSED
    result = CompactResult(
        status=status,
        artifact="",
        tests={"collected": collected, "passed": passed, "failed": failed},
        failures=failures,
        notes=[] if collected else ["junitxml report contained no <testcase> elements"],
    )
    return result, fragments
