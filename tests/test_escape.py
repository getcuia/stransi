"""Tests for the Escape class."""


from unsi import Escape, SetAttribute
from unsi.attribute import Attribute


def test_escape_has_separator():
    """Ensure the class has a (constant) separator property."""
    assert hasattr(Escape, "SEPARATOR")


def test_vt100_escapes():
    """Ensure the classical VT100 escapes are supported."""

    def instr(t):
        return list(Escape(t).instructions())

    assert instr("\x1B[0m") == instr("\033[m")
    assert instr("\033[0m") == [SetAttribute(Attribute.NORMAL)]
    assert instr("\033[1m") == [SetAttribute(Attribute.BOLD)]
    assert instr("\033[4m") == [SetAttribute(Attribute.UNDERLINE)]
    assert instr("\033[5m") == [SetAttribute(Attribute.BLINK)]
    assert instr("\033[7m") == [SetAttribute(Attribute.REVERSE)]
