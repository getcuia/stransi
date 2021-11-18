"""Tests for the Escape class."""


from __future__ import annotations

from typing import Text

import ochre
import pytest

from unsi import Escape, SetAttribute, SetColor
from unsi.attribute import Attribute
from unsi.color import ColorRole
from unsi.instruction import Instruction


def _instr(t):
    return list(Escape(t).instructions())


def _fore(color):
    return SetColor(ColorRole.FOREGROUND, color)


def _back(color):
    return SetColor(ColorRole.BACKGROUND, color)


def test_escape_has_separator():
    """Ensure the class has a (constant) separator property."""
    assert hasattr(Escape, "SEPARATOR")


@pytest.mark.parametrize(
    "text, expected",
    [
        ("\033[m", _instr("\033[0m")),
        ("\033[0m", [SetAttribute(Attribute.NORMAL)]),
        ("\033[1m", [SetAttribute(Attribute.BOLD)]),
        ("\033[4m", [SetAttribute(Attribute.UNDERLINE)]),
        ("\033[5m", [SetAttribute(Attribute.BLINK)]),
        ("\033[7m", [SetAttribute(Attribute.REVERSE)]),
    ],
)
def test_vt100_escapes(text: Text, expected: list[Instruction[Attribute]]):
    """Ensure the classical VT100 escapes are supported."""
    assert _instr(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        # Foreground colors
        ("\x1B[30m", [_fore(ochre.Ansi256(0))]),
        ("\x1B[31m", [_fore(ochre.Ansi256(1))]),
        ("\x1B[32m", [_fore(ochre.Ansi256(2))]),
        ("\x1B[33m", [_fore(ochre.Ansi256(3))]),
        ("\x1B[34m", [_fore(ochre.Ansi256(4))]),
        ("\x1B[35m", [_fore(ochre.Ansi256(5))]),
        ("\x1B[36m", [_fore(ochre.Ansi256(6))]),
        ("\x1B[37m", [_fore(ochre.Ansi256(7))]),
        # Background colors
        ("\x1B[40m", [_back(ochre.Ansi256(0))]),
        ("\x1B[41m", [_back(ochre.Ansi256(1))]),
        ("\x1B[42m", [_back(ochre.Ansi256(2))]),
        ("\x1B[43m", [_back(ochre.Ansi256(3))]),
        ("\x1B[44m", [_back(ochre.Ansi256(4))]),
        ("\x1B[45m", [_back(ochre.Ansi256(5))]),
        ("\x1B[46m", [_back(ochre.Ansi256(6))]),
        ("\x1B[47m", [_back(ochre.Ansi256(7))]),
    ],
)
def test_ecma48_8bit_colors(text: Text, expected: list[Instruction[ochre.Color]]):
    """Ensure the ECMA-48 colors are supported."""
    assert _instr(text) == expected
