const execSync = require("child_process").execSync;
const fs = require("fs");
const { GIGAHTML_DIR } = require("./constants");

const PROJECT_DIR = process.argv[2];
const scriptName = process.argv[3];

fs.writeFileSync(GIGAHTML_DIR + "/js/runtime-values.js", "module.exports.PROJECT_DIR = \"" + PROJECT_DIR + "\";");

const { readJson } = require("./file-io");

const json = readJson("gigahtml-package.json");

scripts = json["scripts"]

if (Object.keys(scripts).includes(scriptName)) {
    console.log(execSync(scripts[scriptName]).toString());
}
else {
    console.log("No such script " + scriptName);
}
