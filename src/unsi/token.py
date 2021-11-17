r"""
Facilities for working with ANSI escape sequences as objects.

Representation of ANSI escape sequences.

The token is the hub of all things ANSI.





The parser understands the 24-bit format of RGB colors as per ISO-8613-6 (marked in
ECMA-48 as "reserved for future standardization"). This format is also supported
by Xterm and linux (although only approximately).

-   Foreground: `\033[38;2;<r>;<g>;<b>m` (ISO-8613-6, Xterm, linux)
-   Background: `\033[48;2;<r>;<g>;<b>m` (ISO-8613-6, Xterm, linux)

In short, the above should work fine in Xterm, KDE's Konsole, GNOME Terminal (in
fact all libvte-based terminals), iTerm and probably many others. Since ncurses
requires setting colors beforehand, the parser will keep track of the already set
colors and manage them accordingly.

Furthermore, the following are mapped to default colors:

-   `BLACK` (Black): `\033[30m` (ECMA-48, Xterm, linux)
-   `RED` (Red): `\033[31m` (ECMA-48, Xterm, linux)
-   `GREEN` (Green): `\033[32m` (ECMA-48, Xterm, linux)
-   `YELLOW` (Yellow): `\033[33m` (ECMA-48, Xterm, linux)
-   `BLUE` (Blue): `\033[34m` (ECMA-48, Xterm, linux)
-   `MAGENTA` (Magenta): `\033[35m` (ECMA-48, Xterm, linux)
-   `CYAN` (Cyan): `\033[36m` (ECMA-48, Xterm, linux)
-   `WHITE` (White): `\033[37m` (ECMA-48, Xterm, linux)

(Plus their background counterparts `\033[40m`-`\033[47m`.)

256-bit colors are presently not supported. Open an issue if you want to have
them.
"""


from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Text

import ochre

BLACK = ochre.Ansi256(0)
RED = ochre.Ansi256(1)
GREEN = ochre.Ansi256(2)
YELLOW = ochre.Ansi256(3)
BLUE = ochre.Ansi256(4)
MAGENTA = ochre.Ansi256(5)
CYAN = ochre.Ansi256(6)
WHITE = ochre.Ansi256(7)


class Escapable:
    """
    An object that corresponds to an ANSI escape sequence.

    This is not meant to be instantiated directly, but rather to be used as a
    base class for other classes.
    """

    def __str__(self) -> Text:
        """Return the ANSI escape sequence for this object."""
        return escape(encode(self))


@dataclass(frozen=True)
class Token(Escapable):
    """
    A token is a single ANSI escape.

    A complete ANSI escape sequence can require multiple tokens.
    This object is used as a representation of the ANSI escape sequence "language": we
    can make properties into tokens, and we can make strings into tokens.
    Furthermore, by having a token, we can make them into compact strings.
    """

    kind: Text
    data: int

    def issgr(self) -> bool:
        """
        Return True if this is a SGR escape sequence.

        Examples
        --------
        >>> Token(kind="m", data=0).issgr()
        True
        >>> Token(kind="H", data=0).issgr()
        False
        """
        return self.kind == "m"


def escape(ts: Token | Iterable[Token]) -> Text:
    r"""
    Return a compact ANSI escape sequence for the given token or tokens.

    Examples
    --------
    >>> escape(Token(kind="m", data=1))
    '\x1b[1m'
    >>> escape([Token(kind="m", data=38),
    ...         Token(kind="m", data=2),
    ...         Token(kind="m", data=255),
    ...         Token(kind="m", data=0),
    ...         Token(kind="m", data=0)])
    '\x1b[38;2;255;;m'
    >>> escape([Token(kind="m", data=1), Token(kind="H", data=0)])
    '\x1b[1m\x1b[H'
    """

    def _escape(kind: Text, data: int | Text) -> Text:
        return f"\N{ESC}[{data or ''}{kind}"

    if isinstance(ts, Token):
        return _escape(ts.kind, ts.data)

    # TODO: call encode(...) automatically if not a token using a map, but wait
    # for encode to stabilize
    #
    # tokens = map(encode, tokens)

    # TODO: make a fold/reduce
    first, *rest = ts
    res = _escape(first.kind, first.data)[:-1]
    kind = first.kind
    for token in rest:
        if token.kind == kind:
            res += f";{token.data or ''}"
        else:
            res += f"{kind}{_escape(token.kind, token.data)[:-1]}"
            kind = token.kind
    return f"{res}{kind}"


