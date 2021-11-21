# Recognized ANSI Sequences

[ANSI escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code)
generally take the form:

    ESC [ <parameter> ; <parameter> ; ... <command>

where `ESC` is the escape character (`\033`), `[` is the opening bracket,
`<parameter>` is an integer, `;` is the semicolon separator, and `<command>` is
a single character. Zero or more parameters can be specified, but generally
assumed to be zero if unspecified. No spaces are allowed, they are shown here
only for clarity.

Only a subset of the ANSI escape sequences are supported by this library. See
the tables below for a complete list of currently supported (and planned to be
supported) ANSI escape sequences.

## CSI (Control Sequence Introducer) sequences

| Status? | Sequence        | Description                              | Colorama? | VT100? | ECMA-48? | XTerm? | Linux? | Windows? |
| :-----: | :-------------- | :--------------------------------------- | :-------: | :----: | :------: | :----: | :----: | :------: |
|   ✔️    | `ESC [ n A`     | Move cursor n lines up                   |    ✔️     |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ n B`     | Move cursor n lines down                 |    ✔️     |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ m C`     | Move cursor m characters forward         |    ✔️     |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ m D`     | Move cursor m characters backward        |    ✔️     |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|         | `ESC [ n ; m H` | Position cursor at m across, n down      |    ✔️     |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|         | `ESC [ n ; m f` | Basically the same as `ESC [ n ; m H`    |    ✔️     |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|         | `ESC [ mode J`  | Clear in screen (cursor stays in place)  |    ✔️     |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|         | `ESC [ mode K`  | Clear in line (cursor moves)             |    ✔️     |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|         | `ESC [ param m` | **Select graphic rendition** (see below) |    ✔️     |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |

Positions default to one, and are relative to the top left corner of the screen.
Most of these positioning commands have no effect if the cursor is already at
the edge of the screen.

Clearing functions default to mode `0`, which clears from cursor to the end of
the screen. Other available modes are: `1` (from cursor to the beginning of the
screen), and `2` (entire screen).

### SGR (Select Graphic Rendition, `m`) sequences

Multiple parameters can be specified, separated by semicolons:

    ESC [ <parameter> ; <parameter> ; ... m

See below for a list of supported parameters.

#### Styling attributes

| Status? | Sequence     | Description                  | Colorama? | VT100? | ECMA-48? | XTerm? | Linux? | Windows? |
| :-----: | :----------- | :--------------------------- | :-------: | :----: | :------: | :----: | :----: | :------: |
|   ✔️    | `ESC [ 0 m`  | **Reset rendition**          |    ✔️     |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 1 m`  | Bold or extra bright         |    ✔️     |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 2 m`  | Dim or half bright           |    ✔️     |        |    ✔️    |   ✔️   |   ✔️   |          |
|   ✔️    | `ESC [ 3 m`  | Italic text                  |           |        |    ✔️    |   ✔️   |        |          |
|   ✔️    | `ESC [ 4 m`  | (Singly) underlined text     |           |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 5 m`  | (Slowly) blinking text       |           |   ✔️   |    ✔️    |   ✔️   |   ✔️   |          |
|   ✔️    | `ESC [ 7 m`  | Reverse (negative) video     |           |   ✔️   |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 8 m`  | Invisible text               |           |        |    ✔️    |   ✔️   |        |          |
|         | `ESC [ 9 m`  | Strike-through (crossed-out) |           |        |    ✔️    |   ✔️   |        |          |
|   ✔️    | `ESC [ 22 m` | Reset brightness             |    ✔️     |        |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 23 m` | Reset italic                 |           |        |    ✔️    |   ✔️   |        |          |
|   ✔️    | `ESC [ 24 m` | Reset underline              |           |        |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 25 m` | Reset blinking (steady)      |           |        |    ✔️    |   ✔️   |   ✔️   |          |
|   ✔️    | `ESC [ 27 m` | Reset reverse (positive)     |           |        |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 28 m` | Reset invisible (visible)    |           |        |    ✔️    |   ✔️   |        |          |
|         | `ESC [ 29 m` | Reset strike-through         |           |        |    ✔️    |   ✔️   |        |          |

#### Colors

| Status? | Sequence                     | Description                | Colorama? | VT100? | ECMA-48? | XTerm? | Linux? | Windows? |
| :-----: | :--------------------------- | :------------------------- | :-------: | :----: | :------: | :----: | :----: | :------: |
|   ✔️    | `ESC [ 30-37 m`              | 8-color foreground         |    ✔️     |        |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 38 ; 5 ; s m`         | 256-color foreground       |           |        |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 38 ; 2 ; r ; g ; b m` | RGB color foreground       |           |        |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 39 m`                 | **Reset foreground color** |    ✔️     |        |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 40-47 m`              | 8-color background         |    ✔️     |        |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 48 ; 5 ; s m`         | 256-color background       |           |        |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 48 ; 2 ; r ; g ; b m` | RGB color background       |           |        |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 49 m`                 | **Reset background color** |    ✔️     |        |    ✔️    |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 90-97 m`              | Bright 8-color foreground  |           |        |          |   ✔️   |   ✔️   |    ✔️    |
|   ✔️    | `ESC [ 100-107 m`            | Bright 8-color background  |           |        |          |   ✔️   |   ✔️   |    ✔️    |

The 8-color set are defined in the following order: black, red, green, yellow,
blue, magenta, cyan, and white.

### Remarks

The supported sequences should work fine in most popular terminal emulators such
as KDE's Konsole, GNOME Terminal (in fact all libvte-based terminals), and
iTerm.

All other (unsupported) sequences are "ignored" (returned as unsupported
instructions).

## References and specifications

-   [Colorama](https://github.com/tartley/colorama#recognised-ansi-sequences)
-   [VT100](https://vt100.net/docs/vt100-ug/chapter3.html)
-   [ECMA-48](https://www.ecma-international.org/publications-and-standards/standards/ecma-48/)
-   [XTerm](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html)
-   [Linux console](https://man7.org/linux/man-pages/man4/console_codes.4.html)
-   [Windows console](https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences)
