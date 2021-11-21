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
    def up(steps: int = 1) -> CursorMove:
        """Move the cursor up by the given number of steps."""
        return CursorMove(relative=True, y=-steps)

    @staticmethod
    def down(steps: int = 1) -> CursorMove:
        """Move the cursor down by the given number of steps."""
        return CursorMove(relative=True, y=steps)

    @staticmethod
    def left(steps: int = 1) -> CursorMove:
        """Move the cursor left by the given number of steps."""
        return CursorMove(relative=True, x=-steps)

    @staticmethod
    def right(steps: int = 1) -> CursorMove:
        """Move the cursor right by the given number of steps."""
        return CursorMove(relative=True, x=steps)


@dataclass
class SetCursor(Instruction[CursorMove]):
    """Instruction to set the cursor position."""

    move: CursorMove
