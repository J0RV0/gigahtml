function isLetter(char) {
    const v = char.charCodeAt(0);
    return (65 <= v && v <= 90 || 97 <= v && v <= 122);
}

function isDigit(char) {
    const v = char.charCodeAt(0);
    return (48 <= v && v <= 57);
}

function isWhitespace(char) {
    return " \t".includes(char);
}

function isStringDelimiter(char) {
    return "\"'".includes(char);
}

function parseTag(tag, removeBrackets = true) {

    const originalTag = tag;
    
    if (removeBrackets) {
        tag = tag.slice(2, tag.length - 1);
    }

    const output = [""];

    var index = 0;

    while (index < tag.length && tag[index] !== " ") {
        output[0] = output[0] + tag[index];
        index++;
    }

    const d = {};
    var q = "start-name";
    var name = "";
    var value = "";
    var bracketDepth = 0;
    var character = "";

    while (index < tag.length) {

        character = tag[index++];

        if (q === "start-name") {
            if (isLetter(character)) {
                name = character;
                q = "name";
            }
            else if (!isWhitespace(character)) {
                throwError("invalid tag", originalTag);
            }
        }

        else if (q === "name") {
            if (isLetter(character) || character === "-") {
                name = name + character;
            }
            else if (isWhitespace(character)) {
                q = "equals";
            }
            else if (character === "=") {
                q = "start-value";
            }
            else {
                throwError("invalid tag", originalTag);
            }
        }

        else if (q === "equals") {
            if (character === "=") {
                q = "start-value";
            }
        }

        else if (q === "start-value") {
            if (isStringDelimiter(character)) {
                q = "value-string";
                value = character;
            }
            else if (isDigit(character)) {
                q = "value-number";
                value = character;
            }
            else if (["{","["].includes(character)) {
                q = "value-object";
                value = character;
                bracketDepth = 1;
            }
            else if (!isWhitespace(character)) {
                throwError("invalid tag", originalTag);
            }
        }

        else if (q === "value-string") {
            value = value + character
            if (isStringDelimiter(character)) {
                d[name] = eval(value)
                name = "";
                value = "";
                q = "start-name";
            }
        }

        else if (q === "value-number") {
            if (isDigit(character) || character === ".") {
                value = value + character;
            }
            else {
                d[name] = eval(value);
                name = "";
                value = "";
                q = "start-name";
            }
        }

        else if (q === "value-object") {
            value = value + character;
            if (["}", "]"].includes(character)) {
                bracketDepth--;
                if (bracketDepth === 0) {
                    d[name] = eval(value);
                    name = "";
                    value = "";
                    q = "start-name";
                }
            }
            else if (["{","["].includes(character)) {
                 bracketDepth++;
            }
        }

    }

    if (value !== "") {
        d[name] = eval(value);
    }

    output.push(d);

    return output;

}

function throwError(type, message) {
    console.log("error: " + type + ": " + message);
}

function removeRepeats(array) {
    var removed_count = 0;
    const values = [];
    var index = 0;
    while (index < array.length) {
        if (values.includes(array[index])) {
            array.splice(index, 1);
        }
        else {
            values.push(array[index]);
            index++;
        }
    }
}

module.exports = { parseTag, removeRepeats, throwError };
