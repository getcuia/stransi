"""ANSI text style attributes."""

from dataclasses import dataclass
from enum import Enum

from .instruction import Instruction


class Attribute(Enum):
    """An ANSI text style attribute."""

    # VT100, ECMA-48
    NORMAL = 0

    # VT100, ECMA-48
    BOLD = 1
    # ECMA-48
    NOT_BOLD = 22

    # FAINT = auto()
    # ITALIC = auto()

    # VT100, ECMA-48
    UNDERLINE = 4
    # ECMA-48
    NOT_UNDERLINE = 24

    # VT100, ECMA-48
    BLINK = 5
    # ECMA-48
    NOT_BLINK = 25

    # VT100, ECMA-48
    REVERSE = 7
    # ECMA-48
    NOT_REVERSE = 27


@dataclass
class SetAttribute(Instruction[Attribute]):
    """Instruction to set an ANSI text style attribute."""

    attribute: Attribute
