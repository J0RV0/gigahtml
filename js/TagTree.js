class TagTree {

    constructor(text, kind = "MASTER") {
        this.tags = [];
        this.kind = kind;
        this.OPENING_BRACKETS = "{(<";
        this.CLOSING_BRACKETS = "})>";
        this.process(text);
    }

    process(text) {
    
        var string = "";
        var inTag = false;
        var firstBracket = false;
        var kind = "";
        var hold = "";
        var bracketDepth = 0;
        var index = 0;

        for (let index = 0; index < text.length; index++) {

            var character = text[index];

            if (!inTag) {
                if ("$<#".includes(character)) {
                    hold = character;
                    if (string.length > 0) {
                        this.addTag(string);
                    }
                    string = "";
                    inTag = true;
                    firstBracket = true;
                    if ("$#".includes(character)) {
                        bracketDepth = 0;
                    }
                    else if (character === "<") {
                        bracketDepth = 1;
                    }
                }
                else {
                    string = string + character;
                }
            }

            else if (firstBracket) {
                if (this.OPENING_BRACKETS.includes(character)) {
                    bracketDepth++;
                    firstBracket = false;
                    if (character === "{") {
                        if (hold === "$") {
                            kind = "VAR";
                        }
                        else if (hold === "#") {
                            kind = "HASH";
                        }
                    }
                    else if (character === "(") {
                        kind = "EVAL";
                    }
                }
                else if (hold === "<") {
                    if (character === "%") {
                        kind = "COMP";
                        firstBracket = false;
                    }
                    else {
                        inTag = false;
                        string = string + "<" + character;
                    }
                }
                    
                else {
                    inTag = false;
                    firstBracket = false;
                    bracketDepth = 0;
                }
            }

            else {
                if (this.OPENING_BRACKETS.includes(character)) {
                    bracketDepth++;
                    string = string + character;
                }
                else if (this.CLOSING_BRACKETS.includes(character)) {
                    bracketDepth--;
                    if (bracketDepth === 0) {
                        inTag = false;
                        this.addTag(new TagTree(string, kind));
                        string = "";
                    }
                    else {
                        string = string + character;
                    }
                }
                else {
                    string = string + character;
                }
            }
        }

        if (string.length > 0) {
            this.addTag(string);
        }

    }

    addTag(tag) {
        if (typeof(tag) === "string" && this.tags.length > 0 && typeof(this.tags[this.tags.length-1]) === "string") {
            this.tags[this.tags.length - 1] = this.tags[this.tags.length - 1] + tag;
        }
        else {
            this.tags.push(tag);
        }
    }

    print(indent = 0) {
        const TAB = "  ";
        console.log(TAB.repeat(indent) + "|" + this.kind);
        var index = 0;
        for (let index = 0; index < this.tags.length; index++) {
            let item = this.tags[index];
            if (typeof(item) === "string") {
                console.log(TAB.repeat(indent) + "|" + item);
            }
            else {
                item.print(indent + 1);
            }
        }
    }

    performSubstitutions(params, GLOBAL) {

        var text = "";
        var index = 0;
        this.tags.forEach(value => {
            if (value.constructor.name === "TagTree") {
                text = text + value.performSubstitutions(params, GLOBAL);
            }
            else if (value.constructor.name === "Array") {
                text = text + "[" + value.toString() + "]";
            }
            else {
                text = text + value.toString();
            }
        });

        if (this.kind == "VAR") {
            output = str(params[text]);
        }
        else if (this.kind === "EVAL") {
            // TODO: error catch
            output = str(eval(text));
        }
        else if (this.kind === "COMP") {
            output = expandCompTag(text, GLOBAL);
        }
        else if (this.kind === "HASH") {
            output = str(GLOBAL["config_vars"][text]);
        }
        else if (this.kind === "MASTER") {
            output = text;
        }

        return output;
    }

}

const tagTree = new TagTree("<h1>Well who is it?<%profile name='Jack' age=21></h1>");

tagTree.print();
