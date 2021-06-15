#!/usr/bin/env python3
from tkinter import Tk
from tkinter import (Frame, Text, Listbox, 
        Entry, Button, StringVar, END,
        Menu
        )
# import action button
from action import saveFile, openFileOrFolder


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
        self.menu_file.add_command(label='save Ctrl+S',)
        self.menu_file.add_command(label='open file Ctrl+O',command=self.insertion)
        self.menu_file.add_command(label='open folder',)
        
        # menu view
        self.menu_view.add_command(label='split verticat')
        self.menu_view.add_command(label='split horizontal')
        self.menu_view.add_command(label="show terminal Ctrl+'")
        
        #menu tools
        self.menu_tools.add_command(label='build Ctrl+B')
        self.menu_tools.add_command(label='Cancel')

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
        self.file_list = Listbox(self.left, width=20, height=38)
        self.file_list.pack()
        self.left.pack(side='left')
        
        self.right = Frame(self.frame)
        self.frame_top_right = Frame(self.right)
        self.label = Button(self.frame_top_right, text='titre')
        self.label.pack(side='left')
        self.frame_top_right.pack()
        self.text = Text(self.right, width=800, height=40)
        self.text.pack()
        self.right.pack(side='right')
        
        self.frame.pack()
    
    def insertion(self):
        name, content , directory = openFileOrFolder('file')
        self.title(f'{directory} - magic-text')
        self.file_list.insert(END, name)       
        self.text.insert(END, content) 


if __name__ == "__main__":
    app = App()
    app.mainloop()
