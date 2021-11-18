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
from typing import Text


@dataclass
class Token:
    r"""
    A token is the basic unit of ANSI escape sequences.

    Examples
    --------
    >>> from unsi import Escape
    >>> list(Escape("\033[38;2;255;0;255m")
    ...      .tokens())  # doctest: +NORMALIZE_WHITESPACE
    [Token(kind='m', data=38),
     Token(kind='m', data=2),
     Token(kind='m', data=255),
     Token(kind='m', data=0),
     Token(kind='m', data=255)]
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
