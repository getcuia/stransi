"""Clear screen regions."""

from dataclasses import dataclass
from enum import Enum

from .instruction import Instruction


class Clear(Enum):
    """Screen regions to clear."""

    SCREEN_AFTER = 0
    SCREEN_BEFORE = 1
    SCREEN = 2
    LINE_AFTER = 3
    LINE_BEFORE = 4
    LINE = 5


@dataclass
class SetClear(Instruction[Clear]):
    """Instruction to clear a screen region."""

    region: Clear
