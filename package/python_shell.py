from tkinter import END
from os import popen

class PythonShell:
    def __init__(self, body, entry_content):
        self.body = body
        self.entry_content = entry_content
    
    def get_text(self):
        code = self.body.get(1.0, END)
        with open('.cache/idle.magic', 'w') as code_file:
            code_file.write(code)
        output = popen(f'python3 .cache/idle.magic').read()
        self.entry_content.set(output)

