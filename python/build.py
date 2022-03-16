from file_io import read_json
from rendering import render_pages

GLOBAL = {}
GLOBAL["config_vars"] = read_json("config/variables.json")

render_pages(GLOBAL)
