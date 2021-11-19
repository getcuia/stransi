"""Tests for the Ansi class."""

from typing import Text

import ochre
import pytest

from stransi import Ansi, SetAttribute, SetColor
from stransi.attribute import Attribute
from stransi.color import ColorRole


@pytest.fixture
def raw_example() -> Text:
    """Return a raw example string."""
    return "\x1b[0;31;1mHello\033[m, \x1B[32mWorld!\N{ESC}[0m"


@pytest.fixture
def example(raw_example: Text) -> Ansi:
    """Return an example Ansi string."""
    return Ansi(raw_example)


def test_ansi_has_pattern():
    """Ensure the class has a (constant) pattern property."""
    assert hasattr(Ansi, "PATTERN")


def test_ansi_is_a_string(example: Ansi, raw_example: Text):
    """Ansi is a string."""
    assert isinstance(example, Ansi)
    assert isinstance(example, Text)

    assert example == raw_example


def test_ansi_can_be_concatenated(example: Ansi, raw_example: Text):
    """Ansi can be concatenated."""
    double_example = example + example
    assert double_example == raw_example * 2

    # assert not isinstance(double_example, Ansi)
    assert isinstance(double_example, Text)


def test_ansi_can_be_iterated(example: Ansi):
    """Ansi can be iterated."""
    assert list(example.instructions()) == [
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
