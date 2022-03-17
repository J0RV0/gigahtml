function expandCompTag(tag, GLOBAL) {

    tag = parseTag(tag, false);

    var output = copyComponent("./components/" + tag[0] + ".html");
    const tagTree = TagTree(output);
    output = tagTree.performSubstitutions(tag[1], GLOBAL);

    return output;

}

function renderPages(GLOBAL) {

    renderPublicDirectory(GLOBAL);

    handleGigaspec(GLOBAL);

}

function produceFiles(directory, specs, GLOBAL) {

    // TODO
    os.system("mkdir -p " + os.path.join("BUILD", directory))

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

    tagTree = TagTree(compObj);

    compObj = tagTree.performSubstitutions(content["params"], GLOBAL);
    writeComponent(compObj, os.path.join("BUILD", directory, key));
}

function renderPublicDirectory(GLOBAL) {
    pagesToRender, staticPages, directories = listdirRecursive("./public")

    // copy directories in public to BUILD
    for (let directory of directories) {
        directory = directory.slice(9);
        newDir = os.path.join("BUILD", directory);
        // TODO
        if (!os.path.exists(newDir)) {
            os.mkdir(newDir);
        }
    }

    // copy static pages from public to BUILD
    for (let file of staticPages) {
        var command = "cp " + file + " BUILD/" + file.slice(9);
        os.system(command);
    }

    // render html pages
    for (let path of pagesToRender) {

        var compObj = copyComponent(path)

        var tagTree = TagTree(compObj)

        var result = tagTree.performSubstitutions({}, GLOBAL)

        writeComponent(result, "BUILD/" + path.slice(9))
    }

}
