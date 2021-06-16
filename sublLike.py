#!/usr/bin/env python3
from tkinter import Tk
from tkinter import (Frame, Text, Listbox, 
        Entry, Button, StringVar, END,
        Menu, Label, font
        )
# import action button
from package.action import saveFile, openFileOrFolder
from package.python_shell import PythonShell


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('magic-text')
        self.geometry("1000x800")
        
        # Text editor
        self.frame = Frame(self, bg='#1E201C')
        
        self.left = Frame(self.frame, bg='#1E201C')
        self.enthete = Label(self.left, bg='#1E201C', fg='#5A5C58', text='file').pack()
        self.file_list = Listbox(self.left, bg='#1E201C', fg='white', width=20, height=48)
        self.file_list.pack()
        self.left.pack(side='left', fill='y')
        
        self.right = Frame(self.frame, bg='#1E201C')
        self.frame_top_right = Frame(self.right, bg='#1E201C')
        self.file_name = StringVar()
        self.label = Button(self.frame_top_right, bg='#262626', fg='#5A5C58', textvariable=self.file_name)
        self.file_name.set('nothing')
        self.label.pack(side='left')
        
        self.frame_top_right.pack(fill="x")
        self.text = Text(self.right, bg='#2C2E28', fg='#FFFFFF', width=800, height=31)
        self.text.pack(side='top', fill='y', expand=1)
        self.text.configure(font=('Courier New', 14))
        self.text_in_terminal = StringVar()
        self.terminal = Entry(self.right, bg='#1E201C', fg='#FFFFFF', font=('Courier New', 14),textvariable=self.text_in_terminal)
        self.terminal.pack(side='bottom', fill='x', ipady=35)
        self.right.pack(side='right', fill='y')
        
        self.frame.pack(fill='x')
        
        self.menu = Menu(self, bg='#1E201C', fg='white') # menu base
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
        
        # menu view
        self.menu_view.add_command(label="show terminal Ctrl+'", )
        self.menu_view.add_command(label='hide terminal', )
                
        # menu tools
        self.pythonshell = PythonShell(self.text, self.text_in_terminal)
        self.menu_tools.add_command(label='build Ctrl+B', command=self.pythonshell.get_text)
        self.menu_tools.add_command(label='Cancel')

        # preference
        self.menu_theme = Menu(self.menu_preference, tearoff=0)
        self.menu_preference.add_cascade(label='theme', menu=self.menu_theme)
        # font_tuple = font.families()
        font_tuple = ("Comic Sans MS","Courier New")
        for font_family in font_tuple:
            self.menu_theme.add_command(label=font_family,
                    command=lambda:(self.text.configure(font=(font_family, 14))))
        
        self.config(menu=self.menu, bg='#1E201C')
        
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
