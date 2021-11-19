"""ANSI foreground and background colors."""


from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ochre import Color

from .instruction import Instruction


class ColorRole(Enum):
    """An ANSI color kinds: foreground or background."""

    # ECMA-48
    FOREGROUND = 30

    # ECMA-48
    BACKGROUND = 40


@dataclass
class SetColor(Instruction[Color]):
    """An ANSI instruction to set a foreground or background color."""

    role: ColorRole
    color: Optional[Color] = None
