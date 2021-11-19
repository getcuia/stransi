"""Generic ANSI instructions."""


from typing import Generic, TypeVar

T = TypeVar("T")


class Instruction(Generic[T]):
    """An ANSI instruction."""
