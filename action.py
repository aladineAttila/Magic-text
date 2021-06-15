#!/usr/bin/env python3
import os
from tkinter import filedialog


def saveFile(content ,file_name, extension=None):
    if extension is None:
        with open(f"{file_name}", 'w') as text:
            text.write(content)
    else:
        with open(f"{file_name}.{extension}", w) as text:
            text.write(content)
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
    openFileOrFolder('file')
