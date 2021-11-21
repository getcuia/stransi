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

| Status | Sequence    | Description          |
| :----: | :---------- | :------------------- |
|  [x]   | `ESC [ 0 m` | Reset all attributes |
|  [x]   | `ESC [ 1 m` | Bold                 |
|  [x]   | `ESC [ 4 m` | Underline            |
|  [x]   | `ESC [ 5 m` | Blink                |
|  [x]   | `ESC [ 7 m` | Inverse              |
|  [x]   | `ESC [ 8 m` | Invisible            |
