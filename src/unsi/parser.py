r"""
A lightweight parser for ANSI escape code sequences.

Only a subset of the ANSI escape sequences are supported, namely a subset of
the SGR (Select Graphic Rendition) escape sequences.

This performs [lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis) in
general.










### Attributes and color

Since curses handles colors and attributes for us in a terminal-independent way,
directly using ANSI escape sequences is not possible. But since kay uses a
simple string output, colors and attributes are supported by a simple ANSI
escape sequence parser. A subset of ECMA-48 (the standard for ANSI escape
sequences) is supported:

**Attributes**:

-   `BOLD` (Extra bright/bold): `\033[1m` (ECMA-48, VT100, Xterm, linux)
-   `FAINT` (Half bright/dim): `\033[2m` (ECMA-48, Xterm, linux)
-   `UNDERLINE` (Underlined): `\033[4m` (ECMA-48, VT100, Xterm, linux)
-   `BLINK` (Blinking): `\033[5m` (ECMA-48, VT100, Xterm, linux)
-   `REVERSE` (Reverse video): `\033[7m` (ECMA-48, VT100, Xterm, linux)

_Note 0:_ references available:

-   [ECMA-48](https://www.ecma-international.org/publications-and-standards/standards/ecma-48/)
-   [VT100](https://vt100.net/docs/vt100-ug/chapter3.html#SGR)
-   [Xterm](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html)
-   [linux](https://man7.org/linux/man-pages/man4/console_codes.4.html) (the
    linux console, that is)

_Note 1:_ there's no support for curses' `A_STANDOUT` ("the best highlighting
mode available"), as it seems not to be mapped to a single escape sequence. On
Gnome Terminal, `A_STANDOUT` seems to be the same as `A_REVERSE`. If you're
interested in having this, open an issue and let's talk about it.

_Note 2:_ I plan on supporting italics (`\033[3m`, available in ECMA-48 and
Xterm) in the future. If you're interested in having this, open an issue and
let's talk about it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Text

from . import Ansi
from .token import Token


@dataclass
class Parser:
    """A parser for ANSI escape sequences."""

    tokens: Optional[Iterable[Text | Token]] = None

    def tokenize(self, text: Text) -> None:
        r"""
        Tokenize ANSI escape sequences in a string and store them in the parser.

        Examples
        --------
        >>> p = Parser()
        >>> p.tokenize("\x1B[38;2;0;255;0mHello, green!\x1b[m")
        """
        self.tokens = Ansi(text).tokens()


if __name__ == "__main__":
    p = Parser()
    p.tokenize("\N{ESC}[0;31mHello\x1b[m, \x1B[1;32mWorld!\N{ESC}[0m")
    for x in p.parse():
        print(repr(x))
