"""A string-like object representing a single ANSI escape sequence."""

from __future__ import annotations

import re
from typing import Iterable, Text

from ._misc import _isplit
from .token import Token

SEPARATOR = re.compile(r";")


class Escape(str):
    """A single ANSI escape sequence."""

    def parse(text: Text) -> Iterable[Text | Token]:
        r"""
        Parse a string into tokens if possible, otherwise yield the string as-is.

        Examples
        --------
        >>> list(Escape("\033[m").parse())
        [Token(kind='m', data=0)]
        >>> list(Escape("\x1b[1;31m").parse())
        [Token(kind='m', data=1), Token(kind='m', data=31)]
        >>> list(Escape("\x1b[38;2;30;60;90m").parse())  # doctest: +NORMALIZE_WHITESPACE
        [Token(kind='m', data=38),
            Token(kind='m', data=2),
            Token(kind='m', data=30),
            Token(kind='m', data=60),
            Token(kind='m', data=90)]
        """
        if not text.startswith("\N{ESC}["):
            yield text
        else:
            kind = text[-1]
            if params := text[2:-1]:
                for param in _isplit(params, SEPARATOR):
                    yield Token(kind=kind, data=int(param))
            else:
                yield Token(kind=kind, data=0)
