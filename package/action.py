#!/usr/bin/env python3
import os
from tkinter import (filedialog, Toplevel, Entry,
        StringVar, Button, Label, Frame
        )

def popup(content):
    app = Toplevel()
    app.geometry("250x100")
    file_name = StringVar()
    Label(app, text='Enter the name of file').pack()
    frame = Frame(app)
    Entry(frame, textvariable=file_name).pack(side='left')
    def entre(file_name):
        with open(f"{file_name}", 'w') as text:
            if file_name != 'nothing' or file_name != "" or file_name != " ":
                text.write(content)
                app.destroy()
    Button(frame, text='entre', command=lambda:(entre(file_name.get()))).pack(side='right')
    frame.pack()
    


def saveFile(content ,file_name, extension=None):
    if file_name == 'nothing':
        popup(content)

    if extension is None:
        with open(f"{file_name}", 'w') as text:
            text.write(content)
            return 1
    else:
        with open(f"{file_name}.{extension}", w) as text:
            text.write(content)
            return 1
    return 0

def openFileOrFolder(thing):
    if thing == 'file':
        files =  filedialog.askopenfiles(title='select file to open on magic-text', mode='rb')
        os.chdir('/'.join(files[0].name.split('/')[:-1]))
        for file_ in files:
            with open(f'{file_.name}', 'r') as file_text:
                return file_.name.split('/')[-1],file_text.read(), file_.name
    elif thing == "folder":
        folders = filedialog.askdirectory(initialdir='/', title='Select folder to open on magic-text')
        return folders


if __name__ == "__main__":
    #openFileOrFolder('file')
    popup('test')
