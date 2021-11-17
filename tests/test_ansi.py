"""Tests for strings containing ANSI escape sequences."""

from unsi import Ansi


def test_ansi_is_a_string():
    """Ansi is a string."""
    s = Ansi("Hello, world!")

    assert isinstance(s, Ansi)
    assert isinstance(s, str)
    assert s == "Hello, world!"
