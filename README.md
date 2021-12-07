[![PyPI](https://img.shields.io/pypi/v/stransi)](https://pypi.org/project/stransi/)
[![Python package](https://github.com/getcuia/stransi/actions/workflows/python-package.yml/badge.svg)](https://github.com/getcuia/stransi/actions/workflows/python-package.yml)
[![PyPI - License](https://img.shields.io/pypi/l/stransi)](https://github.com/getcuia/stransi/blob/main/LICENSE)

# [stransi](https://github.com/getcuia/stransi#readme) 🖍️

<div align="center">
    <img class="hero" src="https://github.com/getcuia/stransi/raw/main/banner.jpg" alt="stransi" width="33%" />
</div>

> I see a `\033[1;31m`red`\033[;39m` door, and I want it painted
> `\033[1;30m`black`\033[;39m`.

stransi is a lightweight parser for
[ANSI escape code sequences](https://en.wikipedia.org/wiki/ANSI_escape_code). It
implements a string-like type that is aware of its own ANSI escape sequences,
and can be used to parse most of the common escape sequences used in terminal
output manipulation.

## Features

-   ✨ [Good support of ANSI escape sequences](FEATURES.md)
-   🎨 Focus on coloring and styling
-   🛡️ Unsupported `CSI` escape sequences are emitted as tokens
-   🏜️ Only one dependency: [ochre](https://github.com/getcuia/ochre)
-   🐍 Python 3.8+

## Installation

```console
$ pip install stransi
```

## Usage

```python
In [1]: from stransi import Ansi

In [2]: text = Ansi(
   ...:     "I see a \033[1;31mred\033[;39m door, "
   ...:     "and I want it painted \033[1;30mblack\033[;39m"
   ...: )

In [3]: list(text.escapes())
Out[3]:
['I see a ',
 Escape('\x1b[1;31m'),
 'red',
 Escape('\x1b[;39m'),
 ' door, and I want it painted ',
 Escape('\x1b[1;30m'),
 'black',
 Escape('\x1b[;39m')]

In [4]: list(text.instructions())
Out[4]:
['I see a ',
 SetAttribute(attribute=<Attribute.BOLD: 1>),
 SetColor(role=<ColorRole.FOREGROUND: 30>, color=Ansi256(1)),
 'red',
 SetAttribute(attribute=<Attribute.NORMAL: 0>),
 SetColor(role=<ColorRole.FOREGROUND: 30>, color=None),
 ' door, and I want it painted ',
 SetAttribute(attribute=<Attribute.BOLD: 1>),
 SetColor(role=<ColorRole.FOREGROUND: 30>, color=Ansi256(0)),
 'black',
 SetAttribute(attribute=<Attribute.NORMAL: 0>),
 SetColor(role=<ColorRole.FOREGROUND: 30>, color=None)]
```

## Credits

[Photo](https://github.com/getcuia/stransi/raw/main/banner.jpg) by
[Tien Vu Ngoc](https://unsplash.com/@tienvn3012?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
on
[Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).
