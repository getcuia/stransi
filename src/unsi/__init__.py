"""A lightweight parser for ANSI escape code sequences."""

__version__ = "0.1.0"


__all__ = ["Ansi", "Escape", "SetAttribute", "SetColor"]


from .ansi import Ansi
from .attribute import SetAttribute
from .color import SetColor
from .escape import Escape
