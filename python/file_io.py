import json, os, re
from functions import parse_tag, remove_repeats

def match_component_tags(comp_obj):

    # list all component tags in comp_obj
    raw_tags = re.findall("<%.*?>", comp_obj)

    # create tag objects from tag text
    component_tags = []
    for tag in raw_tags:
        tag = parse_tag(tag)
        component_tags.append(tag)

    return component_tags

def match_references(comp_obj, symbol, parenthesis = "{"):
    if symbol == "$":
        symbol = "\$"

    if parenthesis == "{":
        opening = "{"
        closing = "}"
    elif parenthesis == "(":
        opening = "\("
        closing = "\)"

    references = re.findall(symbol + opening + ".*?" + closing, comp_obj)
    remove_repeats(references)
    for index in range(len(references)):
        references[index] = references[index][2:-1]
    return references

def OKJFQJLKEWFLEWQGmatch_references_old(comp_obj, symbol):
    if symbol == "$":
        symbol = "\$"
    references = os.popen("cat " +  path + " | grep -P -o '" + symbol + "{.*?}' | sed 's/" + symbol + "{//' | sed 's/}//'").read()
    references = references.split("\n")
    remove_repeats(references)
    del references[-1]
    return references

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
