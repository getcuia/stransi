"""Tests for the Ansi class."""

from typing import Text

import ochre

from unsi import Ansi, ColorRole, SetAttribute, SetColor
from unsi.attribute import Attribute


def test_ansi_is_a_string():
    """Ansi is a string."""
    ansi = Ansi("Hello, world!")

    assert isinstance(ansi, Ansi)
    assert isinstance(ansi, Text)
    assert ansi == "Hello, world!"


def test_ansi_can_be_concatenated():
    """Ansi can be concatenated."""
    ansi = Ansi("Hello, ") + Ansi("world!")

    # assert not isinstance(s, Ansi)
    assert isinstance(ansi, Text)
    assert ansi == "Hello, world!"


def test_ansi_can_be_iterated():
    """Ansi can be iterated."""
    ansi = Ansi("\N{ESC}[0;31;1mHello\x1b[m, \x1B[32mWorld!\N{ESC}[0m")

    assert list(ansi.instructions()) == [
        SetAttribute(Attribute.NORMAL),
        SetColor(role=ColorRole.FOREGROUND, color=ochre.Ansi256(1)),
        SetAttribute(Attribute.BOLD),
        "Hello",
        SetAttribute(Attribute.NORMAL),
        ", ",
        SetColor(role=ColorRole.FOREGROUND, color=ochre.Ansi256(2)),
        "World!",
        SetAttribute(Attribute.NORMAL),
    ]


def test_ansi_has_pattern():
    """Ensure the class has a (constant) pattern property."""
    assert hasattr(Ansi, "PATTERN")
