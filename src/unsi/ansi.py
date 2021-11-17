"""A string-like object that is aware of ANSI escape sequences."""

from __future__ import annotations

import re
from typing import Iterable, Text

from ._misc import _isplit
from .escape import Escape, isescape
from .token import Escapable
from .token_chunk import TokenChunk

PATTERN = re.compile(r"(\N{ESC}\[[\d;]*[a-zA-Z])")


class Ansi(Text):
    """A string that is aware of its own embedded ANSI escape sequences."""

    def __repr__(self) -> Text:
        """Return a string representation of object."""
        return f"{self.__class__.__name__}({super().__repr__()})"

    def escapes(self) -> Iterable[Escape | Text]:
        """Yield ANSI escapes and text in the order they appear."""
        for piece in _isplit(self, PATTERN, include_separators=True):
            if not isescape(piece):
                yield piece
            else:
                yield Escape(piece)

    def chunks(self) -> Iterable[TokenChunk | Text]:
        """Yield token chunks and text in the order they appear."""
        for escape in self.escapes():
            if isinstance(escape, Escape):
                yield TokenChunk(escape)
            else:
                yield escape

    def escapables(self) -> Iterable[Escapable | Text]:
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
        <Attribute.NORMAL: 0>
        Fore(color=RGB(red=1.0, green=0.0, blue=0.0))
        'Hello'
        <Attribute.NORMAL: 0>
        ', '
        <Attribute.BOLD: 1>
        Fore(color=RGB(red=0.0, green=1.0, blue=0.0))
        'World!'
        <Attribute.NORMAL: 0>
        >>> s = Ansi("\x1B[38;2;0;255;0mHello, green!\x1b[m")
        >>> for code in s.escapables():
        ...     code
        Fore(color=RGB(red=0.0, green=1.0, blue=0.0))
        'Hello, green!'
        <Attribute.NORMAL: 0>
        """
        for chunk in self.chunks():
            if isinstance(chunk, TokenChunk):
                yield from chunk.escapables()
            else:
                yield chunk
