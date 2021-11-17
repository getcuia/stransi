"""Generic ANSI instructions."""


from dataclasses import dataclass
from typing import Generic, TypeVar

from unsi.token import Token

T = TypeVar("T")


class Instruction(Generic[T]):
    """An ANSI instruction."""


@dataclass
class Unsupported(Instruction[Token]):
    """An instruction that we don't support."""

    token: Token
