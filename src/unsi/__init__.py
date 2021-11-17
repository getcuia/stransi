"""A lightweight parser for ANSI escape code sequences."""

__version__ = "0.1.0"


__all__ = ["Ansi"]


from .ansi import Ansi

if __name__ == "__main__":
    s = Ansi("\N{ESC}[0;31mHello\x1b[m, \x1B[1;32mWorld!\N{ESC}[0m")
    for x in s.escapables():
        print(repr(x))
