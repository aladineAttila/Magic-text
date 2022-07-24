#!/usr/bin/env python3
from dataclasses import dataclass

def generateDict(themes: str) -> dict:
    themes: list = [elt.split('\n') for elt in themes.split("\n\n")]
    dictionnairy: dict = {}
    title: str = ''
    for theme in themes:
        tmp_dict: dict = {}
        for i, line in enumerate(theme):
            if i == 0:
                title = line.strip('[]')
            else:
                try:
                    key, value = line.split("=")
                    tmp_dict[key.strip(' ')] = value.strip(' ')
                except ValueError:
                    pass
        dictionnairy[title] = tmp_dict
    return dictionnairy


def readColorscheme(path: str) -> dict:
    with open(path, 'r') as colorschemes:
        themes = colorschemes.read()
        return generateDict(themes)


@dataclass
class Colorscheme:
    def __init__(self, path: str, title_colorscheme: str) -> None:
        self.colorscheme = readColorscheme(path)
        self.color = self.colorscheme[title_colorscheme]

        self.function = (
             'fonction',
             r'(\w+)(?=\s?\()',
             self.color['definition-foreground'],
             self.color['definition-background']
         )

        self.keyword = (
            'keyword',
            r'(if |elif |else:|def |for |while |try:|except|class|from |import | as | in |return )',
            self.color['keyword-foreground'],
            self.color['keyword-background']
        )

        self.comment = (
            'comment',
            r'(#.+|""".+""")',
            self.color['comment-foreground'],
            self.color['comment-background']
        )

        self.char = (
            'char',
            r'(\'.+\')',
            self.color['string-foreground'],
            self.color['string-background']
        )

        self.string = (
            'string', r'(".+")',
            self.color['string-foreground'],
            self.color['string-background']
        )

