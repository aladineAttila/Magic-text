#!/usr/bin/env python3
from tkinter import Tk
from tkinter import (Frame, Text, Listbox, 
        Entry, Button, StringVar, END,
        Menu, Label, font, Variable, ACTIVE, Scrollbar 
        )
from package.action import saveFile, openFile, PythonShell
import os

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
        
        # Frame principal
        self.frame = Frame(self, bg=app_background)
        
        # left frame contient file_list
        self.left = Frame(self.frame, bg=app_background)
        self.enthete = Label(self.left, bg=app_background, fg='#5A5C58', text='file').pack(ipady=5)
        self.file_list = Listbox(self.left, bg=app_background, fg='white', width=20, height=48)
        self.file_list.pack()
        self.left.pack(side='left', fill='y')
        
        # right frame contient text editor and label button
        # et le scrollbar et la linenumber
        self.right = Frame(self.frame, bg=app_background)
        # bar de status
        self.frame_top_right = Frame(self.right, bg=app_background)
        self.file_name = StringVar()
        self.frame_top_right.pack(fill="x")
        # text editor
        self.text_container = Frame(self.right)
        self.rigth_scrolbar = Scrollbar(self.text_container)
        self.rigth_scrolbar.pack(side="right", fill='y')
        self.line_number = Listbox(self.text_container, width=1, height=31, font=(None,11),bg=text_widget_background, fg='#5A5C58', 
                yscrollcommand=self.rigth_scrolbar.set)
        self.line_number.pack(side='left', fill='y')
        self.text = TextWithColorisation(self.text_container, undo=True, autoseparators=True, maxundo=-1,bg=text_widget_background, fg='#FFFFFF', width=800, height=31,
                yscrollcommand=self.rigth_scrolbar.set)
        self.text.pack(side='left', fill='y')
        self.rigth_scrolbar.config(command=self.scroll_yview)
        self.font_active_now = 'Courier New'
        self.text.configure(insertbackground='white', font=('Courier New', 11))
        self.text_container.pack(side='top', fill='y', expand=1)
        # terminal
        self.text_in_terminal = StringVar()
        self.terminal = Entry(self.right, bg=app_background, fg=app_foreground, font=('Courier New', 14),textvariable=self.text_in_terminal)
        self.right.pack(side='right', fill='y')
        
        self.frame.pack(fill='x')
        
        # Barre de menu
        self.menu = Menu(self, bg=menu_background, fg=menu_foreground) 
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
                command=lambda:self.ctrl_S('<Control+s>'))
        self.menu_file.add_command(label='open file Ctrl+O',command=self.insertion)
        self.menu_file.add_command(label='quit Ctrl+Q', command=self.quit)
        
        # menu view
        self.menu_view.add_command(label="show terminal Ctrl+T", command=lambda:self.hideAndShowTerminal('show'))
        self.menu_view.add_command(label='hide terminal Ctrl+T', command=lambda:self.hideAndShowTerminal('hide'))
                
        # menu tools
        self.pythonshell = PythonShell(self.text, self.text_in_terminal)
        self.menu_tools.add_command(label='Build Ctrl+B', command=lambda:self.ctrl_B('<Control-b>'))

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
        self.text.bind('<KeyRelease>', self.groupFonction)
        self.file_list.bind('<<ListboxSelect>>', self.fillOut)
        self.bind('<Control-s>', self.ctrl_S)
        self.bind('<Control-b>', self.ctrl_B)
        self.bind('<Control-o>', (lambda e:self.insertion()))
        self.bind('<Control-q>', (lambda e:self.quit()))
        self.bind('<Control-y>', self.ctrl_Y)
        self.term_mod = 'show'
        self.bind('<Control-t>', (lambda e:self.hideAndShowTerminal(self.term_mod)))

    def scroll_yview(self, *args):
        self.line_number.yview(*args)
        self.text.yview(*args)
    
    def ctrl_Y(self, e):
        try:
            self.text.edit_redo()
        except:
            pass
        
    def ctrl_S(self, e):
        saveFile(self.text.get(1.0,END),self.file_active_now, self.insertion)
    
    def ctrl_B(self, e):
        self.hideAndShowTerminal('show')
        try:
            self.pythonshell.build(self.dic[self.file_active_now], 'buildAndWrite', self.insertion)
        except:
            self.pythonshell.build(None, 'buildAndWrite', self.insertion)
    
    def fillOut(self,e):
        try:
            self.activeFile(self.dic[self.file_list.get(ACTIVE)])
        except:
            pass
    
    def changeFont(self, font_family):
            self.font_active_now = font_family
            self.text.configure(font=(font_family, 11))
    
    def activeFile(self, directory):
        '''
        1- Change the current directory
        2- verify if self.acitve_now
        3- delete all and read file on the directory and insert this
        4- set title
        5- call groupFonction
        fromule loi de poisson

        :return: None
        '''
        os.chdir('/'.join(directory.split('/')[:-1])) # change the current directory
        if self.file_active_now != directory.split('/')[-1]:
            self.file_active_now = directory.split('/')[-1]
            self.text.delete(1.0, END)
            with open(directory, 'r') as file_text:
                self.text.insert(END, file_text.read())
            self.title(f'{directory} - magic-text')
        self.groupFonction('<KeyRelease>')
        
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
        7- call fonction groupFonction
        8- Add Button and her command

        :return: None
        '''
        if mode == None:
            name, content , directory = openFile()
        self.file_active_now = name
        self.dic[name] = directory
        self.title(f'{directory} - magic-text')
        self.file_list.insert(END, name)
        self.text.delete(1.0, END)
        self.text.insert(END, content)
        self.groupFonction('<KeyRelease>')
        Button(self.frame_top_right, text=name,
                command=lambda:(self.activeFile(self.dic[name])),
                bg='#262626', fg='#5A5C58', width=15, 
                ).pack(side='left')
    
    def hideAndShowTerminal(self, mode):
        try:
            if mode == "show":
                self.terminal.pack(side='bottom', fill='x', ipady=35)
                self.term_mod = 'hide'
            elif mode == "hide":
                self.term_mod = 'show'
                self.terminal.destroy()
                self.terminal = Entry(self.right, bg=app_background, fg=app_foreground, font=('Courier New', 14), textvariable=self.text_in_terminal)
        except:
            pass

    def updateLineNumber(self):
        # 1- effacer la line_number
        # 2- recupere le nombre de ligne
        # 3- insert le nombre de ligne
        # configure la taille width line_number en fonction de la taille des chiffre
        self.line_number.delete(0, END)
        line = len(self.text.get(1.0, END).split('\n'))
        list = []
        for i in range(1, line):
            self.line_number.insert(END, str(i))
            list.append(i)
        self.line_number.config(width=len(str(max(list)))) 

    def groupFonction(self, e):
        fonction_ = r'(if |elif |else:|def |for |while |try:|except|class|from |import | as | in |return )'
        string = r'(".+\"|\'.+\')'
        autre = r'(print|.set|.get|self)'
        attribute_ = r'(\.\w+)'
        commentaire_ = r'(#.+)'
        integer = r'(\d+)'

        self.color('fonction', fonction_, '#D25D5B')
        self.color('autre', autre, '#CA7A02')
        self.color('attribute', attribute_, '#3F82AC')
        self.color('string', string, '#DFDC11')
        self.color('commentaire', commentaire_, '#BEBEBE')
        self.color('integer', integer, "#F9710A")
        self.updateLineNumber()
    
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
