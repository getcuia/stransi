"""Tests for the Ansi class."""

from typing import Text

import ochre

from unsi import Ansi, Attribute
from unsi.token import Fore


def test_ansi_is_a_string():
    """Ansi is a string."""
    s = Ansi("Hello, world!")

    assert isinstance(s, Ansi)
    assert isinstance(s, Text)
    assert s == "Hello, world!"


def test_ansi_can_be_concatenated():
    """Ansi can be concatenated."""
    s = Ansi("Hello, ") + Ansi("world!")

    # TODO: should we override __add__?
    # assert not isinstance(s, Ansi)
    assert isinstance(s, Text)
    assert s == "Hello, world!"


def test_ansi_can_be_iterated():
    """Ansi can be iterated."""
    s = Ansi("\N{ESC}[0;31;1mHello\x1b[m, \x1B[32mWorld!\N{ESC}[0m")

    assert list(s.instructions()) == [
        Attribute.NORMAL,
        Fore(color=ochre.Ansi256(1)),
        Attribute.BOLD,
        "Hello",
        Attribute.NORMAL,
        ", ",
        Fore(color=ochre.Ansi256(2)),
        "World!",
        Attribute.NORMAL,
    ]


def test_ansi_has_pattern():
    """Ensure the class has a (constant) pattern property."""
    assert hasattr(Ansi, "PATTERN")
