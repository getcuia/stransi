"""Private miscellaneous utilities."""

from __future__ import annotations

import re
from typing import Iterable, Pattern, Text


def _isplit(
    text: Text, pattern: Pattern[Text], include_separators: bool = False
) -> Iterable[Text]:
    r"""
    Split text into parts separated by the given pattern.

    This yields the text before the first match, then the match, then the text
    after the match and so on. Empty strings are *never* yielded.

    If `include_separators` is False (the default), separators are not
    included in the result.

    Examples
    --------
    >>> list(_isplit('a b  c', ' '))
    ['a', 'b', 'c']
    >>> list(_isplit('a b  c', r'\s+', include_separators=True))
    ['a', ' ', 'b', '  ', 'c']
    """
    prev_end = 0
    for separator in re.finditer(pattern, text):
        # Yield the text before separator.
        if piece := text[prev_end : separator.start()]:
            yield piece

        # Yield separator.
        if include_separators and (piece := separator.group(0)):
            yield piece

        # Update the start position.
        prev_end = separator.end()

    # Yield the text after the last separator.
    if piece := text[prev_end:]:
        yield piece


class _CustomText(Text):
    """A custom string type for subclassing."""

    def __repr__(self) -> Text:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}({super().__repr__()})"