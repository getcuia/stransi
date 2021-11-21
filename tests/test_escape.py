"""Tests for the Escape class."""


from __future__ import annotations

from typing import Optional, Text

import ochre
import pytest
from hypothesis import given
from hypothesis import strategies as st

from stransi import Escape, SetAttribute, SetColor, SetCursor
from stransi.attribute import Attribute
from stransi.color import ColorRole
from stransi.cursor import CursorMove
from stransi.instruction import Instruction
from stransi.token import Token

SINGLE_BYTE = st.integers(min_value=0, max_value=255)


def _instr(text):
    return list(Escape(text).instructions())


def _fore(color: Optional[ochre.Color] = None):
    return SetColor(ColorRole.FOREGROUND, color)


def _back(color: Optional[ochre.Color] = None):
    return SetColor(ColorRole.BACKGROUND, color)


def _rgb(red, green, blue):
    return ochre.RGB(red / 255, green / 255, blue / 255)


# GENERAL


def test_escape_has_separator():
    """Ensure the class has a (constant) separator property."""
    assert hasattr(Escape, "SEPARATOR")


def test_defaults_are_zero():
    """Ensure the default values are zero."""
    assert list(Escape("\033[H").tokens()) == [Token(kind="H", data=0)]
    assert list(Escape("\033[1H").tokens()) == [Token(kind="H", data=1)]
    assert list(Escape("\033[1;H").tokens()) == [
        Token(kind="H", data=1),
        Token(kind="H", data=0),
    ]
    assert list(Escape("\033[;1H").tokens()) == [
        Token(kind="H", data=0),
        Token(kind="H", data=1),
    ]
    assert list(Escape("\033[;H").tokens()) == [
        Token(kind="H", data=0),
        Token(kind="H", data=0),
    ]


# VT100


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
def test_vt100_attributes(text: Text, expected: list[Instruction[Attribute]]):
    """Ensure the classical VT100 attributes are supported."""
    assert _instr(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("\033[A", _instr("\033[0A")),
        ("\033[0A", _instr("\033[1A")),
        ("\033[1A", [SetCursor(CursorMove.up())]),
        ("\033[1A", [SetCursor(CursorMove.up(1))]),
        ("\033[2A", [SetCursor(CursorMove.up(2))]),
        ("\033[1B", [SetCursor(CursorMove.down())]),
        ("\033[1C", [SetCursor(CursorMove.right())]),
        ("\033[1D", [SetCursor(CursorMove.left())]),
        ("\033[H", [SetCursor(CursorMove.to_home())]),
        ("\033[1H", [SetCursor(CursorMove.to_home())]),
        ("\033[;1H", [SetCursor(CursorMove.to_home())]),
        ("\033[1;1H", [SetCursor(CursorMove.to_home())]),
        ("\033[2H", [SetCursor(CursorMove.to(x=1, y=0))]),
        # ("\033[;2H", [SetCursor(CursorMove.to(x=0, y=1))]),
        ("\033[2;2H", [SetCursor(CursorMove.to(x=1, y=1))]),
        ("\033[f", _instr("\033[H")),
    ],
)
def test_vt100_cursor_movements(text: Text, expected: list[Instruction[Attribute]]):
    """Ensure the classical VT100 cursor movements are supported."""
    assert _instr(text) == expected


# ECMA-48


