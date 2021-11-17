"""Tests for the Escape class."""


from unsi import Escape


def test_escape_has_separator():
    """Ensure the class has a (constant) separator property."""
    assert hasattr(Escape, "SEPARATOR")
