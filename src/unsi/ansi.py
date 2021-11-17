"""A string-like object that is aware of ANSI escape sequences."""

from __future__ import annotations

import re
from typing import Iterable, Text

from ._misc import _isplit
from .escape import Escape
from .token import Token

PATTERN = re.compile(r"(\N{ESC}\[[\d;]*[a-zA-Z])")


class Ansi(str):
    """A string that is aware of its own embedded ANSI escape sequences."""

    def tokens(self) -> Iterable[Text | Token]:
        r"""
        Tokenize ANSI escape sequences from this string.

        This yields strings and escape sequences in the order they appear in
        the input.

        Examples
        --------
        >>> text = Ansi("I say: \x1b[38;2;0;255;0mhello, green!\x1b[m")
        >>> list(text.tokens())  # doctest: +NORMALIZE_WHITESPACE
        ['I say: ',
        Token(kind='m', data=38),
        Token(kind='m', data=2),
        Token(kind='m', data=0),
        Token(kind='m', data=255),
        Token(kind='m', data=0),
        'hello, green!',
        Token(kind='m', data=0)]
        """
        for piece in _isplit(self, PATTERN, include_separators=True):
            if piece:
                yield from Escape(piece).parse()
