"""Tests for strings containing ANSI escape sequences."""

from typing import Text

from unsi import Ansi


def test_ansi_is_a_string():
    """Ansi is a string."""
    s = Ansi("Hello, world!")

    assert isinstance(s, Ansi)
    assert isinstance(s, Text)
    assert s == "Hello, world!"
