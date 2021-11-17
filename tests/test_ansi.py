"""Tests for strings containing ANSI escape sequences."""

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


def test_ansi_can_be_iterated():
    """Ansi can be iterated."""
    s = Ansi("\N{ESC}[0;31;1mHello\x1b[m, \x1B[32mWorld!\N{ESC}[0m")

    assert list(s.escapables()) == [
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
