[![Python package](https://github.com/getcuia/stransi/actions/workflows/python-package.yml/badge.svg)](https://github.com/getcuia/stransi/actions/workflows/python-package.yml)

# stransi

<div align="center">
    <img class="hero" src="https://github.com/getcuia/stransi/raw/main/banner.jpg" alt="stransi" width="33%" />
</div>

> A lightweight parser for ANSI escape sequences.

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

## Credits

[Photo](https://github.com/getcuia/stransi/raw/main/banner.jpg) by
[Rabah Al Shammary](https://unsplash.com/@rabah_shammary?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
on
[Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).
