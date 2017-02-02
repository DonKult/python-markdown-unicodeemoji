# Python-Markdown UnicodeEmoji extension

A simple hack disguised as an extension to allow common emoji shortnames
to be found and replaced in markdown text by the python-markdown engine.

There are many others by potentially more experienced python coders, but the
distinguishing feature of this extension is that proper Unicode is used as
replacement rather than various forms of images delegating the display task to
fonts you have (hopefully) installed on your system.

## How to build & run

There are no build steps and as an extension it is to be run by
python-markdown only as configured.

The extension requires various data files to function properly.
These data files are *NOT* included in the repository, you may find
them in other locations on the web:

* *emoji-test.txt*: http://www.unicode.org/Public/emoji/4.0/emoji-test.txt
* *api-github-com-emojis.json*: https://api.github.com/emojis
* *emojione.json*: https://github.com/Ranks/emojione/blob/master/emoji.json

See their upstream sites for licensing details and how to use them "properly"
as this extension isn't really using them properly. You have been warned.
They are also the right place to report bugs if you miss a mapping (and have
verified before that it isn't an error on my part that it is missing).

To ensure a browser picks the right fonts for the emoji display it is recommended
to provide a hint via CSS:

```css
.emoji {
  font-family: "EmojiOne", "EmojiOne Mozilla", "Apple Color Emoji", "Segoe UI",
    "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", "EmojiSymbols",
    "DejaVu Sans", "Symbola";
  /* avoid the splitting of multi-char unicodes */
  white-space: nowrap;
}
```

If you know of other font families which have reasonable support for the emoji
sets feel free to contact me to have them added.

## License

    Copyright (C) 2016-2017  David Kalnischkies

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.


Note that the "graphics" you see and the text strings they are replacing are
not part of this repository and might be covered by an entirely different
license. If you are on Linux and are running Firefox the "graphics" you see are
e.g. likely [EmojiOne](http://emojione.com/) released under [CC-BY
4.0](https://creativecommons.org/licenses/by/4.0/).