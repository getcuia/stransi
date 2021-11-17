"""A dedicated class for representing sequences of ANSI escapes."""


from __future__ import annotations

from typing import Iterable, Iterator, Type

import ochre

from .token import GROUNDS, Attr, Back, Escapable, Fore, Ground, Token


# TODO: this should go to a dedicated object
def decode(ts: Iterable[Token]) -> Iterable[Escapable]:
    """
    Decode a string of tokens into objects if possible, otherwise yield the token as-is.

    Examples
    --------
    >>> list(decode([Token(kind="m", data=1)]))
    [<Attr.BOLD: 1>]
    >>> list(decode([Token(kind="m", data=31)]))  # doctest: +SKIP
    [Fore(color=Color(red=1.0, green=0.5826106699754192, blue=0.5805635742506021))]
    """
    if not isinstance(ts, Iterator):
        ts = iter(ts)
    while t := next(ts, None):
        if t.issgr():
            # TODO: use a dispatch table instead of a switch-like construct.
            if t.data < 30 or 50 <= t.data < 76:
                # Parse an SGR attribute token
                try:
                    yield Attr(t.data)
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
                            ochre.RGB(red.data / 255, green.data / 255, blue.data / 255)
                        )
                    else:
                        # Send them back, we don't support 256-color mode yet (and we
                        # might never do).
                        yield t
                        yield bits

                if t.data in GROUNDS:
                    yield GROUNDS[t.data]
                elif t.data == 38:
                    yield from _rgb(t, ts, Fore)
                elif t.data == 48:
                    yield from _rgb(t, ts, Back)
                else:
                    yield t
            else:
                yield t
        else:
            # We currently don't support any other escape sequences.
            yield t
