#!/usr/bin/env python3
from tkinter import Tk
from tkinter import (Frame, Text, Listbox, 
        Entry, Button, StringVar, END,
        Menu, Label, font, Variable, ACTIVE
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

app_background = "#1E201C"
app_foreground = "white"

text_widget_background = "#2C2E28"
text_widget_foreground = "white"
cursor_color = "white"

menu_background = "white"
menu_foreground = "#1E201C"


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('magic-text')
        self.geometry("1000x800")
        
        self.dic = {}
        self.file_active_now = None
        
        # Text editor
        self.frame = Frame(self, bg=app_background)
        
        self.left = Frame(self.frame, bg=app_background)
        self.enthete = Label(self.left, bg=app_background, fg='#5A5C58', text='file').pack()
        self.file_list = Listbox(self.left, bg=app_background, fg='white', width=20, height=48)
        self.file_list.pack()
        self.left.pack(side='left', fill='y')
        
        self.right = Frame(self.frame, bg=app_background)
        self.frame_top_right = Frame(self.right, bg=app_background)
        self.file_name = StringVar()
        
        self.frame_top_right.pack(fill="x")
        self.text = TextWithColorisation(self.right, bg=text_widget_background, fg='#FFFFFF', width=800, height=31)
        self.text.pack(side='top', fill='y', expand=1)
        self.font_active_now = 'Courier New'
        self.text.configure(insertbackground='white', font=('Courier New', 11))
        
        self.text_in_terminal = StringVar()
        self.terminal = Entry(self.right, bg=app_background, fg=app_foreground, font=('Courier New', 14),textvariable=self.text_in_terminal)
        
        self.right.pack(side='right', fill='y')
        
        self.frame.pack(fill='x')
        
        self.menu = Menu(self, bg=menu_background, fg=menu_foreground) # menu base
        self.menu_file = Menu(self.menu, bg=menu_background, fg=menu_foreground, tearoff=0)
        self.menu_view = Menu(self.menu, bg=menu_background, fg=menu_foreground, tearoff=0)
        self.menu_preference = Menu(self.menu, bg=menu_background, fg=menu_foreground, tearoff=0)
        self.menu_tools = Menu(self.menu, bg=menu_background, fg=menu_foreground, tearoff=0)
        
        # add menu file into menu
        self.menu.add_cascade(label='file', menu=self.menu_file)
        self.menu.add_cascade(label='view', menu=self.menu_view)
        self.menu.add_cascade(label='tools', menu=self.menu_tools)
        self.menu.add_cascade(label='preference', menu=self.menu_preference)

        # menu file
        self.menu_file.add_command(label='save Ctrl+S', 
                command=lambda:(
                    saveFile(self.text.get(1.0,END),self.file_active_now, self.insertion)
                ))
        self.menu_file.add_command(label='open file Ctrl+O',command=self.insertion)
        self.menu_file.add_command(label='quit', command=self.quit)
        
        # menu view
        self.menu_view.add_command(label="show terminal Ctrl+'", command=lambda:self.hideAndShowTerminal('show'))
        self.menu_view.add_command(label='hide terminal', command=lambda:self.hideAndShowTerminal('hide'))
                
        # menu tools
        self.pythonshell = PythonShell(self.text, self.text_in_terminal)

        try:
            self.file_path = self.dic[self.file_active_now]
        except:
            self.file_path = None
        
        self.menu_tools.add_command(label='build and Save',
                command=lambda:(
                    self.pythonshell.build(self.file_path, 'buildAndWrite', self.insertion)
                    ))

        # preference
        self.menu_theme = Menu(self.menu_preference, bg=menu_background, fg=menu_foreground, tearoff=0)
        self.menu_preference.add_cascade(label='theme', menu=self.menu_theme)
        #font_tuple = font.families()
        font_tuple = ("Comic Sans MS","Courier New", "Helvetica", "Times New Roman")
        
        for font_family in font_tuple:
            self.menu_theme.add_command(label=font_family,
                    command=lambda:(self.changeFont(font_family)))
        
        self.config(menu=self.menu, bg=menu_background)

        # key binding
        self.text.bind('<KeyRelease>', self.groupAllFoctionColor)
        self.file_list.bind('<<ListboxSelect>>', self.fillOut)
    
    def fillOut(self,e):
        self.activeFile(self.dic[self.file_list.get(ACTIVE)])
    
    def changeFont(self, font_family):
            self.font_active_now = font_family
            self.text.configure(font=(font_family, 11))
    
    def activeFile(self, directory):
        '''
        1- call groupAllFoctionColor
        2- verify if self.acitve_now
        3- delete all and read file on the directory and insert this
        4- set title
        
        :return: None
        '''
        self.groupAllFoctionColor('')
        if self.file_active_now != directory.split('/')[-1]:
            self.file_active_now = directory.split('/')[-1]
            self.text.delete(1.0, END)
            with open(directory, 'r') as file_text:
                self.text.insert(END, file_text.read())
            self.title(f'{directory} - magic-text')
        
    def insertion(self):
        """
        1 - open file broweser
        2 - insert file name in file_list
        3 - set text in label
        
        return None
        """
        name, content , directory = openFileOrFolder('file')
    def insertion(self, mode=None, name=None, content=None, directory=None):
        '''
        1- get name, contenu, directory
        2- set file_active_now to name 
        3- add directory in dic
        4- set title
        5- add name to file_list
        6- delete all and insert content
        7- call fonction groupAllFoctionColor
        8- Add Button and her command

        :return: None
        '''
        if mode == None:
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
                self.terminal = Entry(self.right, bg=app_background, fg=app_foreground, font=('Courier New', 14), textvariable=self.text_in_terminal)
        except:
            pass

    def groupAllFoctionColor(self, e):
        fonction_ = r'(if |elif |else:|def |for |while |try:|except|class|from |import | as | in |return )'
        entre_guemet_ = r'(".+\"|\'.+\')'
        autre = r'(print|set|get|self)'
        attribute_ = r'(\.\w+)'
        commentaire_ = r'(#.+)'

        self.color('fonction', fonction_, '#D25D5B')
        self.color('autre', autre, '#CA7A02')
        self.color('attribute', attribute_, '#3F82AC')
        self.color('entre_guemet', entre_guemet_, '#DFDC11')
        self.color('commentaire', commentaire_, '#BEBEBE')
    
    def color(self, type_, keyword, hercolor):
        try:
            self.text.tag_configure(type_, font=(self.font_active_now, 11, 'bold'), foreground=hercolor, background=text_widget_background)
            indices = self.text.findall(keyword)
            self.text.tag_add(type_, *indices) 
            
        except:
            pass
    
if __name__ == "__main__":
    app = App()
    app.mainloop()
