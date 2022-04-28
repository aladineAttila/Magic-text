from tkinter import Menu


class MyMenu(Menu):
    def __init__(self, master=None, cnf={}, **kw):
        self.kw = kw
        self.cnf = cnf
        super().__init__(master, cnf, **kw)

    def get_value(self):
        return self.kw
