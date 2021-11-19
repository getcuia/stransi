# stransi

A lightweight parser for ANSI escape code sequences.

## Features

-   [x] Any `CSI` sequences are tokenized.
-   [x] Escape sequences not supported by the terminal are emitted as token
        objects.
-   [x] Only one dependency: `ochre`.
-   [x] Python 3.8+
-   [-] Focus on coloring and styling: `SGR` (Select Graphic Rendition)
    parameters are parsed. stransi understands the following:
    -   [-] Text styles
    -   [-] Foreground colors
    -   [-] Background colors
-   [-] Works with what most ANSI/Unix terminals understand (xterm, Linux
    console, GNOME Terminal, etc.)
