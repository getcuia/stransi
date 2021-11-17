"""A string-like object that is aware of ANSI escape sequences."""

from __future__ import annotations

import re
from typing import Iterable, Pattern, Text

from unsi.token import Token

PATTERN = re.compile(r"(\N{ESC}\[[\d;]*[a-zA-Z])")
SEPARATOR = re.compile(r";")


def _isplit(
    text: Text, pattern: Pattern[Text], include_separators: bool = False
) -> Iterable[Text]:
    r"""
    Split text into parts separated by the given pattern.

    This yields the text before the first match, then the match, then the text after
    the match and so on. If include_separators is False (the default), the separator is
    not included in the result. In any case, empty strings are never yielded.

    Examples
    --------
    >>> list(_isplit('a b  c', r'\s+'))
    ['a', 'b', 'c']
    >>> list(_isplit('a b  c', r'\s+', include_separators=True))
    ['a', ' ', 'b', '  ', 'c']
    """
    if isinstance(pattern, Text):
        pattern = re.compile(pattern)

    start, end = 0, 0
    for match in pattern.finditer(text):
        # Yield the text before the match.
        end = match.start()
        if piece := text[start:end]:
            yield piece

        # Yield the match.
        if include_separators and (piece := match.group(0)):
            yield piece

        # Update the start position.
        start = match.end()

    # Yield the text after the last match.
    if piece := text[start:]:
        yield piece


class Escape(str):
    """A string representing a single ANSI escape sequence."""

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
