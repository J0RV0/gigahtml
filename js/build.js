const { readJson } = require("./file-io");
const { renderPages } = require("./rendering");

const GLOBAL = {}
GLOBAL["config_vars"] = readJson("config/variables.json")

renderPages(GLOBAL)
