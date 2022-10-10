from tkinter import Text, Variable


class TextWithColorisation(Text):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self._variable = Variable()

    def findall(self, pattern, start='1.0', end='end'):
        v = self._variable
        s = self.tk.call(
            self, 'search', '-all',
            '-count', v,
            '-regexp', pattern,
            start, end
        )

        indices = []
        for a, b in zip(s, v.get()):
            indices += [f'{a}', f'{a}+{b}c']
        return indices
