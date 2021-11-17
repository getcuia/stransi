"""A string that can be disassembled into text and ANSI escape sequences."""

from __future__ import annotations

import re
from typing import Iterable, Text

from ._misc import _isplit
from .escape import Escape, isescape
from .token import Escapable


class Ansi(Text):
    r"""
    A string that can be disassembled into text and ANSI escape sequences.

    Examples
    --------
    >>> s = Ansi("\x1b[1;31mHello\x1b[m, world!")
    >>> list(s.escapes())
    [Escape('\x1b[1;31m'), 'Hello', Escape('\x1b[m'), ', world!']
    >>> list(s.escapables())
    [<Attribute.BOLD: 1>, Fore(color=Ansi256(1)), 'Hello', <Attribute.NORMAL: 0>, ', world!']
    """

    PATTERN = re.compile(r"(\N{ESC}\[[\d;]*[a-zA-Z])")

    def __repr__(self) -> Text:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}({super().__repr__()})"

    def escapes(self) -> Iterable[Escape | Text]:
        """Yield ANSI escapes and text in the order they appear."""
        for match in _isplit(self, self.PATTERN, include_separators=True):
            if not isescape(match):
                yield match
            else:
                yield Escape(match)

    # TODO: this method and the Escapable type have ugly names
    def escapables(self) -> Iterable[Escapable | Text]:
        """Yield escapables and text in the order they appear."""
        for escape in self.escapes():
            if not isinstance(escape, Escape):
                yield escape
            else:
                yield from escape.escapables()
