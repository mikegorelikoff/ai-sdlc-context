from context_guard.compact.parsers import pytest_text

ALL_PASS_OUTPUT = b"""
collected 500 items

test_generated.py .................................................. [100%]

============================== 500 passed in 1.23s ==============================
"""

ONE_FAILURE_OUTPUT = b"""
collected 501 items

test_generated.py .......F......................................... [100%]

=================================== FAILURES ===================================
_______________________________ test_duplicate_callback ________________________

    def test_duplicate_callback():
>       assert 1 == 2, "Expected one event, found two"
E       AssertionError: Expected one event, found two

test_generated.py:1502: AssertionError
------------------------------- short test summary info -------------------------
FAILED test_generated.py::test_duplicate_callback - AssertionError: Expected one event, found two
======================= 1 failed, 500 passed in 1.40s =======================
"""

NOT_PYTEST_OUTPUT = b"some random tool output\nwith no recognizable summary line\n"


def test_all_pass_summary_parsed():
    result, fragments = pytest_text.parse(ALL_PASS_OUTPUT)
    assert result.status == "passed"
    assert result.tests == {"collected": 500, "passed": 500, "failed": 0}
    assert result.failures == []


def test_one_failure_identified():
    result, fragments = pytest_text.parse(ONE_FAILURE_OUTPUT)
    assert result.status == "failed"
    assert result.tests == {"collected": 501, "passed": 500, "failed": 1}
    assert len(result.failures) == 1
    failure = result.failures[0]
    assert failure.name == "test_duplicate_callback"
    assert failure.file == "test_generated.py"
    assert "AssertionError" in failure.diagnostic
    assert failure.evidence in fragments
    spec = fragments[failure.evidence]
    assert ONE_FAILURE_OUTPUT[spec["start"]:spec["end"]].decode() == (
        "FAILED test_generated.py::test_duplicate_callback - AssertionError: Expected one event, found two"
    )


def test_unrecognized_output_returns_none():
    assert pytest_text.parse(NOT_PYTEST_OUTPUT) is None
