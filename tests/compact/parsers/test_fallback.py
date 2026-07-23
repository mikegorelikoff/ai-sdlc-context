from context_guard.compact.parsers import fallback


def test_launch_error_reported_without_fabricating_diagnosis():
    result, fragments = fallback.parse(-1, b"", b"", "No such file or directory: 'weirdtool'")
    assert result.status == "error"
    assert result.failures == []
    assert any("failed to launch" in note for note in result.notes)


def test_unrecognized_success_output_is_unparsed():
    result, fragments = fallback.parse(0, b"some tool output\nline 2\n", b"", None)
    assert result.status == "unparsed"
    assert result.failures == []
    assert "preview-stdout" in fragments


def test_unrecognized_nonzero_exit_is_error_without_invented_failure():
    result, fragments = fallback.parse(1, b"weird output", b"stderr text", None)
    assert result.status == "error"
    assert result.failures == []
    assert any("not recognized" in note for note in result.notes)
