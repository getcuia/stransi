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


def test_ecma48_8bit_colors():
    """Ensure the ECMA-48 colors are supported."""

    def _fore(color):
        return SetColor(ColorRole.FOREGROUND, color)

    def _back(color):
        return SetColor(ColorRole.BACKGROUND, color)

    assert _instr("\x1B[30m") == [_fore(ochre.Ansi256(0))]
    assert _instr("\x1B[31m") == [_fore(ochre.Ansi256(1))]
    assert _instr("\x1B[32m") == [_fore(ochre.Ansi256(2))]
    assert _instr("\x1B[33m") == [_fore(ochre.Ansi256(3))]
    assert _instr("\x1B[34m") == [_fore(ochre.Ansi256(4))]
    assert _instr("\x1B[35m") == [_fore(ochre.Ansi256(5))]
    assert _instr("\x1B[36m") == [_fore(ochre.Ansi256(6))]
    assert _instr("\x1B[37m") == [_fore(ochre.Ansi256(7))]

    assert _instr("\x1B[40m") == [_back(ochre.Ansi256(0))]
    assert _instr("\x1B[41m") == [_back(ochre.Ansi256(1))]
    assert _instr("\x1B[42m") == [_back(ochre.Ansi256(2))]
    assert _instr("\x1B[43m") == [_back(ochre.Ansi256(3))]
    assert _instr("\x1B[44m") == [_back(ochre.Ansi256(4))]
    assert _instr("\x1B[45m") == [_back(ochre.Ansi256(5))]
    assert _instr("\x1B[46m") == [_back(ochre.Ansi256(6))]
    assert _instr("\x1B[47m") == [_back(ochre.Ansi256(7))]
