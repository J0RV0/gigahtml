import os, re, sys
from constants import *
from file_io import copy_component, listdir_recursive, match_component_tags, match_references, read_json, write_component
from functions import *

def has_been_rendered(component_tag):
    return os.path.exists("./.BUILD/components/" + component_tag[0] + ".html")

def references_rendered(component_tags):
    for tag in component_tags:
        if not has_been_rendered(tag):
            return False
    return True

def expand_comp_tag(tag, GLOBAL):

    tag = parse_tag(tag, False)

    output = copy_component("./components/" + tag[0] + ".html")

    tag_tree = TagTree(output)

    output = tag_tree.perform_substitutions(tag[1], GLOBAL)

    output = re.sub("\n", "", output)

    return output

def render_component_old(comp_obj, root_tag, GLOBAL):

    config_var_references = match_references(comp_obj, "#")

    if root_tag != None:
        comp_obj = substitute_param_tags(comp_obj, root_tag, GLOBAL)

    comp_obj = substitute_hash_references(comp_obj, config_var_references, GLOBAL)

    eval_tags = match_references(comp_obj, "$", "(")

    comp_obj = substitute_eval_tags(comp_obj, eval_tags, GLOBAL)

    component_tags = match_component_tags(comp_obj)

    if len(component_tags) > 0:
        comp_obj = substitute_component_references(comp_obj, component_tags, GLOBAL)

    return comp_obj

def substitute_component_references(comp_obj, component_tags, GLOBAL):
    for tag in component_tags:
        sub = copy_component("./components/" + tag[0] + ".html")

        sub = render_component(sub, tag, GLOBAL)
        # DANGER (.*?) We should be looking for the exact tag (so that includes looking at params)
        comp_obj = re.sub("<%" + tag[0] + ".*?" + ">", sub, comp_obj, 1)
        comp_obj = re.sub("\n\n", "\n", comp_obj)
    return comp_obj

def substitute_eval_tags(comp_obj, eval_tags, GLOBAL):
    for tag in eval_tags:
        try:
            substitution = eval(tag)
        except:
            print_error_message("cannot evaluate $(" + str(tag) + ")")
            sys.exit(1)
        comp_obj = re.sub("\$\(" + regex_cleanse(tag) + "\)", str(substitution), comp_obj)
        comp_obj = re.sub("\n\n", "\n", comp_obj)
    return comp_obj

def substitute_param_tags(comp_obj, root_tag, GLOBAL):
    params = root_tag[1]
    for param in params:
        substitution = params[param]
        comp_obj = re.sub("\${" + regex_cleanse(param) + "}", str(substitution), comp_obj)
        comp_obj = re.sub("\n\n", "\n", comp_obj)
    return comp_obj

def substitute_hash_references(comp_obj, references, GLOBAL):
    for reference in references:
        substitution = GLOBAL["config_vars"][reference]
        comp_obj = re.sub("#{" + reference + "}", substitution, comp_obj)
        comp_obj = re.sub("\n\n", "\n", comp_obj)
    return comp_obj

def render_pages(GLOBAL):

    render_public_directory(GLOBAL)

    handle_gigaspec(GLOBAL)


def handle_gigaspec(GLOBAL):

    gigaspec = read_json("config/gigaspec.json")

    for directory in gigaspec.keys():
        produce_files(directory, gigaspec[directory], GLOBAL)

    
def produce_files(directory, specs, GLOBAL):
    os.system("mkdir -p " + os.path.join("BUILD", directory))

    for spec in specs:
        content = read_json(spec["source"])
        for key in content.keys():
            fill_template(spec["template"], directory, key, content[key], GLOBAL)

def fill_template(template, directory, key, content, GLOBAL):
    comp_obj = copy_component(template)

    #comp_obj = render_component(comp_obj, ["TEMPLATE", content["params"]], GLOBAL)

    tag_tree = TagTree(comp_obj)

    comp_obj = tag_tree.perform_substitutions(content["params"], GLOBAL)
    write_component(comp_obj, os.path.join("BUILD", directory, key))

def render_public_directory(GLOBAL):
    pages_to_render, static_pages, directories = listdir_recursive("./public")

    # copy directories in public to BUILD
    for directory in directories:
        directory = directory[9:]
        new_dir = os.path.join("BUILD", directory)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

    # copy static pages from public to BUILD
    for file in static_pages:
        command = "cp " + file + " BUILD/" + file[9:]
        os.system(command)

    # render html pages
    for path in pages_to_render:

        comp_obj = copy_component(path)

        tag_tree = TagTree(comp_obj)

        result = tag_tree.perform_substitutions({}, GLOBAL)

        write_component(result, "BUILD/" + path[9:])


class TagTree:
    
    def __init__(self, text, kind = "MASTER"):
        self.tags = []
        self.opening_brackets = "{(<"
        self.closing_brackets = "})>"
        self.kind = kind
        self.process(text)

    def process(self, text):

        string = ""
        in_tag = False
        first_bracket = False
        kind = ""
        hold = ""
        bracket_depth = 0

        for char in text:

            if not in_tag:
                if char in "$<#":
                    hold = char
                    if len(string) > 0:
                        self.add_tag(string)
                    string = ""
                    in_tag, first_bracket = True, True
                    if char in "$#":
                        bracket_depth = 0
                    elif char == "<":
                        bracket_depth = 1
                else:
                    string = string + char

            elif first_bracket:
                if char in self.opening_brackets:
                    bracket_depth += 1
                    first_bracket = False
                    if char == "{":
                        if hold == "$":
                            kind = "VAR"
                        elif hold == "#":
                            kind = "HASH"
                    elif char == "(":
                        kind = "EVAL"
                elif hold == "<":
                    if char == "%":
                        kind = "COMP"
                        first_bracket = False
                    else:
                        in_tag = False
                        string = string + "<" + char
                    
                else:
                    in_tag, first_bracket, bracket_depth = False, False, 0

            else:
                if char in self.opening_brackets:
                    bracket_depth += 1
                    string = string + char
                elif char in self.closing_brackets:
                    bracket_depth -= 1
                    if bracket_depth == 0:
                        in_tag = False
                        self.add_tag(TagTree(string, kind))
                        string = ""
                    else:
                        string = string + char
                else:
                    string = string + char

        if len(string) > 0:
            self.add_tag(string)

    def add_tag(self, tag):
        if type(tag) == TagTree or len(self.tags) == 0 or len(self.tags) > 0 and type(self.tags[-1]) == TagTree:
            self.tags.append(tag)
        else:
            self.tags[-1] = self.tags[-1] + tag

    def __str__(self):
        return str(self.tags)

    def print(self, indent = 0):
        print("  " * indent + "|" + self.kind)
        for item in self.tags:
            if type(item) == TagTree:
                item.print(indent + 1)
            else:
                print("  " * indent + "|" + item)

    def perform_substitutions(self, params, GLOBAL):

        text = ""
        for value in self.tags:
            if type(value) == TagTree:
                text = text + value.perform_substitutions(params, GLOBAL)
            else:
                text = text + str(value)

        if self.kind == "VAR":
            output = str(params[text])
        elif self.kind == "EVAL":
            output = str(eval(text))
        elif self.kind == "COMP":
            output = expand_comp_tag(text, GLOBAL)
        elif self.kind == "HASH":
            output = str(GLOBAL["config_vars"][text])
        elif self.kind == "MASTER":
            output = text

        return output
