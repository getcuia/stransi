"""Tests for the Escape class."""


import ochre

from unsi import Escape, SetAttribute, SetColor
from unsi.attribute import Attribute
from unsi.color import ColorRole


def _instr(t):
    return list(Escape(t).instructions())


def test_escape_has_separator():
    """Ensure the class has a (constant) separator property."""
    assert hasattr(Escape, "SEPARATOR")


def test_vt100_escapes():
    """Ensure the classical VT100 escapes are supported."""

    assert _instr("\x1B[0m") == _instr("\033[m")
    assert _instr("\033[0m") == [SetAttribute(Attribute.NORMAL)]
    assert _instr("\033[1m") == [SetAttribute(Attribute.BOLD)]
    assert _instr("\033[4m") == [SetAttribute(Attribute.UNDERLINE)]
    assert _instr("\033[5m") == [SetAttribute(Attribute.BLINK)]
    assert _instr("\033[7m") == [SetAttribute(Attribute.REVERSE)]


def test_ecma48_colors():
    """Ensure the ECMA-48 colors are supported."""

    assert _instr("\x1B[30m") == [
        SetColor(role=ColorRole.FOREGROUND, color=ochre.Ansi256(0))
    ]
