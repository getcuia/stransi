# Recognized ANSI Sequences

ANSI sequences generally take the form:

    ESC [ <parameter> ; <parameter> ; ... <command>

where `ESC` is the escape character (`\033`), `[` is the opening bracket,
`<parameter>` is an integer, `;` is the semicolon separator, and `<command>` is
a single character. Zero or more parameters can be specified, but generally
assumed to be zero if unspecified. No spaces are allowed, they are shown here
only for clarity.

Only a subset of the ANSI escape sequences are supported by this library. See
the tables below for a complete list of currently supported (and planned to be
supported) ANSI escape sequences.

## SGR (Select Graphic Rendition, `m`)

| Status? | Sequence     | Description            | Colorama? |
| :-----: | :----------- | :--------------------- | :-------: |
|    ✔️   | `ESC [ 0 m`  | Reset all attributes   |     ✔️     |
|    ✔️   | `ESC [ 1 m`  | Bold/bright            |     ✔️     |
|    ✔️   | `ESC [ 2 m`  | Dim                    |     ✔️     |
|    ✔️   | `ESC [ 22 m` | Reset brightness       |     ✔️     |
|    ✔️   | `ESC [ 30 m` | Black foreground       |     ✔️     |
|    ✔️   | `ESC [ 31 m` | Red foreground         |     ✔️     |
|    ✔️   | `ESC [ 32 m` | Green foreground       |     ✔️     |
|    ✔️   | `ESC [ 33 m` | Yellow foreground      |     ✔️     |
|    ✔️   | `ESC [ 34 m` | Blue foreground        |     ✔️     |
|    ✔️   | `ESC [ 35 m` | Magenta foreground     |     ✔️     |
|    ✔️   | `ESC [ 36 m` | Cyan foreground        |     ✔️     |
|    ✔️   | `ESC [ 37 m` | White foreground       |     ✔️     |
|    ✔️   | `ESC [ 39 m` | Reset foreground color |     ✔️     |
|    ✔️   | `ESC [ 40 m` | black background       |     ✔️     |
|    ✔️   | `ESC [ 41 m` | red background         |     ✔️     |
|    ✔️   | `ESC [ 42 m` | green background       |     ✔️     |
|    ✔️   | `ESC [ 43 m` | yellow background      |     ✔️     |
|    ✔️   | `ESC [ 44 m` | blue background        |     ✔️     |
|    ✔️   | `ESC [ 45 m` | magenta background     |     ✔️     |
|    ✔️   | `ESC [ 46 m` | cyan background        |     ✔️     |
|    ✔️   | `ESC [ 47 m` | white background       |     ✔️     |
|    ✔️   | `ESC [ 49 m` | reset background color |     ✔️     |
