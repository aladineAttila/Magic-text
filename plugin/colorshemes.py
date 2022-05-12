#!/usr/bin/env python3
from dataclasses import dataclass

def generateDict(themes):
    themes = [elt.split('\n') for elt in themes.split("\n\n")]
    dictionnairy = {}
    title = ''
    for theme in themes:
        dic = {}
        for i, line in enumerate(theme):
            if i == 0:
                title = line.strip('[]')
            else:
                try:
                    key, value = line.split("=")
                    dic[key.strip(' ')] = value.strip(' ')
                except ValueError:
                    pass
        dictionnairy[title] = dic
    return dictionnairy


def readColorscheme(path):
    with open(path, 'r') as colorschemes:
        themes = colorschemes.read()
        return generateDict(themes)


class Colorscheme:
    def __init__(self, path, title_colorschemes):
        self.colorschemes = readColorscheme(path)
        self.color = self.colorschemes[title_colorschemes]

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

