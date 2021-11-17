"""A string-like object representing a single ANSI escape sequence."""

from __future__ import annotations

import re
from typing import Iterable, Text

from ._misc import _isplit
from .token import Token

SEPARATOR = re.compile(r";")


class Escape(Text):
    """A single ANSI escape sequence."""

    def __repr__(self) -> Text:
        """Return a string representation of object."""
        return f"{self.__class__.__name__}({super().__repr__()})"

    def tokens(self) -> Iterable[Token]:
        r"""
        Parse a string into tokens if possible, otherwise yield the string as-is.

        Examples
        --------
        >>> list(Escape("\033[m").tokens())
        [Token(kind='m', data=0)]
        >>> list(Escape("\x1b[1;31m").tokens())
        [Token(kind='m', data=1), Token(kind='m', data=31)]
        >>> list(Escape("\x1b[38;2;30;60;90m").tokens())  # doctest: +NORMALIZE_WHITESPACE
        [Token(kind='m', data=38),
            Token(kind='m', data=2),
            Token(kind='m', data=30),
            Token(kind='m', data=60),
            Token(kind='m', data=90)]
        """
        # if not self.startswith("\N{ESC}["):
        #     raise ValueError(f"{self!r} is not an escape sequence")
        kind = self[-1]
        if params := self[2:-1]:
            for param in _isplit(params, SEPARATOR):
                yield Token(kind=kind, data=int(param))
        else:
            yield Token(kind=kind, data=0)