@pytest.mark.parametrize(
    "text, expected",
    [
        ("\x1B[2m", [SetAttribute(Attribute.DIM)]),
        ("\x1B[3m", [SetAttribute(Attribute.ITALIC)]),
        ("\x1B[8m", [SetAttribute(Attribute.HIDDEN)]),
    ],
)
def test_ecma48_only_attributes(text: Text, expected: list[Instruction[Attribute]]):
    """Ensure some ECMA-48-only attributes are supported."""
    assert _instr(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("\x1B[22m", [SetAttribute(Attribute.NEITHER_BOLD_NOR_DIM)]),
        ("\x1B[23m", [SetAttribute(Attribute.NOT_ITALIC)]),
        ("\x1B[24m", [SetAttribute(Attribute.NOT_UNDERLINE)]),
        ("\x1B[25m", [SetAttribute(Attribute.NOT_BLINK)]),
        ("\x1B[27m", [SetAttribute(Attribute.NOT_REVERSE)]),
        ("\x1B[28m", [SetAttribute(Attribute.NOT_HIDDEN)]),
    ],
)
def test_ecma48_remove_attributes(text: Text, expected: list[Instruction[Attribute]]):
    """Ensure we can remove attributes as per ECMA-48."""
    assert _instr(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        # Regular foreground colors
        ("\x1B[30m", [_fore(ochre.Ansi256(0))]),
        ("\x1B[31m", [_fore(ochre.Ansi256(1))]),
        ("\x1B[32m", [_fore(ochre.Ansi256(2))]),
        ("\x1B[33m", [_fore(ochre.Ansi256(3))]),
        ("\x1B[34m", [_fore(ochre.Ansi256(4))]),
        ("\x1B[35m", [_fore(ochre.Ansi256(5))]),
        ("\x1B[36m", [_fore(ochre.Ansi256(6))]),
        ("\x1B[37m", [_fore(ochre.Ansi256(7))]),
        # Regular background colors
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
def test_ecma48_3bit_colors(text: Text, expected: list[Instruction[ochre.Color]]):
    """Ensure the ECMA-48 colors are supported."""
    assert _instr(text) == expected


@given(index=SINGLE_BYTE)
def test_ecma48_8bit_colors(index: int):
    """Ensure the ECMA-48 8-bit colors are supported."""
    assert _instr(f"\x1B[38;5;{index}m") == [_fore(ochre.Ansi256(index))]
    assert _instr(f"\x1B[48;5;{index}m") == [_back(ochre.Ansi256(index))]


@given(red=SINGLE_BYTE, green=SINGLE_BYTE, blue=SINGLE_BYTE)
def test_ecma48_24bit_colors(red: int, green: int, blue: int):
    """Ensure the ECMA-48 24-bit colors are supported."""
    assert _instr(f"\x1B[38;2;{red};{green};{blue}m") == [_fore(_rgb(red, green, blue))]
    assert _instr(f"\x1B[48;2;{red};{green};{blue}m") == [_back(_rgb(red, green, blue))]


def test_ecma48_default_colors():
    """Ensure the ECMA-48 default colors are supported."""
    assert _instr("\x1B[39m") == [_fore()]
    assert _instr("\x1B[49m") == [_back()]


# XTERM


@pytest.mark.parametrize(
    "text, expected",
    [
        # Bright foreground colors
        ("\x1B[90m", [_fore(ochre.Ansi256(8))]),
        ("\x1B[91m", [_fore(ochre.Ansi256(9))]),
        ("\x1B[92m", [_fore(ochre.Ansi256(10))]),
        ("\x1B[93m", [_fore(ochre.Ansi256(11))]),
        ("\x1B[94m", [_fore(ochre.Ansi256(12))]),
        ("\x1B[95m", [_fore(ochre.Ansi256(13))]),
        ("\x1B[96m", [_fore(ochre.Ansi256(14))]),
        ("\x1B[97m", [_fore(ochre.Ansi256(15))]),
        # Bright background colors
        ("\x1B[100m", [_back(ochre.Ansi256(8))]),
        ("\x1B[101m", [_back(ochre.Ansi256(9))]),
        ("\x1B[102m", [_back(ochre.Ansi256(10))]),
        ("\x1B[103m", [_back(ochre.Ansi256(11))]),
        ("\x1B[104m", [_back(ochre.Ansi256(12))]),
        ("\x1B[105m", [_back(ochre.Ansi256(13))]),
        ("\x1B[106m", [_back(ochre.Ansi256(14))]),
        ("\x1B[107m", [_back(ochre.Ansi256(15))]),
    ],
)
def test_xterm_bright_colors(text: Text, expected: list[Instruction[ochre.Color]]):
    """Ensure the XTerm bright colors are supported."""
    assert _instr(text) == expected
