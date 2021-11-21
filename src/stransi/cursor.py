"""Cursor movements."""

from __future__ import annotations

from dataclasses import dataclass

from .instruction import Instruction


@dataclass
class CursorMove:
    """A single cursor movement."""

    x: int = 0
    y: int = 0
    relative: bool = False

    @staticmethod
    def to(x: int = 0, y: int = 0) -> CursorMove:
        """
        Move the cursor to the given position.

        The position is relative to the zero-based origin of the screen
        (home position).
        """
        assert x >= 0, "x must be >= 0"
        assert y >= 0, "y must be >= 0"
        return CursorMove(x=x, y=y)

    @staticmethod
    def to_home() -> CursorMove:
        """Move the cursor to the home position."""
        return CursorMove(x=0, y=0)

    @staticmethod
    def up(steps: int = 1) -> CursorMove:
        """Move the cursor up by the given number of steps."""
        return CursorMove(y=-steps, relative=True)

    @staticmethod
    def down(steps: int = 1) -> CursorMove:
        """Move the cursor down by the given number of steps."""
        return CursorMove(y=steps, relative=True)

    @staticmethod
    def left(steps: int = 1) -> CursorMove:
        """Move the cursor left by the given number of steps."""
        return CursorMove(x=-steps, relative=True)

    @staticmethod
    def right(steps: int = 1) -> CursorMove:
        """Move the cursor right by the given number of steps."""
        return CursorMove(x=steps, relative=True)


@dataclass
class SetCursor(Instruction[CursorMove]):
    """Instruction to set the cursor position."""

    move: CursorMove
