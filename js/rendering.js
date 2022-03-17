const fs = require("fs");
const { copyComponent, listDirRecursive, readJson, writeComponent } = require("./file-io");
const { parseTag } = require("./functions");
const TagTree = require("./TagTree");

function expandCompTag(tag, GLOBAL) {

    tag = parseTag(tag, false);

    var output = copyComponent("./components/" + tag[0] + ".html");
    const tagTree = new TagTree(output);
    output = performSubstitutions(tagTree, tag[1], GLOBAL);

    return output;

}

function renderPages(GLOBAL) {
    renderPublicDirectory(GLOBAL);
    handleGigaspec(GLOBAL);
}

function handleGigaspec(GLOBAL) {
    gigaspec = readJson("config/gigaspec.json");

    for (let directory of Object.keys(gigaspec)) {
        produceFiles(directory, gigaspec[directory], GLOBAL);
    }
}

function produceFiles(directory, specs, GLOBAL) {

    fs.mkdirSync("BUILD/" + directory, { recursive: true });

    specs.forEach(spec => {
        // require
        var content = readJson(spec["source"]);
        Object.keys(content).forEach(key => {
            fillTemplate(spec["template"], directory, key, content[key], GLOBAL);
        });
    });

}


function fillTemplate(template, directory, key, content, GLOBAL) {
    var compObj = copyComponent(template);

    tagTree = new TagTree(compObj);

    compObj = performSubstitutions(tagTree, content["params"], GLOBAL);
    writeComponent(compObj, "BUILD/" + directory + "/" + key);
}

function renderPublicDirectory(GLOBAL) {
    const { pagesToRender, staticFiles, directories } = listDirRecursive("./public")

    // copy directories in public to BUILD
    for (let directory of directories) {
        directory = directory.slice(9);
        newDir = "BUILD/" + directory;

        if (!fs.existsSync(newDir)) {
            fs.mkdirSync(newDir);
        }
    }


    // copy static pages from public to BUILD
    for (let file of staticFiles) {
        fs.cpSync(file, "BUILD/" + file.slice(9));
    }

    // render html pages
    for (let path of pagesToRender) {

        var compObj = copyComponent(path);

        var tagTree = new TagTree(compObj);

        var result = performSubstitutions(tagTree, {}, GLOBAL);

        writeComponent(result, "BUILD/" + path.slice(9))
    }

}

function performSubstitutions(tagTree, params, GLOBAL) {

    var text = "";
    var index = 0;
    tagTree.tags.forEach(value => {
        if (value.constructor.name === "TagTree") {
            text = text + performSubstitutions(value, params, GLOBAL);
        }
        else {
            text = text + stringify(value);
        }
    });

    var output;

    if (tagTree.kind == "VAR") {
        output = params[text];
        output = stringify(output);
    }
    else if (tagTree.kind === "EVAL") {
        output = stringify(eval(text));
    }
    else if (tagTree.kind === "COMP") {
        output = stringify(expandCompTag(text, GLOBAL));
    }
    else if (tagTree.kind === "HASH") {
        output = stringify(GLOBAL["config_vars"][text]);
    }
    else if (tagTree.kind === "MASTER") {
        output = text;
    }
    else {
        throwError("compiler error", "TagTree.performSubstitutions");
    }

    return output;
}

function stringify(value) {
    if (value.constructor.name === "Array") {
        return arrayToString(value);
    }
    else {
        return value.toString();
    }
}

function arrayToString(array) {
    
    var output = "";

    array.forEach(item => {
        if (item.constructor.name === "Array") {
            output = output + arrayToString(item);
        }
        else {
            output = output + item.toString();
        }
        output = output + ",";
    });

    output = "[" + output.slice(0, output.length - 1) + "]";

    return output;

}

module.exports = { expandCompTag, renderPages };
