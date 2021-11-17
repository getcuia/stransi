"""ANSI text style attributes."""

from enum import Enum, auto


class Attribute(Enum):
    r"""
    An ANSI text style attribute.

    Examples
    --------
    >>> Attribute.BOLD
    <Attribute.BOLD: 1>
    """

    # VT100
    NORMAL = 0

    # VT100
    BOLD = 1

    # FAINT = auto()
    # ITALIC = auto()

    # VT100
    UNDERLINE = 4

    # VT100
    BLINK = 5

    # VT100
    REVERSE = 7
