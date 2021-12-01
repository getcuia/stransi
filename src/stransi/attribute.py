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
    DIM = 2
    # ECMA-48
    NEITHER_BOLD_NOR_DIM = 22

    # ECMA-48
    ITALIC = 3
    # ECMA-48
    NOT_ITALIC = 23

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

    # ECMA-48
    HIDDEN = 8
    NOT_HIDDEN = 28

    def is_on(self):
        """Return True if this attribute actually "turns on" an attribute."""
        return not self.is_off()

    def is_off(self):
        """Return True if this attribute actually "turns off" (resets) an attribute."""
        return self.value >= 22


@dataclass
class SetAttribute(Instruction[Attribute]):
    """Instruction to set an ANSI text style attribute."""

    attribute: Attribute
