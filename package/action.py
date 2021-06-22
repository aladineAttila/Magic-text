#!/usr/bin/env python3
import os
from tkinter import (filedialog, Toplevel, Entry,
        StringVar, Button, Label, Frame, END
        )


class PythonShell:
    def __init__(self, body, entry_content):
        self.body = body
        self.entry_content = entry_content
    
    def build(self, file_path, mode=None, fonction_=None):
        code = self.body.get(1.0, END)
        if file_path:
            if mode == "buildAndWrite":
                with open(file_path, 'w') as code_file:
                    code_file.write(code)
        else:
            file_path = saveFile(content=self.body.get(1.0, END), fonction=fonction_)
        output = os.popen(f'python3 {file_path}').read()
        self.entry_content.set(output)


def saveFile(content ,file_name=None, fonction=None):
    '''
    args = content, file_name, fonction None by default

    1- if file_name is None asksaveasfile and write content inside
    2- call fonction insertion with fonction()
    3- else save file with content

    :return: None
    '''
    if file_name == None:
        files = filedialog.asksaveasfile(title='entre le nom de votre fichier', mode='w')
        print(files)
        with open(files.name, 'w') as file_text:
            file_text.write(content)
            file_name = files.name.split('/')[-1]
            fonction('',file_name, content, files.name)
            return files.name
        
    else:
        with open(f"{file_name}", 'w') as text:
            text.write(content)

    
def openFileOrFolder(thing):
    if thing == 'file':
        files =  filedialog.askopenfiles(title='select file to open on magic-text', mode='rb')
        os.chdir('/'.join(files[0].name.split('/')[:-1]))
        for file_ in files:
            with open(file_.name, 'r') as file_text:
                return file_.name.split('/')[-1],file_text.read(), file_.name
    elif thing == "folder":
        folders = filedialog.askdirectory(initialdir='/', title='Select folder to open on magic-text')
        return folders


if __name__ == "__main__":
    #openFileOrFolder('file')
    #popup('test')
    pass
