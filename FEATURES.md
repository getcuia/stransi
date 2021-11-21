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

| Status? | Sequence        | Description                              | Colorama? |
| :-----: | :-------------- | :--------------------------------------- | :-------: |
|         | `ESC [ n A`     | Move cursor n lines up                   |    ✔️     |
|         | `ESC [ n B`     | Move cursor n lines down                 |    ✔️     |
|         | `ESC [ m C`     | Move cursor m characters forward         |    ✔️     |
|         | `ESC [ m D`     | Move cursor m characters backward        |    ✔️     |
|         | `ESC [ n ; m H` | Position cursor at m across, n down      |    ✔️     |
|         | `ESC [ n ; m f` | Basically the same as `ESC [ n ; m H`    |    ✔️     |
|         | `ESC [ mode J`  | Clear in screen (cursor moves)           |    ✔️     |
|         | `ESC [ mode K`  | Clear in line (cursor stays in place)    |    ✔️     |
|         | `ESC [ param m` | **Select graphic rendition** (see below) |    ✔️     |

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

| Status? | Sequence     | Description              | Colorama? | ECMA-48? | VT100? | XTerm? | Linux? | Windows? |
| :-----: | :----------- | :----------------------- | :-------: | :------: | :----: | :----: | :----: | :------: |
|   ✔️    | `ESC [ 0 m`  | **Reset all attributes** |    ✔️     |
|   ✔️    | `ESC [ 1 m`  | Extra bright or bold     |    ✔️     |    ✔️    |   ✔️   |   ✔️   |   ✔️   |    ?     |
|   ✔️    | `ESC [ 2 m`  | Half bright or dim       |    ✔️     |    ✔️    |        |   ✔️   |   ✔️   |    ?     |
|   ✔️    |              | Italic text              |           |
|   ✔️    | `ESC [ 4 m`  | Underlined text          |           |    ✔️    |   ✔️   |   ✔️   |   ✔️   |    ?     |
|   ✔️    | `ESC [ 5 m`  | Blinking text            |           |    ✔️    |   ✔️   |   ✔️   |   ✔️   |    ?     |
|   ✔️    | `ESC [ 7 m`  | Reverse video            |           |    ✔️    |   ✔️   |   ✔️   |   ✔️   |    ?     |
|   ✔️    | `ESC [ 22 m` | Reset brightness         |    ✔️     |
|   ✔️    |              | Reset italic             |           |
|   ✔️    |              | Reset underline          |           |
|   ✔️    |              | Reset blinking           |           |
|   ✔️    |              | Reset reverse video      |           |

#### Colors

| Status? | Sequence     | Description            | Colorama? | ECMA-48? | VT100? | XTerm? | Linux? | Windows? |
| :-----: | :----------- | :--------------------- | :-------: | :------: | :----: | :----: | :----: | :------: |
|   ✔️    | `ESC [ 30 m` | Black foreground       |    ✔️     |
|   ✔️    | `ESC [ 31 m` | Red foreground         |    ✔️     |
|   ✔️    | `ESC [ 32 m` | Green foreground       |    ✔️     |
|   ✔️    | `ESC [ 33 m` | Yellow foreground      |    ✔️     |
|   ✔️    | `ESC [ 34 m` | Blue foreground        |    ✔️     |
|   ✔️    | `ESC [ 35 m` | Magenta foreground     |    ✔️     |
|   ✔️    | `ESC [ 36 m` | Cyan foreground        |    ✔️     |
|   ✔️    | `ESC [ 37 m` | White foreground       |    ✔️     |
|   ✔️    | `ESC [ 39 m` | Reset foreground color |    ✔️     |
|   ✔️    | `ESC [ 40 m` | Black background       |    ✔️     |
|   ✔️    | `ESC [ 41 m` | Red background         |    ✔️     |
|   ✔️    | `ESC [ 42 m` | Green background       |    ✔️     |
|   ✔️    | `ESC [ 43 m` | Yellow background      |    ✔️     |
|   ✔️    | `ESC [ 44 m` | Blue background        |    ✔️     |
|   ✔️    | `ESC [ 45 m` | Magenta background     |    ✔️     |
|   ✔️    | `ESC [ 46 m` | Cyan background        |    ✔️     |
|   ✔️    | `ESC [ 47 m` | White background       |    ✔️     |
|   ✔️    | `ESC [ 49 m` | Reset background color |    ✔️     |

### Others

All other sequences are ignored and returned as unsupported instructions.

## References and specifications

-   [Colorama](https://github.com/tartley/colorama#recognised-ansi-sequences)
-   [ECMA-48](https://www.ecma-international.org/publications-and-standards/standards/ecma-48/)
-   [VT100](https://vt100.net/docs/vt100-ug/chapter3.html#SGR)
-   [XTerm](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html)
-   [linux](https://man7.org/linux/man-pages/man4/console_codes.4.html) (the
    linux console, that is)
