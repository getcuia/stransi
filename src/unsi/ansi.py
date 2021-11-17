"""A string that is aware of its own embedded ANSI escape sequences."""

from __future__ import annotations

import re
from typing import Iterable, Text

from ._misc import _isplit
from .escape import Escape, isescape
from .token import Escapable

PATTERN = re.compile(r"(\N{ESC}\[[\d;]*[a-zA-Z])")


class Ansi(Text):
    """A string that is aware of its own embedded ANSI escape sequences."""

    def __repr__(self) -> Text:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}({super().__repr__()})"

    def escapes(self) -> Iterable[Escape | Text]:
        """Yield ANSI escapes and text in the order they appear."""
        for match in _isplit(self, PATTERN, include_separators=True):
            if not isescape(match):
                yield match
            else:
                yield Escape(match)

    def escapables(self) -> Iterable[Escapable | Text]:
        """Yield escapables and text in the order they appear."""
        for chunk in self.escapes():
            if not isinstance(chunk, Escape):
                yield chunk
            else:
                yield from chunk.escapables()
