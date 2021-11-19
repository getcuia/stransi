"""A dedicated class for representing ANSI escape sequences."""

from __future__ import annotations

import re
from typing import Iterable, Iterator, Text

import ochre

from ._misc import _CustomText, _isplit
from .attribute import Attribute, SetAttribute
from .color import ColorRole, SetColor
from .instruction import Instruction
from .token import Token
from .unsupported import Unsupported


def isescape(text: Text) -> bool:
    """Return True if text is an ANSI escape sequence."""
    return text.startswith("\N{ESC}[")


class Escape(_CustomText):
    """A single ANSI escape sequence."""

    SEPARATOR = re.compile(r";")
    ALL_ATTRIBUTE_CODES: set[int] = set(a.value for a in Attribute)
    ALL_FOREGROUND_CODES: set[int] = set(range(30, 40)) | set(range(90, 98))
    ALL_BACKGROUND_CODES: set[int] = set(range(40, 50)) | set(range(100, 108))
    ALL_COLOR_CODES: set[int] = ALL_FOREGROUND_CODES | ALL_BACKGROUND_CODES

    def tokens(self) -> Iterator[Token]:
        """Yield individual tokens from the escape sequence."""
        assert isescape(self), f"{self!r} is not an escape sequence"
        kind = self[-1]
        if params := self[2:-1]:
            for param in _isplit(params, self.SEPARATOR):
                yield Token(kind=kind, data=int(param))
            return
        yield Token(kind=kind, data=0)

    def instructions(self) -> Iterable[Instruction]:
        r"""
        Decode a string of tokens into escapable objects.

        Examples
        --------
        >>> list(Escape("\x1b[1m").instructions())
        [SetAttribute(attribute=<Attribute.BOLD: 1>)]
        >>> list(Escape("\x1b[5;44m")
        ...      .instructions())  # doctest: +NORMALIZE_WHITESPACE
        [SetAttribute(attribute=<Attribute.BLINK: 5>),
         SetColor(role=<ColorRole.BACKGROUND: 40>, color=Ansi256(4))]
        """
        tokens = self.tokens()
        while token := next(tokens, None):
            if not token.issgr():
                # We only support SGR (Select Graphic Rendition)
                yield Unsupported(token)
                continue

            if token.data in self.ALL_ATTRIBUTE_CODES:
                yield SetAttribute(Attribute(token.data))
                continue

            if token.data in self.ALL_COLOR_CODES:
                if token.data in self.ALL_FOREGROUND_CODES:
                    role = ColorRole.FOREGROUND
                elif token.data in self.ALL_BACKGROUND_CODES:
                    role = ColorRole.BACKGROUND

                if token.data in {38, 48}:
                    color_spec_token = next(tokens)
                    if color_spec_token.data == 5:
                        # 256-color support
                        color_index_token = next(tokens)
                        color = ochre.Ansi256(color_index_token.data)
                    elif color_spec_token.data == 2:
                        # 24-bit color support
                        red_token = next(tokens)
                        green_token = next(tokens)
                        blue_token = next(tokens)
                        color = ochre.RGB(
                            red_token.data / 255,
                            green_token.data / 255,
                            blue_token.data / 255,
                        )
                    else:
                        raise ValueError(f"Unsupported color spec {color_spec_token!r}")
                elif token.data in {39, 49}:
                    # Default color
                    color = None
                else:
                    # 8-color support

                    # The value of role is the index of the first color in
                    # the corresponding palette, that's why it works.
                    color_index = token.data - role.value
                    if token.data >= 90:
                        # Bright colors
                        color_index -= 52

                    color = ochre.Ansi256(color_index)

                yield SetColor(role=role, color=color)
                continue

            # Unsupported SGR code
            yield Unsupported(token)