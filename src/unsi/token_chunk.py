"""A dedicated class for representing sequences of ANSI escapes."""


from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Type

import ochre

from unsi.escape import Escape

from .token import GROUNDS, Attribute, Back, Escapable, Fore, Ground, Token


@dataclass
class TokenChunk:
    """A meaningful token sequence."""

    escape: Escape

    def tokens(self) -> Iterable[Token]:
        """Yield all tokens in this chunk."""
        yield from self.escape.tokens()

    def escapables(self) -> Iterable[Escapable]:
        """
        Decode a string of tokens into escapable objects.

        Examples
        --------
        >>> list(TokenChunk(Escape("\x1b[1m")).escapables())
        [<Attribute.BOLD: 1>]
        >>> list(TokenChunk(Escape("\x1b[1;31m")).escapables())  # doctest: +SKIP
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
