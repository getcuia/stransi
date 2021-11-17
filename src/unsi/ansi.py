"""A string-like object that is aware of ANSI escape sequences."""

from __future__ import annotations

import re
from typing import Iterable, Text

from ._misc import _isplit
from .escape import Escape
from .escape_sequence import decode
from .token import GROUNDS, Escapable, Token

PATTERN = re.compile(r"(\N{ESC}\[[\d;]*[a-zA-Z])")


class Ansi(Text):
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
                # TODO: redo this iterating over escapes
                if piece.startswith("\N{ESC}"):
                    yield from Escape(piece).tokens()
                else:
                    yield piece

    def escapables(self) -> Iterable[Text | Escapable]:
        r"""
        Parse ANSI escape sequences from a string.

        This yields strings and attributes in order they appear in the input.
        Only a subset of the ANSI escape sequences are supported, namely a subset of
        the SGR (Select Graphic Rendition) escape sequences.
        If an escape sequence is not supported, it is yielded separately as a
        non-parsed Token.

        A SGR escape sequence is a sequence that starts with an Control Sequence
        Introducer (CSI) and ends with an `m`.
        A CSI escape sequence is a sequence that starts with an escape character
        (`\033` or `\x1B`) followed by an opening bracket (`[` or `\x5B`).

        Examples
        --------
        >>> s = Ansi(
        ...     "\N{ESC}[0;38;2;255;0;0mHello\x1b[m, "
        ...     "\x1B[1;38;2;0;255;0mWorld!\N{ESC}[0m"
        ... )
        >>> for code in s.escapables():
        ...     code  # doctest: +NORMALIZE_WHITESPACE
        <Attr.NORMAL: 0>
        Fore(color=RGB(red=1.0, green=0.0, blue=0.0))
        'Hello'
        <Attr.NORMAL: 0>
        ', '
        <Attr.BOLD: 1>
        Fore(color=RGB(red=0.0, green=1.0, blue=0.0))
        'World!'
        <Attr.NORMAL: 0>
        >>> s = Ansi("\x1B[38;2;0;255;0mHello, green!\x1b[m")
        >>> for code in s.escapables():
        ...     code
        Fore(color=RGB(red=0.0, green=1.0, blue=0.0))
        'Hello, green!'
        <Attr.NORMAL: 0>
        """
        if self.tokens is None:
            raise RuntimeError(
                "Parser has not been tokenized. "
                "tokenize() must be called before parse()"
            )

        ts: list[Token] = []
        tokens = iter(self.tokens())
        while t := next(tokens, None):
            if isinstance(t, Token):
                ts.append(t)
            else:
                if ts:
                    yield from decode(ts)
                    ts.clear()

                yield t

        if ts:
            yield from decode(ts)
