from context_guard.compact.parsers import pytest_junitxml

SAMPLE_ALL_PASS = b"""<?xml version="1.0" encoding="utf-8"?>
<testsuites><testsuite name="pytest" tests="2" failures="0" errors="0">
<testcase classname="test_mod" name="test_a" time="0.001" />
<testcase classname="test_mod" name="test_b" time="0.001" />
</testsuite></testsuites>
"""

SAMPLE_ONE_FAILURE = b"""<?xml version="1.0" encoding="utf-8"?>
<testsuites><testsuite name="pytest" tests="3" failures="1" errors="0">
<testcase classname="test_mod" name="test_a" time="0.001" />
<testcase classname="test_mod" name="test_dup" file="test_mod.py" line="42" time="0.001">
<failure message="AssertionError: Expected one event, found two">assert 1 == 2
Expected one event, found two</failure>
</testcase>
<testcase classname="test_mod" name="test_c" time="0.001" />
</testsuite></testsuites>
"""

NOT_XML = b"not xml at all"
NOT_JUNIT_XML = b"<root><child/></root>"


def test_all_pass_reports_zero_failures():
    result, fragments = pytest_junitxml.parse(SAMPLE_ALL_PASS)
    assert result.status == "passed"
    assert result.tests == {"collected": 2, "passed": 2, "failed": 0}
    assert result.failures == []
    assert fragments == {}


def test_one_failure_identifies_name_file_line():
    result, fragments = pytest_junitxml.parse(SAMPLE_ONE_FAILURE)
    assert result.status == "failed"
    assert result.tests == {"collected": 3, "passed": 2, "failed": 1}
    assert len(result.failures) == 1
    failure = result.failures[0]
    assert failure.name == "test_dup"
    assert failure.file == "test_mod.py"
    assert failure.line == 42
    assert "Expected one event" in failure.diagnostic
    assert failure.evidence == "failure-1"
    assert "Expected one event, found two" in fragments["failure-1"]["content"]


def test_malformed_xml_returns_none():
    assert pytest_junitxml.parse(NOT_XML) is None


def test_non_junit_xml_returns_none():
    assert pytest_junitxml.parse(NOT_JUNIT_XML) is None
