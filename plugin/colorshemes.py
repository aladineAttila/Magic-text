#!/usr/bin/env python3

def generate_dictionnairy(themes):
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


def loadRegex():
    with open('all_fonction_python', 'r') as file_fonction:
        r = "|".join(elt.strip("\n").lower() for elt in file_fonction.readlines())
        return r


def loading_colorscheme(path):
    with open(path, 'r') as colorschemes:
        themes = colorschemes.read()
        return generate_dictionnairy(themes)


class Colorscheme:
    def __init__(self, path, title_colorschemes):
        self.colorschemes = loading_colorscheme(path)
        self.color = self.colorschemes[title_colorschemes]

        self.function = ('fonction',
                         r"(abs|all|any|ascii|bin|bool|bytearray|bytes|callable|chr|classmethod|compile|complex"
                         r"|delatrr|dir|divmod|enumerate|eval|exec|filter|float|format|getattr|globals|hasattr|hash"
                         r"|help|hex|id|isinstance|issubclass|iter|len|locals|map|max|memoryview|min|next|object|oct"
                         r"|open|ord|pow|print|property|range|repr|reversed|round|set|setattr|slice|sorted"
                         r"|staticmethod|str|sum|super|type|vars|_import_|capitalize|casefold|center|count|encode"
                         r"|endswith|expandtabs|find|format|format_map|index|input|int|isalnum|isalpha|isdecimal"
                         r"|isdigit|isidentifier|islower|isnumeric|isprintable|isspace|istitle|isupper|join|ljust"
                         r"|lower|lstrip|maketrans|partition|replace|rfind|rindex|rjust|rpartition|rsplit|rstrip"
                         r"|slice|split|splitlines|startswith|strip|swapcase|title|translate|upper|zfill|function"
                         r"|append|clear|copy|count|extend|index|insert|list|pop|remove|reverse|slice|sort|count"
                         r"|index|slice|tuple|zip|add|clear|copy|difference|difference_update|discard|frozenset"
                         r"|intersection|intersection_update|isdisjoint|issubset|issuperset|pop|remove|set|union"
                         r"|update|clear|copy|dict|fromkeys|get|items|keys|pop|popitem|setdefault|update|values)",
                         self.color['definition-foreground'], self.color['definition-background'])

        self.keyword = ('keyword', r'(if |elif |else:|def |for |while |try:|except|class|from |import | as | in '
                                   r'|return )', self.color['keyword-foreground'], self.color['keyword-background'])

        self.comment = ('comment', r'(#.+)', self.color['comment-foreground'], self.color['comment-background'])

        self.string = ('string', r'(".+\"|\'.+\')', self.color['string-foreground'], self.color['string-background'])


if __name__ == "__main__":
    # print([elt for elt in loading_colorscheme('colorshemes')])
    print(loadRegex())
