const fs = require("fs");
const path = require("path");
const { PROJECT_DIR } = require("./runtime-values");

function copyComponent(filePath) {
    return fs.readFileSync(filePath).toString();
}

function listDirRecursive(directory) {
    const pagesToRender = [];
    const staticFiles = [];
    const directories = [];
    const dirs = [directory];
    while (dirs.length > 0) {
        var current = dirs[0];
        for (item of fs.readdirSync(current)) {
            item = current + "/" + item;
            if (fs.statSync(item).isDirectory()) {
                dirs.push(item);
                directories.push(item);
            }
            else if (path.extname(item) == ".html") {
                pagesToRender.push(item);
            }
            else {
                staticFiles.push(item);
            }
        }
        dirs.splice(0, 1);
    }
    return { pagesToRender, staticFiles, directories };
}

function writeComponent(compObj, filePath) {
    fs.writeFileSync(PROJECT_DIR + "/" + filePath, compObj);
}

function readJson(filePath) {
    return require(PROJECT_DIR + "/" + filePath);
}

module.exports = { copyComponent, listDirRecursive, readJson, writeComponent };
