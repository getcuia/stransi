"""A lightweight parser for ANSI escape code sequences."""

__version__ = "0.1.0"


__all__ = ["Ansi"]


from .ansi import Ansi
from .token import Attribute
