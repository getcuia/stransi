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
        """Yield escapables and text in the order they appear."""
        for chunk in self.chunks():
            if isinstance(chunk, TokenChunk):
                yield from chunk.escapables()
            else:
                yield chunk
