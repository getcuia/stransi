# unsi

A lightweight parser for ANSI escape code sequences.

## Features

-   [ ] Any `CSI` sequences are tokenized.
-   [ ] Focus on coloring and styling: `SGR` (Select Graphic Rendition)
        parameters are parsed. unsi understands the following:
    -   [ ] Text styles
    -   [ ] Foreground colors
    -   [ ] Background colors
-   [ ] Escape sequences not supported by the terminal are emitted as token
        objects.
-   [ ] Keeps track of the current style and colors.
-   [ ] Only one dependency: `ochre`.
-   [ ] Python 3.8+
