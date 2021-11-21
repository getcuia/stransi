[![Python package](https://github.com/getcuia/stransi/actions/workflows/python-package.yml/badge.svg)](https://github.com/getcuia/stransi/actions/workflows/python-package.yml)

# [stransi](https://github.com/getcuia/stransi#readme)

<div align="center">
    <img class="hero" src="https://github.com/getcuia/stransi/raw/main/banner.jpg" alt="stransi" width="33%" />
</div>

> I see a `\033[31m` door, and I want it painted `\033[30m`.

stransi is a lightweight parser for
[ANSI escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code). It
implements a string-like type that is aware of its own ANSI escape sequences,
and can be used to parse most of the common escape sequences used in terminal
output manipulation.

## Features

-   [x] Any `CSI` sequences are tokenized.
-   [x] Escape sequences not supported by the terminal are emitted as token
        objects.
-   [x] Only one dependency: `ochre`.
-   [x] Python 3.8+
-   [x] Focus on coloring and styling: `SGR` (Select Graphic Rendition)
        parameters are parsed. stransi understands the following:
    -   [x] Text styles
    -   [x] Foreground colors
    -   [x] Background colors
-   [x] Works with what most ANSI/Unix terminals understand (xterm, Linux
        console, GNOME Terminal, etc.)

See all the supported ANSI escape sequences in the [FEATURES.md](FEATURES.md).

## Credits

[Photo](https://github.com/getcuia/stransi/raw/main/banner.jpg) by
[Tien Vu Ngoc](https://unsplash.com/@tienvn3012?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
on
[Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).
