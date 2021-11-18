"""An instruction that we don't support."""

from dataclasses import dataclass

from .instruction import Instruction
from .token import Token


@dataclass
class Unsupported(Instruction[Token]):
    """An instruction that we don't support."""

    token: Token