def encode(data: Escapable | Iterable[Token]) -> Iterable[Token]:
    """
    Encode an object into tokens if possible, otherwise yield the object as-is.

    Examples
    --------
    >>> list(encode(Attribute.BOLD))
    [Token(kind='m', data=1)]
    >>> list(encode(encode(Attribute.BOLD))) == list(encode(Attribute.BOLD))
    True
    """
    # TODO: dispatch table!
    if isinstance(data, Attribute):
        yield Token(kind="m", data=data.value)
    if isinstance(data, Ground):
        base = 40 if isinstance(data, Back) else 30
        if data.color == BLACK:
            yield Token(kind="m", data=base)
        elif data.color == RED:
            yield Token(kind="m", data=base + 1)
        elif data.color == GREEN:
            yield Token(kind="m", data=base + 2)
        elif data.color == YELLOW:
            yield Token(kind="m", data=base + 3)
        elif data.color == BLUE:
            yield Token(kind="m", data=base + 4)
        elif data.color == MAGENTA:
            yield Token(kind="m", data=base + 5)
        elif data.color == CYAN:
            yield Token(kind="m", data=base + 6)
        elif data.color == WHITE:
            yield Token(kind="m", data=base + 7)
        else:
            yield Token(kind="m", data=base + 8)
            yield Token(kind="m", data=2)

            red, green, blue = data.color.tobytes()
            yield Token(kind="m", data=red)
            yield Token(kind="m", data=green)
            yield Token(kind="m", data=blue)
    if isinstance(data, Token):
        yield data
    if isinstance(data, Iterable):
        yield from data


# TODO: create an hierarchy of classes for attributes and colors that is
# generic on a type parameter.


@dataclass(frozen=True)
class Ground(Escapable):
    """A ground color."""

    color: ochre.Color


@dataclass(frozen=True)
class Fore(Ground):
    """
    A terminal foreground color.

    Examples
    --------
    >>> Fore(RED)  # doctest: +SKIP
    Fore(color=Color(red=1.0, green=0.5826106699754192, blue=0.5805635742506021))
    """


@dataclass(frozen=True)
class Back(Ground):
    """
    A terminal background color.

    Examples
    --------
    >>> Back(RED)  # doctest: +SKIP
    Back(color=Color(red=1.0, green=0.5826106699754192, blue=0.5805635742506021))
    """


GROUNDS = {
    # Foregrounds
    30: Fore(BLACK),
    31: Fore(RED),
    32: Fore(GREEN),
    33: Fore(YELLOW),
    34: Fore(BLUE),
    35: Fore(MAGENTA),
    36: Fore(CYAN),
    37: Fore(WHITE),
    # Backgrounds
    40: Back(BLACK),
    41: Back(RED),
    42: Back(GREEN),
    43: Back(YELLOW),
    44: Back(BLUE),
    45: Back(MAGENTA),
    46: Back(CYAN),
    47: Back(WHITE),
}


class Attribute(Escapable, Enum):
    r"""
    ANSI escape sequence text style attributes.

    Examples
    --------
    >>> Attribute.BOLD
    <Attribute.BOLD: 1>
    >>> list(encode(Attribute.BOLD))
    [Token(kind='m', data=1)]
    >>> escape(encode(Attribute.BOLD))
    '\x1b[1m'
    """

    NORMAL = 0
    BOLD = 1
    FAINT = 2
    # ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    #
    REVERSE = 7
