#!/usr/bin/env python3
import os
from tkinter import (
        Tk, Text, Listbox, Button, StringVar, END, Menu,
        ACTIVE, Scrollbar, filedialog, PhotoImage
)
import customtkinter

from mywidget.text import TextWithColorisation
from plugin.colorshemes import Colorscheme

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

BACKGROUND = "#181915"
FOREGROUND = "white"
TEXT_BACKGROUND = "#2C2E28"
TEXT_FOREGROUND = "white"
CURSOR = "white"
MENU_BACKGROUND = "white"
MENU_FOREGROUND = "#1E201C"
CURRENT_DIRECTORY = os.path.abspath('.')


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('magic-text')
        self.geometry("1000x800")
        self.dic = {}
        self.file_active_now = None
        self.call('wm', 'iconphoto', self._w, PhotoImage(file='sublike.png'))
        self.colorscheme = Colorscheme(f'{CURRENT_DIRECTORY}/plugin/colorshemes', 'IDLE Classic')

        # customtkinter.CTkFrame principal
        self.main_frame = customtkinter.CTkFrame(self, bg=BACKGROUND)

        # left frame contient file_list
        self.left_frame = customtkinter.CTkFrame(self.main_frame, bg=BACKGROUND)
        self.enthete = customtkinter.CTkLabel(self.left_frame, bg=BACKGROUND, fg='#9E9F9B', text='FILES').pack(ipady=4)
        self.file_list = Listbox(self.left_frame, bg=self.colorscheme.color['normal-background'],
                                 fg=self.colorscheme.color['normal-foreground'], width=20, height=48)
        self.file_list.pack()
        self.left_frame.pack(side='left', fill='y')

        # right frame contient text editor and label button
        # et le scrollbar et la linenumber
        self.right = customtkinter.CTkFrame(self.main_frame, bg=BACKGROUND)

        # top barre
        self.frame_top_right = customtkinter.CTkFrame(self.right, bg=BACKGROUND, height=0)
        self.file_name = StringVar()
        self.frame_top_right.pack(fill="x")

        # text editor
        self.frame_bottom_right = customtkinter.CTkFrame(self.right)
        self.scrollbar = Scrollbar(self.frame_bottom_right)
        self.scrollbar.pack(side="right", fill='y')
        self.line_number = Listbox(self.frame_bottom_right, width=1, height=31, font=(None, 11),
                                   fg=self.colorscheme.color['linenumber-foreground'],
                                   bg=self.colorscheme.color['linenumber-background'],
                                   yscrollcommand=self.scrollbar.set)
        self.line_number.pack(side='left', fill='y')
        self.textarea = TextWithColorisation(self.frame_bottom_right, undo=True, autoseparators=True, maxundo=-1,
                                             fg=self.colorscheme.color['normal-foreground'],
                                             bg=self.colorscheme.color['normal-background'], width=1000, height=31,
                                             yscrollcommand=self.scrollbar.set)
        self.textarea.pack(side='left', fill='y')
        self.scrollbar.config(command=self.scrollYview)
        self.font_active_now = 'Courier New'
        self.textarea.configure(insertbackground=self.colorscheme.color['cursor-foreground'], font=('Courier New', 11))
        self.frame_bottom_right.pack(side='top', fill='y', expand=1)

        # terminal
        self.terminal = Text(self.right, bg=BACKGROUND, fg=FOREGROUND, font=('Courier New', 10))
        self.right.pack(side='right', fill='y')

        self.main_frame.pack(fill='x')

        # Barre de menu
        self.menu = Menu(self, bg=MENU_BACKGROUND, fg=MENU_FOREGROUND)
        self.menu_file = Menu(self.menu, bg=MENU_BACKGROUND, fg=MENU_FOREGROUND, tearoff=0)
        self.menu_view = Menu(self.menu, bg=MENU_BACKGROUND, fg=MENU_FOREGROUND, tearoff=0)
        self.menu_preference = Menu(self.menu, bg=MENU_BACKGROUND, fg=MENU_FOREGROUND, tearoff=0)
        self.menu_tools = Menu(self.menu, bg=MENU_BACKGROUND, fg=MENU_FOREGROUND, tearoff=0)

        # add menu file into menu
        self.menu.add_cascade(label='File', menu=self.menu_file)
        self.menu.add_cascade(label='View', menu=self.menu_view)
        self.menu.add_cascade(label='Tools', menu=self.menu_tools)
        self.menu.add_cascade(label='Preference', menu=self.menu_preference)

        # menu file
        self.menu_file.add_command(label='Save Ctrl+S', command=lambda: self.ctrlS('<Control+s>'))
        self.menu_file.add_command(label='Open file Ctrl+O', command=self.insertion)
        self.menu_file.add_command(label='Quit Ctrl+Q', command=self.quit)

        # menu view
        self.menu_view.add_command(label="Show terminal Ctrl+T", command=lambda: self.hideAndShowTerminal('show'))
        self.menu_view.add_command(label='Hide terminal Ctrl+T', command=lambda: self.hideAndShowTerminal('hide'))

        # menu tools
        self.menu_tools.add_command(label='Build Ctrl+B', command=lambda: self.ctrlB('<Control-b>'))

        # preference
        self.menu_font = Menu(self.menu_preference, bg=MENU_BACKGROUND, fg=MENU_FOREGROUND, tearoff=0)
        self.menu_colorscheme = Menu(self.menu_preference, bg=MENU_BACKGROUND, fg=MENU_FOREGROUND, tearoff=0)
        self.menu_preference.add_cascade(label='font', menu=self.menu_font)
        self.menu_preference.add_cascade(label='select colorscheme', menu=self.menu_colorscheme)
        # font_tuple = font.families()
        font_tuple = ("Comic Sans MS", "Courier New", "Helvetica", "Times New Roman")

        # for font_family in font_tuple:
        #     self.menu_font.add_command(label=font_family, command=lambda:self.changeFont(font_family))
        # self.menu_font.add_command(label=font_tuple[0], command=lambda:self.changeFont(font_tuple[0]))
        # self.menu_font.add_command(label=font_tuple[1], command=lambda:self.changeFont(font_tuple[1]))
        # self.menu_font.add_command(label=font_tuple[2], command=lambda:self.changeFont(font_tuple[2]))
        # self.menu_font.add_command(label=font_tuple[3], command=lambda:self.changeFont(font_tuple[3]))

        # self.menu_colorscheme.add_command(label=color, command=lambda:self.change_colorsheme(color))
        self.the_color = [color for color in self.colorscheme.colorschemes]

        self.menu_colorscheme.add_command(label=self.the_color[0],
                                          command=lambda: self.change_colorsheme(self.the_color[0]))
        self.menu_colorscheme.add_command(label=self.the_color[1],
                                          command=lambda: self.change_colorsheme(self.the_color[1]))
        self.menu_colorscheme.add_command(label=self.the_color[2],
                                          command=lambda: self.change_colorsheme(self.the_color[2]))
        self.menu_colorscheme.add_command(label=self.the_color[3],
                                          command=lambda: self.change_colorsheme(self.the_color[3]))

        self.config(menu=self.menu, bg=MENU_BACKGROUND)

        # key binding
        self.textarea.bind('<KeyRelease>', self.groupFonction)
        self.file_list.bind('<<ListboxSelect>>', self.fillOut)
        self.bind('<Control-s>', self.ctrlS)
        self.bind('<Control-b>', self.ctrlB)
        self.bind('<Control-o>', (lambda e: self.insertion()))
        self.bind('<Control-q>', (lambda e: self.quit()))
        self.bind('<Control-y>', self.ctrlY)
        self.term_mod = 'show'
        self.bind('<Control-t>', (lambda e: self.hideAndShowTerminal(self.term_mod)))
        self.textarea.bind('<Return>', self.autoIndent)

    def scrollYview(self, *args):
        self.line_number.yview(*args)
        self.textarea.yview(*args)

    def ctrlY(self, e: str) -> None:
        try:
            self.textarea.edit_redo()
        except:
            pass

    def ctrlS(self, e: str) -> None:
        self.saveFile(self.textarea.get(1.0, END), self.file_active_now)

    def ctrlB(self, e: str) -> None:
        self.hideAndShowTerminal('show')
        try:
            self.build(self.dic[self.file_active_now], 'buildAndWrite')
        except:
            self.build(None, 'buildAndWrite')

    def fillOut(self, e: str) -> None:
        try:
            self.activeFile(self.dic[self.file_list.get(ACTIVE)])
        except:
            pass

    def changeFont(self, font_family: str) -> None:
        self.font_active_now = font_family
        self.textarea.configure(font=(font_family, 11))

    def activeFile(self, directory: str) -> None:
        """
        1- Change the current directory
        2- verify if self.acitve_now
        3- delete all and read file on the directory and insert this
        4- set title
        5- call groupFonction
        :param directory:
        :return: None
        """
        os.chdir('/'.join(directory.split('/')[:-1]))  # change the current directory
        file_name = directory.split('/')[-1]
        if self.file_active_now != file_name:
            self.file_active_now = file_name
            self.textarea.delete(1.0, END)
            with open(directory, 'r') as file_text:
                self.textarea.insert(END, file_text.read())
            self.title(f'{directory} - magic-text')
        self.groupFonction('<KeyRelease>')

    def insertion(self, mode: str=None, name: str=None, content: str=None, directory: str=None) -> None:
        """
        1- get name, contenu, directory
        2- set file_active_now to name
        3- add directory in dic
        4- set title
        5- add name to file_list
        6- delete all and insert content
        7- call fonction groupFonction
        8- Add Button and her command
        :param mode:
        :param name:
        :param content:
        :param directory:
        :return: None
        """
        if mode is None:
            name, content, directory = self.openFile()

        if name and content and directory:
            self.file_active_now = name
            # si la cle existe deja dans le dictionnaire
            if name not in self.dic:
                self.dic[name] = directory
                self.title(f'{directory} - magic-text')
                self.file_list.insert(END, name)
                self.textarea.delete(1.0, END)
                self.textarea.insert(END, content)
                self.groupFonction('<KeyRelease>')
                Button(self.frame_top_right, text=name, relief='flat',
                       command=lambda: (self.activeFile(self.dic[name])), bg=TEXT_BACKGROUND, fg='white',
                       width=15).pack(side='left', ipady=4)

    def saveFile(self, content: str, file_name: str=None) -> str:
        """
        1- if file_name is None asksaveasfile and write content inside
        2- else save file with content

        :param content:
        :param file_name:
        :return: file_path
        """
        try:
            if file_name is None:
                files = filedialog.asksaveasfile(title='entre le nom de votre fichier', mode='w')
                with open(files.name, 'w') as file_text:
                    file_text.write(content)
                    file_name = files.name.split('/')[-1]
                    self.insertion('', file_name, content, files.name)
                    return files.name

            else:
                with open(f"{file_name}", 'w') as file_text:
                    file_text.write(content)
                    return files.name
        except AttributeError:
            pass

    def build(self, file_path: str, mode: str=None) -> None:
        """
        1- get text content
        2- verify is file_path exist
            write content in code_file
            or
            call fonction saveFile
        3- exectute code_file in file_path
        4- print her output

        :param file_path:
        :param mode:
        :return: None
        """
        code = self.textarea.get(1.0, END)
        if file_path:
            if mode == "buildAndWrite":
                with open(file_path, 'w') as code_file:
                    code_file.write(code)
        else:
            file_path = self.saveFile(content=self.textarea.get(1.0, END))
        output = os.popen(f'python {file_path}').read()
        self.terminal.delete(1.0, END)
        self.terminal.insert(END, output)

    def openFile(self) -> tuple:
        """
        args = None

        1- openfiles dialog
        2- change the current directory
        3- open file
        
        :return: name, content, directory
        """
        try:
            files = filedialog.askopenfiles(title='select file to open on magic-text', mode='rb')
            os.chdir('/'.join(files[0].name.split('/')[:-1]))
            for file_ in files:
                with open(file_.name, 'r') as file_text:
                    name = file_.name.split("/")[-1]
                    content = file_text.read()
                    path = file_.name
                    return name, content, path
        except:
            return None, None, None

    def hideAndShowTerminal(self, mode):
        try:
            if mode == "show":
                self.term_mod = 'hide'
                self.terminal.pack(side='bottom', fill='x', ipady=5)
            elif mode == "hide":
                self.term_mod = 'show'
                self.terminal.forget()
        except:
            pass

    def color(self, type_, regex, foreground_, background_):
        try:
            self.textarea.tag_configure(type_, font=(self.font_active_now, 11, 'bold'), foreground=foreground_,
                                        background=background_)
            indices = self.textarea.findall(regex)

            self.textarea.tag_add(type_, *indices)

        except Exception as e:
            pass

    def updateLineNumber(self):
        """
        args = None

        1- effacer la line_number
        2- recupere le nombre de ligne
        3- insert le nombre de ligne
        configure la taille width line_number en fonction de la taille des chiffre

        :return: None
        """
        self.line_number.delete(0, END)
        line = len(self.textarea.get(1.0, END).split('\n'))
        list = []
        for i in range(1, line):
            self.line_number.insert(END, str(i))
            list.append(i)
        self.line_number.config(width=len(str(max(list))))

    def groupFonction(self, e):
        self.color(*self.colorscheme.keyword)
        self.color(*self.colorscheme.function)
        self.color(*self.colorscheme.parenthese)
        self.color(*self.colorscheme.char)
        self.color(*self.colorscheme.string)
        self.color(*self.colorscheme.comment)
        self.updateLineNumber()

    def change_colorsheme(self, title_colorschemes):
        self.colorscheme = Colorscheme(f'{CURRENT_DIRECTORY}/plugin/colorshemes', title_colorschemes)
        self.textarea.config(fg=self.colorscheme.color['normal-foreground'],
                             bg=self.colorscheme.color['normal-background'],
                             insertbackground=self.colorscheme.color['cursor-foreground'])
        self.line_number.config(fg=self.colorscheme.color['linenumber-foreground'],
                                bg=self.colorscheme.color['linenumber-background'])
        self.file_list.config(fg=self.colorscheme.color['normal-foreground'],
                              bg=self.colorscheme.color['normal-background'])
        self.groupFonction('')
    
    def autoIndent(self, e):
        """
        args Event

        1- get la dernier ligne
        2- get nombre de tab
        3- insert tab
        
        :return: break
        """
        end_line = self.textarea.get('insert linestart', 'insert lineend')
        tab = len([t for t in end_line.split('    ') if t == ''])
        try:
            if end_line[-1] == ':':
                self.textarea.insert('insert', "\n" + "    " * (tab + 1))
            else:
                self.textarea.insert('insert', "\n" + "    " * tab)
            return 'break'
        except IndexError:
            pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
