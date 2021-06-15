#!/usr/bin/env python3
from tkinter import Tk
from tkinter import (Frame, Text, Listbox, 
        Entry, Button, StringVar, END,
        Menu, Label
        )
# import action button
from package.action import saveFile, openFileOrFolder
from package.python_shell import PythonShell


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('magic-text')
        self.geometry("1000x800")

        self.menu = Menu(self) # menu base
        self.menu_file = Menu(self.menu, tearoff=0)
        self.menu_view = Menu(self.menu, tearoff=0)
        self.menu_preference = Menu(self.menu, tearoff=0)
        self.menu_tools = Menu(self.menu, tearoff=0)
        
        # add menu file into menu
        self.menu.add_cascade(label='file', menu=self.menu_file)
        self.menu.add_cascade(label='view', menu=self.menu_view)
        self.menu.add_cascade(label='tools', menu=self.menu_tools)
        self.menu.add_cascade(label='preference', menu=self.menu_preference)

        # menu file
        self.menu_file.add_command(label='save Ctrl+S', command=lambda:(saveFile(
            self.text.get(1.0,END),self.file_name.get()
            )))
        self.menu_file.add_command(label='open file Ctrl+O',command=self.insertion)
        self.menu_file.add_command(label='open folder',)
        
        # menu view
        self.menu_view.add_command(label='split verticat')
        self.menu_view.add_command(label='split horizontal')
        #self.menu_view.add_command(label="show terminal Ctrl+'", command=self.showTerminal)
        #self.menu_view.add_command(label='hide terminal', )
        
        

        # menu preference
        self.theme = Menu(self.menu_preference, tearoff=0)
        self.menu_preference.add_cascade(label='theme', menu=self.theme)
        self.theme.add_command(label='monokai')
        self.theme.add_command(label='maria')
        self.menu_preference.add_command(label='setting')
        self.config(menu=self.menu)
        
        # Text editor
        self.frame = Frame(self)
        
        self.left = Frame(self.frame)
        self.enthete = Label(self.left, text='file').pack()
        self.file_list = Listbox(self.left, width=20, height=38)
        self.file_list.pack()
        self.left.pack(side='left')
        
        self.right = Frame(self.frame)
        self.frame_top_right = Frame(self.right)
        self.file_name = StringVar()
        self.label = Button(self.frame_top_right, textvariable=self.file_name)
        self.file_name.set('nothing')
        self.label.pack(side='left')
        
        self.frame_top_right.pack(fill="x")
        self.text = Text(self.right, width=800, height=40)
        self.text.pack()
        self.right.pack(side='right')
        
        self.frame.pack(fill='x')
        self.text_in_terminal = StringVar()
        self.terminal = Entry(self, textvariable=self.text_in_terminal)
        self.terminal.pack(fill='x', ipady=25)
        
        #menu tools
        self.pythonshell = PythonShell(self.text, self.text_in_terminal)
        self.menu_tools.add_command(label='build Ctrl+B', command=self.pythonshell.get_text)
        self.menu_tools.add_command(label='Cancel')
        
    def insertion(self):
        """
        1 - open file broweser
        2 - insert file name in file_list
        3 - set text in label
        
        return None
        """
        name, content , directory = openFileOrFolder('file')
        self.title(f'{directory} - magic-text')
        self.file_list.insert(END, name)       
        self.text.insert(END, content)
        self.file_name.set(name)


if __name__ == "__main__":
    app = App()
    app.mainloop()
