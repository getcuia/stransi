"""A string that can be disassembled into text and ANSI escape sequences."""

from __future__ import annotations

import re
from typing import Iterable, Text

from ._misc import _CustomText, _isplit
from .escape import Escape, isescape
from .instruction import Instruction


class Ansi(_CustomText):
    r"""
    A string that can be disassembled into text and ANSI escape sequences.

    Examples
    --------
    >>> s = Ansi("\x1b[1;31mHello\x1b[m, world!")
    >>> list(s.escapes())
    [Escape('\x1b[1;31m'), 'Hello', Escape('\x1b[m'), ', world!']
    >>> list(s.instructions())  # doctest: +NORMALIZE_WHITESPACE
    [SetAttribute(attribute=<Attribute.BOLD: 1>),
     SetColor(role=<ColorRole.FOREGROUND: 30>,
     color=Ansi256(code=1)),
     'Hello',
     SetAttribute(attribute=<Attribute.NORMAL: 0>),
     ', world!']
    """

    PATTERN = re.compile(r"(\N{ESC}\[[\d;]*[a-zA-Z])")

    def escapes(self) -> Iterable[Escape | Text]:
        """Yield ANSI escapes and text in the order they appear."""
        for match in _isplit(self, self.PATTERN, include_separators=True):
            if not match:
                continue

            if not isescape(match):
                yield match
                continue
            yield Escape(match)

    def instructions(self) -> Iterable[Instruction | Text]:
        """Yield ANSI instructions and text in the order they appear."""
        for escape in self.escapes():
            if not isinstance(escape, Escape):
                yield escape
                continue
            yield from escape.instructions()
