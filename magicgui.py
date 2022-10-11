from tkinter import (
        Tk, Text, Listbox, Button, StringVar, Menu,
        Scrollbar, filedialog, PhotoImage
)
import os
import customtkinter
from mycustomwidget.text import TextWithColorisation
from plugin.colorshemes import Colorscheme


BACKGROUND_COLOR = "#181915"
FOREGROUND_COLOR = "white"
CURSOR = "white"
MENU_BACKGROUND_COLOR = "white"
MENU_FOREGROUND_COLOR = "#1E201C"
CURRENT_DIRECTORY = os.path.abspath('.')

customtkinter.set_appearance_mode("System")

class MagicGui(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('magic-text')
        self.geometry("1000x800")
        self.files_dictionary = {}
        self.file_active_now = None
        self.call('wm', 'iconphoto', self._w,
            PhotoImage(file=os.path.join(CURRENT_DIRECTORY, 'magic.png'))
        )
        self.font_active_now = 'mononoki'
        self.font_size = 11

        self.colorscheme = Colorscheme(
            path=os.path.join(CURRENT_DIRECTORY, 'plugin/colorshemes'),
            title_colorscheme='Monokai'
        )

        self.main_frame = customtkinter.CTkFrame(self, bg=BACKGROUND_COLOR)

        self.left_frame = customtkinter.CTkFrame(self.main_frame, bg=BACKGROUND_COLOR, height=0)
        self.enthete = customtkinter.CTkLabel(
            self.left_frame,
            bg=self.colorscheme.color['normal-background'],
            fg=self.colorscheme.color['normal-foreground'],
            text=''
        )
        self.enthete.pack(ipady=7)

        self.file_list = Listbox(
            self.left_frame, bg=self.colorscheme.color['normal-background'],
            fg=self.colorscheme.color['normal-foreground'], width=20, height=48,
            font=(self.font_active_now, self.font_size)
        )

        self.file_list.pack()
        self.left_frame.pack(side='left', fill='y')

        self.right_frame = customtkinter.CTkFrame(self.main_frame, bg=BACKGROUND_COLOR)

        self.frame_top_right = customtkinter.CTkFrame(self.right_frame, bg=BACKGROUND_COLOR, height=0)
        self.file_name = StringVar()
        self.frame_top_right.pack(fill="x")

        self.frame_bottom_right = customtkinter.CTkFrame(self.right_frame)
        self.yscrollbar = Scrollbar(self.frame_bottom_right)
        self.yscrollbar.pack(side="right", fill='y')
        self.line_number = Listbox(
                self.frame_bottom_right, width=1, height=30, font=(None, 11),
                fg=self.colorscheme.color['linenumber-foreground'],
                bg=self.colorscheme.color['linenumber-background'],
                yscrollcommand=self.yscrollbar.set
        )
        self.line_number.pack(side='left', fill='y')
        self.textarea = TextWithColorisation(
            self.frame_bottom_right,
            width=700,
            height=31,
            maxundo=-1,
            undo=True,
            autoseparators=True,
            fg=self.colorscheme.color['normal-foreground'],
            bg=self.colorscheme.color['normal-background'],
            insertbackground=self.colorscheme.color['cursor-foreground'],
            font=(self.font_active_now, self.font_size),
            yscrollcommand=self.yscrollbar.set
        )
        self.textarea.pack(side='left', fill='y')

        self.frame_bottom_right.pack(side='top', fill='y', expand=1)

        self.terminal = Text(self.right_frame, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=('Courier New', 10))
        self.right_frame.pack(side='right', fill='y')

        self.main_frame.pack(fill='x')

        # Barre de menu
        self.menu = Menu(self, bg=MENU_BACKGROUND_COLOR, fg=MENU_FOREGROUND_COLOR)
        self.menu_file = Menu(self.menu, bg=MENU_BACKGROUND_COLOR, fg=MENU_FOREGROUND_COLOR, tearoff=0)
        self.menu_view = Menu(self.menu, bg=MENU_BACKGROUND_COLOR, fg=MENU_FOREGROUND_COLOR, tearoff=0)
        self.menu_preference = Menu(self.menu, bg=MENU_BACKGROUND_COLOR, fg=MENU_FOREGROUND_COLOR, tearoff=0)
        self.menu_tools = Menu(self.menu, bg=MENU_BACKGROUND_COLOR, fg=MENU_FOREGROUND_COLOR, tearoff=0)

        # add menu file into menu
        self.menu.add_cascade(label='File', menu=self.menu_file)
        self.menu.add_cascade(label='View', menu=self.menu_view)
        self.menu.add_cascade(label='Tools', menu=self.menu_tools)
        self.menu.add_cascade(label='Preference', menu=self.menu_preference)

       # preference
        self.menu_font = Menu(self.menu_preference, bg=MENU_BACKGROUND_COLOR, fg=MENU_FOREGROUND_COLOR, tearoff=0)
        self.menu_colorscheme = Menu(self.menu_preference, bg=MENU_BACKGROUND_COLOR, fg=MENU_FOREGROUND_COLOR, tearoff=0)
        self.menu_preference.add_cascade(label='font', menu=self.menu_font)
        self.menu_preference.add_cascade(label='select colorscheme', menu=self.menu_colorscheme)

        self.config(menu=self.menu, bg=MENU_BACKGROUND_COLOR)


if __name__ == "__main__":
    guimagic = MagicGui()
    guimagic.mainloop()
