
#!/usr/bin/env python3
import argparse
import os

current_directory = os.path.abspath(".")
# ext and here command
file_map = {
    "py": "python {0}",
    "rs": "cargo run",
    "cpp": "g++ {0} -o {1} && ./{1}",
    "c": "gcc {0} -o {1} && ./{1}",
}

def build(file_path):
    file = file_path.split(".")
    if len(file) == 2 and os.path.exists(os.path.join(current_directory, file_path)):
        name, ext = file
        command = file_map[ext]
        if ext == "py":
            return os.popen(command.format(file_path)).read()
        elif ext == "rs":
            os.popen(command)
        elif ext == "cpp" or ext == "c":
            return os.popen(command.format(file_path, name)).read()
        else:
            return "this programme can't compile or run this file"
    else:
        return "file not found"

