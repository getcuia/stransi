"""A lightweight parser for ANSI escape code sequences."""

__version__ = "0.1.0"


__all__ = ["Ansi", "Attribute", "ColorRole", "Escape", "SetAttribute", "SetColor"]


from .ansi import Ansi
from .attribute import Attribute, SetAttribute
from .color import ColorRole, SetColor
from .escape import Escape
