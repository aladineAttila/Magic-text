import os
import customtkinter
from magicgui import MagicGui, CURRENT_DIRECTORY, MENU_BACKGROUND_COLOR
from tkinter import filedialog
from plugin.builder import build
from plugin.colorshemes import Colorscheme


class MagicFonctionalityWithGui(MagicGui):
    def __init__(self):
        super().__init__()

        self.yscrollbar.config(command=self.scrollYview)

        # menu file
        self.menu_file.add_command(
            label="Save Ctrl+S", command=lambda: self.ctrlS("<Control+s>")
        )
        self.menu_file.add_command(
            label="Open file Ctrl+O", command=self.insertContentOnTextarea
        )
        self.menu_file.add_command(label="Quit Ctrl+Q", command=self.quit)

        # menu view
        self.menu_view.add_command(
            label="Show terminal Ctrl+T",
            command=lambda: self.hideAndShowTerminal("show"),
        )
        self.menu_view.add_command(
            label="Hide terminal Ctrl+T",
            command=lambda: self.hideAndShowTerminal("hide"),
        )

        # menu tools
        self.menu_tools.add_command(
            label="Build Ctrl+B", command=lambda: self.ctrlB("<Control-b>")
        )

        self.font = ("mononoki", "ubuntu")

        self.menu_font.add_command(
            label=self.font[0], command=lambda: self.changeFont(self.font[0])
        )
        self.menu_font.add_command(
            label=self.font[1], command=lambda: self.changeFont(self.font[1])
        )

        self.the_color = [color for color in self.colorscheme.colorscheme]

        self.menu_colorscheme.add_command(
            label=self.the_color[0],
            command=lambda: self.changeColorscheme(title=self.the_color[0]),
        )
        self.menu_colorscheme.add_command(
            label=self.the_color[1],
            command=lambda: self.changeColorscheme(title=self.the_color[1]),
        )
        self.menu_colorscheme.add_command(
            label=self.the_color[2],
            command=lambda: self.changeColorscheme(title=self.the_color[2]),
        )
        self.menu_colorscheme.add_command(
            label=self.the_color[3],
            command=lambda: self.changeColorscheme(title=self.the_color[3]),
        )

        self.config(menu=self.menu, bg=MENU_BACKGROUND_COLOR)

        self.textarea.bind("<KeyRelease>", self.updateTheLineNumberAndColorText)
        self.file_list.bind("<<ListboxSelect>>", self.fillOut)
        self.textarea.bind("<Return>", self.autoIndent)

        self.bind("<Control-s>", self.ctrlS)
        self.bind("<Control-b>", self.ctrlB)
        self.bind("<Control-o>", (lambda e: self.insertContentOnTextarea()))
        self.bind("<Control-q>", (lambda e: self.quit()))
        self.bind("<Control-y>", self.ctrlY)

        self.term_mod = "show"
        self.bind("<Control-t>", (lambda e: self.hideAndShowTerminal(self.term_mod)))

    def scrollYview(self, *args) -> None:
        self.line_number.yview(*args)
        self.textarea.yview(*args)

    def ctrlY(self, event: str) -> None:
        try:
            self.textarea.edit_redo()
        except:
            pass

    def fillOut(self, event: str) -> None:
        try:
            self.activeFile(self.files_dictionary[self.file_list.get("active")])
        except:
            pass

    def changeFont(self, font_family: str) -> None:
        self.font_active_now = font_family
        self.textarea.configure(font=(font_family, self.font_size))
        # print(font_family)

    def activeFile(self, directory: str) -> None:
        # change the current directory
        os.chdir("/".join(directory.split("/")[:-1]))
        file_name = directory.split("/")[-1]
        if self.file_active_now != file_name:
            self.file_active_now = file_name
            self.textarea.delete(1.0, "end")
            with open(directory, "r") as file_text:
                self.textarea.insert("end", file_text.read())
            self.title(f"{directory} - magic-text")
        self.updateTheLineNumberAndColorText("<KeyRelease>")

    def insertContentOnTextarea(
        self, name: str = None, content: str = None, directory: str = None
    ) -> None:
        name, content, directory = self.openFile()
        if name and content and directory:
            self.file_active_now = name
            if name not in self.files_dictionary:
                self.files_dictionary[name] = directory
                self.title(f"{directory} - magic-text")
                self.file_list.insert("end", name)
                self.textarea.delete(1.0, "end")
                self.textarea.insert("end", content)
                self.updateTheLineNumberAndColorText("<KeyRelease>")
                button = customtkinter.CTkButton(
                    self.frame_top_right,
                    text=name,
                    fg_color=self.colorscheme.color["normal-foreground"],
                    command=lambda: (self.activeFile(self.files_dictionary[name])),
                    width=15,
                )
                button.pack(side="left", ipady=4, ipadx=10)

    def saveFile(self, content: str, file_path: str = None) -> str:
        try:
            if file_path is None:
                files = filedialog.asksaveasfile(
                    title="entre le nom de votre fichier", mode="w"
                )
                file_path = files.name
                with open(files.name, "w") as file_text:
                    file_text.write(content)
                    name_of_file = file_path.split("/")[-1]
                    self.insertContentOnTextarea(name_of_file, content, file_path)
            else:
                with open(f"{file_path}", "w") as file_text:
                    file_text.write(content)
            return file_path

        except AttributeError:
            pass

    def ctrlS(self, event: str) -> None:
        self.saveFile(self.textarea.get(1.0, "end"), self.file_active_now)

    def hideAndShowTerminal(self, mode):
        try:
            if mode == "show":
                self.term_mod = "hide"
                self.terminal.pack(side="bottom", fill="x", ipady=5)
            elif mode == "hide":
                self.term_mod = "show"
                self.terminal.forget()
        except:
            pass

    def build(self, file_path: str, mode: str = None) -> None:
        code = self.textarea.get(1.0, "end")
        if file_path and mode == "buildAndWrite":
            with open(file_path, "w") as code_file:
                code_file.write(code)
        else:
            file_path = self.saveFile(content=self.textarea.get(1.0, "end"))
        output = build(file_path)
        self.terminal.delete(1.0, "end")
        self.terminal.insert("end", output)

    def ctrlB(self, event: str) -> None:
        self.hideAndShowTerminal("show")
        try:
            self.build(self.files_dictionary[self.file_active_now], "buildAndWrite")
        except:
            self.build(None, "buildAndWrite")

    def openFile(self) -> tuple[str | None]:
        try:
            files = filedialog.askopenfiles(
                title="select file to open on magic-text", mode="rb"
            )
            os.chdir("/".join(files[0].name.split("/")[:-1]))
            for file_ in files:
                with open(file_.name, "r") as file_text:
                    name = file_.name.split("/")[-1]
                    content = file_text.read()
                    path = file_.name
                    return name, content, path
        except:
            return None, None, None

    def colorTheKeyWordInTextarea(self, type_, regex, foreground, background):
        try:
            self.textarea.tag_configure(
                type_,
                font=(self.font_active_now, self.font_size),
                foreground=foreground,
                background=background,
            )
            indices = self.textarea.findall(regex)
            self.textarea.tag_add(type_, *indices)

        except Exception as e:
            pass

    def updateLineNumber(self):
        self.line_number.delete(0, "end")
        line = len(self.textarea.get(1.0, "end").split("\n"))
        list_line = []
        for i in range(1, line):
            self.line_number.insert("end", str(i))
            list_line.append(i)
        self.line_number.config(width=len(str(max(list_line))))

    def updateTheLineNumberAndColorText(self, event: str) -> None:
        self.updateLineNumber()
        for key_color in self.colorscheme.dict_color:
            self.colorTheKeyWordInTextarea(*self.colorscheme.dict_color[key_color])

    def changeColorscheme(self, title: str) -> None:
        self.colorscheme = Colorscheme(
            path=f"{CURRENT_DIRECTORY}/plugin/colorshemes", title_colorscheme=title
        )
        self.textarea.config(
            fg=self.colorscheme.color["normal-foreground"],
            bg=self.colorscheme.color["normal-background"],
            insertbackground=self.colorscheme.color["cursor-foreground"],
        )
        self.line_number.config(
            fg=self.colorscheme.color["linenumber-foreground"],
            bg=self.colorscheme.color["linenumber-background"],
        )
        self.file_list.config(
            fg=self.colorscheme.color["normal-foreground"],
            bg=self.colorscheme.color["normal-background"],
        )
        self.terminal.config(
            fg=self.colorscheme.color["normal-foreground"],
            bg=self.colorscheme.color["normal-background"],
        )
        self.updateTheLineNumberAndColorText("<KeyRelease>")

    def autoIndent(self, e) -> str:
        end_line = self.textarea.get("insert linestart", "insert lineend")
        if len(end_line.strip("\t")):
            tab_size = len([t for t in end_line.split("    ") if t == ""])
            try:
                if end_line[-1] in [":", "{"]:
                    self.textarea.insert("insert", "\n" + "    " * (tab_size + 1))
                else:
                    self.textarea.insert("insert", "\n" + "    " * tab_size)
                return "break"
            except IndexError:
                pass
        else:
            pass


if __name__ == "__main__":
    magic = MagicFonctionalityWithGui()
    magic.mainloop()
