import json, os, sys

json = json.loads(open("gigahtml-package.json", "r").read())

script_name = sys.argv[1]

scripts = json["scripts"]

if script_name in scripts.keys():
    os.system(scripts[script_name])
else:
    print("No such script " + script_name)

