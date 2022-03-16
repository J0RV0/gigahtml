import re, sys
from constants import CLOSING_BRACKETS, DEV_MODE, OPENING_BRACKETS

def is_letter(char):
    return 65 <= ord(char) <= 90 or 97 <= ord(char) <= 122

def is_digit(char):
    return 48 <= ord(char) <= 57

def is_whitespace(char):
    return char in [" ", "\t"]

def is_string_delimiter(char):
    return char in ["\"", "'"]

def parse_tag(tag, remove_brackets = True):

    original_tag = tag

    # extract name of components (remove the #{ })
    if remove_brackets:
        tag = tag[2:-1]

    output = [""]

    index = 0

    while index < len(tag) and tag[index] != " ":
        output[0] = output[0] + tag[index]
        index += 1

    d = {}
    q = "start-name"
    name = ""
    value = ""
    bracket_depth = 0
    escape = False
    for char in tag[index:]:

        if q == "start-name":
            if is_letter(char):
                name = char
                q = "name"
            elif not is_whitespace(char):
                print("parse_tag 1")
                throw_error("invalid tag", original_tag)

        elif q == "name":
            if is_letter(char) or char == "-":
                name = name + char
            elif is_whitespace(char):
                q = "equals"
            elif char == "=":
                q = "start-value"
            else:
                print("parse_tag 2")
                throw_error("invalid tag", original_tag)

        elif q == "equals":
            if char == "=":
                q = "start-value"

        elif q == "start-value":
            if is_string_delimiter(char):
                q = "value-string"
                value = char
            elif is_digit(char):
                q = "value-number"
                value = char
            elif char in "{[":
                q = "value-object"
                value = char
                bracket_depth = 1
            elif not is_whitespace(char):
                print("parse_tag 3")
                throw_error("invalid tag", original_tag)

        elif q == "value-string":
            value = value + char
            if is_string_delimiter(char):
                d[name] = eval(value)
                name, value = "", ""
                q = "start-name"

        elif q == "value-number":
            if is_digit(char) or char == ".":
                value = value + char
            else:
                d[name] = eval(value)
                name, value = "", ""
                q = "start-name"

        elif q == "value-object":
            value = value + char
            if char in "}]":
                bracket_depth -= 1
                if bracket_depth == 0:
                    d[name] = eval(value)
                    name, value = "", ""
                    q = "start-name"
            elif char in "{[":
                 bracket_depth += 1

    if value != "":
        d[name] = eval(value)

    output.append(d)

    return output


def remove_match(match, array):
    for i in range(len(array)):
        if array[i] == match:
            del array[i]
            return

def remove_repeats(array):
    removed_count = 0
    values = []
    index = 0
    while index < len(array):
        if array[index] in values:
            del array[index]
        else:
            values.append(array[index])
            index += 1

def throw_error(error_type, message):
    print("\033[1;31merror: " + error_type + ": " + message + "\033[0m")
    sys.exit(1)

def regex_cleanse(text):
    output = ""
    for char in text:
        if char in "+*":
            output = output + "\\" + char
        else:
            output = output + char
    return output

def clean_html_text(text):
    text = re.sub("\n", "", text)
    if DEV_MODE:
        text = re.sub("  ", "", text)
        text = re.sub("><", ">\n<", text)
    return text
