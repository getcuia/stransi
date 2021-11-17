"""A dedicated class for representing ANSI escape sequences."""

from __future__ import annotations

import re
from typing import Iterable, Iterator, Text, Type

import ochre

from ._misc import _isplit
from .token import GROUNDS, Attribute, Back, Escapable, Fore, Ground, Token

SEPARATOR = re.compile(r";")


class Escape(Text):
    """A single ANSI escape sequence."""

    def __repr__(self) -> Text:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}({super().__repr__()})"

    def tokens(self) -> Iterable[Token]:
        r"""
        Yield all tokens in this chunk.

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
        assert isescape(self), f"{self!r} is not an escape sequence"

        kind = self[-1]
        if params := self[2:-1]:
            for param in _isplit(params, SEPARATOR):
                yield Token(kind=kind, data=int(param))
        else:
            yield Token(kind=kind, data=0)

    def escapables(self) -> Iterable[Escapable]:
        """
        Decode a string of tokens into escapable objects.

        Examples
        --------
        >>> list(Escape("\x1b[1m").escapables())
        [<Attribute.BOLD: 1>]
        >>> list(Escape("\x1b[1;31m").escapables())  # doctest: +SKIP
        [Fore(color=Color(red=1.0, green=0.5826106699754192, blue=0.5805635742506021))]
        """
        tokens = self.tokens()
        assert isinstance(tokens, Iterator)
        while t := next(tokens, None):
            if t.issgr():
                # TODO: use a dispatch table instead of a switch-like construct.
                if t.data < 30 or 50 <= t.data < 76:
                    # Parse an SGR attribute token
                    try:
                        yield Attribute(t.data)
                    except ValueError:
                        yield t
                elif 30 <= t.data < 50 or 90 <= t.data < 108:

                    def _rgb(
                        t: Token, ts: Iterable[Token], cls: Type[Ground]
                    ) -> Iterable[Token | Ground]:
                        """Parse an RGB color."""
                        bits = next(ts)
                        if isinstance(bits, Token) and bits.data == 2:
                            # 24-bit RGB color

                            red, green, blue = (next(ts), next(ts), next(ts))
                            if not (
                                isinstance(red, Token)
                                and isinstance(green, Token)
                                and isinstance(blue, Token)
                            ):
                                raise ValueError(
                                    f"Expected three numbers after {cls.__name__} "
                                    f"but got {red}, {green}, {blue}"
                                )

                            yield cls(
                                ochre.RGB(
                                    red.data / 255, green.data / 255, blue.data / 255
                                )
                            )
                        else:
                            # Send them back, we don't support 256-color mode yet (and we
                            # might never do).
                            yield t
                            yield bits

                    if t.data in GROUNDS:
                        yield GROUNDS[t.data]
                    elif t.data == 38:
                        yield from _rgb(t, tokens, Fore)
                    elif t.data == 48:
                        yield from _rgb(t, tokens, Back)
                    else:
                        yield t
                else:
                    yield t
            else:
                # We currently don't support any other escape sequences.
                yield t


# TODO: remove all occurrences of 'chunk'
# chunks = iter(self.chunks())
# while t := next(chunks, None):
#     if isinstance(t, Token):
#         ts.append(t)
#     else:
#         if ts:
#             yield from decode(ts)
#             ts.clear()

#         yield t

# if ts:
#     yield from decode(ts)


def isescape(text: Text) -> bool:
    """Return True if text is an ANSI escape sequence."""
    return text.startswith("\N{ESC}[")
