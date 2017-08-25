# coding: utf-8
"""
Converts ascii smilies and similar symbols into proper UTF-8 symbols

A replacement is only done if the pattern is prefixed with a whitespace (or
start of line) and is followed either by whitespace or the end of the line.
Optionally a single dot, comma or ellipse can appear between the emoji-pattern
and the end-pattern.

All utf-8 symbols (which we will subsum under emojis now) are wrapped in a
<span> with the class "emoji" for styling purposes. Strongly recommend is
setting specific font(s).

```css
.emoji {
  font-family: "EmojiOne", "EmojiOne Mozilla", "Apple Color Emoji", "Segoe UI",
    "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", "EmojiSymbols",
    "DejaVu Sans", "Symbola";
}
```

"""
from markdown import Extension
from markdown.util import etree, AtomicString
from markdown.inlinepatterns import Pattern
import json
import string


class UnicodeEmojiExtension(Extension):
    emoji = {}
    mapping = {}

    # removing the unicode variant modifier
    def _cleanCodeList(self, codes):
        return list(filter(lambda u: u not in ['FE0F'], codes))

    def _joinCodeList(self, codes):
        code = ' '.join(codes)
        if code not in self.emoji and '200D' not in codes:
            return ' 200D '.join(codes)
        return code

    def _dataFilePath(self, name):
        import os
        return os.path.join(os.path.dirname(__file__), name)

    def __init__(self, *args, **kwargs):
        super(UnicodeEmojiExtension, self).__init__(*args, **kwargs)
        # load the base dataset
        with open(self._dataFilePath('emoji-test.txt'), 'r') as emojitest:
            for line in emojitest:
                if '; keyboard  #' in line or '; fully-qualified     #' in line:
                    codelist = self._cleanCodeList(line.split(';')[0].strip().split(' '))
                    self.emoji[self._joinCodeList(codelist)] = set()
        # import the github mapping set
        with open(self._dataFilePath('api-github-com-emojis.json'), 'r') as githubemoji:
            for k, v in json.loads(githubemoji.read()).items():
                text = ':' + k + ':'
                code = v.split('/')[-1].split('.', 1)[0].upper().replace('-', ' ')
                splitcode = self._cleanCodeList(code.split(' '))
                code = self._joinCodeList(splitcode)
                if code in self.emoji and all(c in string.hexdigits for c in code.replace(' ', '')):
                    self.emoji[code].add(text)
                else:
                    print('Unknown unicode in github set:', code, text)
        # import emojione mapping set
        with open(self._dataFilePath('emojione.json'), 'r') as emojione:
            for k, v in json.loads(emojione.read()).items():
                if 'unicode_alternates' in v and v['unicode_alternates']:
                    code = v['unicode_alternates'].upper().replace('-', ' ')
                else:
                    code = v['unicode'].upper().replace('-', ' ')
                splitcode = self._cleanCodeList(code.split(' '))
                code = self._joinCodeList(splitcode)
                if code not in self.emoji:
                    self.emoji[code] = set()
                self.emoji[code].add(v['shortname'])
                for a in v['aliases']:
                    self.emoji[code].add(a)
                if 'aliases_ascii' in v:
                    for a in v['aliases_ascii']:
                        self.emoji[code].add(a)
        # reverse key <-> values for the actual task at hand now
        for k, emolist in self.emoji.items():
            for e in emolist:
                if e in self.mapping:
                    if self.mapping[e] == k:
                        continue
                    print('Mapping already exists for', e, 'with', self.mapping[e], 'newly proposed value', k)
                else:
                    self.mapping[e] = k
            code = ''.join(map(lambda u: chr(int(u, 16)), k.split(' ')))
            # add the code itself so that they are wrapped properly if they appear literal
            self.mapping[code] = k
        self.mapping[':ALL_UNICODE_EMOJI:'] = set()

    def extendMarkdown(self, md, md_globals):
        import re
        # an emoji should be surrounded by "whitespace"
        RE = r'((?<=\s)|(?<=^))(?P<emoji>%s)(?=(\.|…|,|)(\s|$))' % '|'.join(map(re.escape, self.mapping.keys()))
        md.inlinePatterns['emoji'] = UnicodeEmojiPattern(RE, md, self)


class UnicodeEmojiPattern(Pattern):
    def __init__(self, pattern, md, extension):
        super(UnicodeEmojiPattern, self).__init__(pattern, md)
        self.extension = extension

    def _createEmoji(self, e, title, tcode, ucode):
        e.set('class', AtomicString('emoji'))
        if title:
            e.set('title', AtomicString(title))
        e.set('data-unicode', AtomicString(tcode))
        e.text = AtomicString(ucode)
        return e

    def handleMatch(self, m):
        if m.group('emoji') == ':ALL_UNICODE_EMOJI:':
            ule = etree.Element('ul')
            ule.set('class', 'emojilist')
            lie = etree.SubElement(ule, 'li')
            lie.text = str(len(self.extension.emoji.items())) + ' emojis with ' + str(len(self.extension.mapping.items())) + ' mappings'
            for k, v in self.extension.emoji.items():
                code = ''.join(map(lambda u: chr(int(u, 16)), k.split(' ')))
                self._createEmoji(etree.SubElement(ule, 'li'), ' '.join(v), k, code)
            return ule
        tcode = self.extension.mapping[m.group('emoji')]
        ucode = ''.join(map(lambda u: chr(int(u, 16)), tcode.split(' ')))
        return self._createEmoji(etree.Element('span'), m.group('emoji'), tcode, ucode)


def makeExtension(*args, **kwargs):
    return UnicodeEmojiExtension(*args, **kwargs)
