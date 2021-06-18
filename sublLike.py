#!/usr/bin/env python3
from tkinter import Tk
from tkinter import (Frame, Text, Listbox, 
        Entry, Button, StringVar, END,
        Menu, Label, font, Variable
        )
from package.action import saveFile, openFileOrFolder, PythonShell


class TextWithColorisation(Text):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self._variable = Variable()
 
    def findall(self, pattern, start='1.0', end='end'):
 
        v = self._variable
        s = self.tk.call(self, 'search', '-all',
                  '-count', v,
                  '-regexp', pattern,
                  start, end)
         
        indices = []
        for a, b in zip(s, v.get()):
            indices += [ '%s' % a, '%s+%dc' % (a, b) ]
            
        return indices


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('magic-text')
        self.geometry("1000x800")
        
        self.dic = {}
        self.file_active_now = None
        
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
        
        self.frame_top_right.pack(fill="x")
        self.text = TextWithColorisation(self.right, bg='#2C2E28', fg='#FFFFFF', width=800, height=31)
        self.text.pack(side='top', fill='y', expand=1)
        self.text.configure(font=('Courier New', 11))
        
        
        
        self.text_in_terminal = StringVar()
        self.terminal = Entry(self.right, bg='#1E201C', fg='#FFFFFF', font=('Courier New', 14),textvariable=self.text_in_terminal)
        
        self.right.pack(side='right', fill='y')
        
        self.frame.pack(fill='x')
        
        self.menu = Menu(self, bg='#1E201C', fg='white') # menu base
        self.menu_file = Menu(self.menu, bg='#1E201C', fg='white', tearoff=0)
        self.menu_view = Menu(self.menu, bg='#1E201C', fg='white', tearoff=0)
        self.menu_preference = Menu(self.menu, bg='#1E201C', fg='white', tearoff=0)
        self.menu_tools = Menu(self.menu, bg='#1E201C', fg='white', tearoff=0)
        
        # add menu file into menu
        self.menu.add_cascade(label='file', menu=self.menu_file)
        self.menu.add_cascade(label='view', menu=self.menu_view)
        self.menu.add_cascade(label='tools', menu=self.menu_tools)
        self.menu.add_cascade(label='preference', menu=self.menu_preference)

        # menu file
        self.menu_file.add_command(label='save Ctrl+S', 
                command=lambda:(
                    saveFile(self.text.get(1.0,END),self.file_active_now)
                ))
        self.menu_file.add_command(label='open file Ctrl+O',command=self.insertion)
        self.menu_file.add_command(label='quit', command=self.quit)
        
        # menu view
        self.menu_view.add_command(label="show terminal Ctrl+'", command=lambda:self.hideAndShowTerminal('show'))
        self.menu_view.add_command(label='hide terminal', command=lambda:self.hideAndShowTerminal('hide'))
                
        # menu tools
        self.pythonshell = PythonShell(self.text, self.text_in_terminal)
        self.menu_tools.add_command(label='build Ctrl+B', 
                command=lambda:(
                    self.pythonshell.build(self.dic[self.file_active_now])))
        self.menu_tools.add_command(label='build and Save',
                command=lambda:(
                    self.pythonshell.build(self.dic[self.file_active_now], 'buildAndWrite')
                    ))

        # preference
        self.menu_theme = Menu(self.menu_preference, bg='#1E201C', fg='white', tearoff=0)
        self.menu_preference.add_cascade(label='theme', menu=self.menu_theme)
        # font_tuple = font.families()
        font_tuple = ("Comic Sans MS","Courier New")
        for font_family in font_tuple:
            self.menu_theme.add_command(label=font_family,
                    command=lambda:(self.text.configure(font=(font_family, 11))))
        
        self.config(menu=self.menu, bg='#1E201C')

        # key binding
        self.text.bind('<KeyRelease>', self.groupAllFoctionColor)
    
    def activeFile(self, directory):
        self.groupAllFoctionColor('')
        if self.file_active_now != directory.split('/')[-1]:
            self.text.delete(1.0, END)
            with open(directory, 'r') as file_text:
                self.text.insert(END, file_text.read())
            self.title(f'{directory} - magic-text')
        
    def insertion(self):
        name, content , directory = openFileOrFolder('file')
        self.file_active_now = name
        self.dic[name] = directory
        self.title(f'{directory} - magic-text')
        self.file_list.insert(END, name)
        self.text.delete(1.0, END)
        self.text.insert(END, content)
        self.groupAllFoctionColor('')
        Button(self.frame_top_right, text=name,
                command=lambda:(self.activeFile(self.dic[name])),
                bg='#262626', fg='#5A5C58' 
                ).pack(side='left')
    
    def hideAndShowTerminal(self, mode):
        try:
            if mode == "show":
                self.terminal.pack(side='bottom', fill='x', ipady=35)
            elif mode == "hide":
                self.terminal.destroy()
                self.terminal = Entry(self.right, bg='#1E201C', fg='#FFFFFF', font=('Courier New', 14), textvariable=self.text_in_terminal)
        except:
            pass

    def groupAllFoctionColor(self, e):
        fonction = r'(if |elif |else:|def |for |while |try:|except|class )'
        entre_g = r'"\w+"|\'\w+\''
        autre = r'(print|set|get)'
        object_ = r'(class|\w+\.)'
        self.color('fonction', fonction, '#D25D5B')
        self.color('autre', autre, '#CA7A02')
        self.color('class', object_,'#3F82AC')
        self.color('entre_g', entre_g,'#DFDC11')
    
    def color(self, type_, keyword, hercolor):
        try:
            self.text.tag_configure(type_, foreground=hercolor, background='#2C2E28')
            indices = self.text.findall(keyword)
            self.text.tag_add(type_, *indices) 
            
        except:
            pass
    
if __name__ == "__main__":
    app = App()
    app.mainloop()
