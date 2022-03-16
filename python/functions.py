import re

def parse_tag(tag, remove_brackets = True):


    # extract name of components (remove the #{ })
    if remove_brackets:
        tag = tag[2:-1]

    output = [""]

    index = 0

    while index < len(tag) and tag[index] != " ":
        output[0] = output[0] + tag[index]
        index += 1

    d = {}
    state = "start-name"
    name = ""
    value = ""
    for char in tag[index:]:

        if state == "start-name":
            if char == " ":
                pass
            else:
                name = name + char
                state = "name"

        elif state == "name":
            if char == "=":
                state = "start-value"
            else:
                name = name + char

        elif state == "start-value":
            if char == " ":
                pass
            elif char in ["\"", "'"]:
                state = "string-value"
                value = value + char
            else:
                state = "value"
                value = value + char

        elif state == "string-value":
            value = value + char
            if char in ["\"", "'"]:
                state = "end-value"
                d[name] = eval(value)
                name = ""
                value = ""

        elif state == "value":
            if char == " ":
                state = "end-value"
                d[name] = eval(value)
                name = ""
                value = ""
            else:
                value = value + char

        elif state == "end-value":
            if char != " ":
                state = "name"
                name = name + char

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

def print_error_message(message):
    print("\033[1;31merror: " + message + "\033[0m")

def regex_cleanse(text):
    output = ""
    for char in text:
        if char in "+*":
            output = output + "\\" + char
        else:
            output = output + char
    return output
