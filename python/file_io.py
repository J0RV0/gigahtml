import json, os, re
from functions import parse_tag, remove_repeats

def copy_component(path):
    file = open(path, "r")
    output = file.read()
    file.close()
    return output

def listdir_recursive(directory):
    html_files = []
    static_files = []
    directories = []
    dirs = [directory]
    while len(dirs) > 0:
        current = dirs[0]
        for item in os.listdir(current):
            item = os.path.join(current, item)
            if os.path.isdir(item):
                dirs.append(item)
                directories.append(item)
            elif file_ext(item) == ".html":
                html_files.append(item)
            else:
                static_files.append(item)
        del dirs[0]
    return html_files, static_files, directories

def read_json(path):
    return json.loads(open(path, "r").read())

def file_ext(path):
    return os.path.splitext(path)[1]

def write_component(comp_obj, path):
    file = open(path, "w")
    file.write(comp_obj)
    file.close()
