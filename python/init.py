import os

name = input("Project name: ")
exists = os.path.exists(name)
while exists or len(name) == 0 or name == "." or len(name) >= 2 and name[:2] == ".." or "/" in name:
    if exists:
        print(name + " already exists")
    else:
        print("Invalid name for project")
    name = input("Project name: ")
    exists = os.path.exists(name)

author = input("Author: ")
description = input("Description:\n")
url = input("URL: ")

os.system("mkdir " + name)

# make package-file
file = open(name + "/gigahtml-package.json", "w")
file.write('{\n')
file.write('    "name": "' + name + '",\n')
file.write('    "author": "' + author + '",\n')
file.write('    "description": "' + description + '",\n')
file.write('    "url": "' + url + '",\n')
file.write('    "version": "1.0.0",\n')
file.write('    "scripts": {\n')
file.write('        "build": "gigahtmlc build",\n')
file.write('        "delete-build": "gigahtmlc delete-build"\n')
file.write('    }\n')
file.write('}\n')
file.close()

# make files
os.system("mkdir -p " + name + "/public " + name + "/components " + name + "/config " + name + "/templates " + name + "/BUILD " + name + "/.BUILD")
os.system("mkdir " + name + "/.BUILD/components")
os.system("mkdir " + name + "/public/css " + name + "/public/js " + name + "/public/res")
os.system("cp ${GIGAHTML}/res/index.html " + name + "/public")
os.system("cp ${GIGAHTML}/res/welcome.html " + name + "/components")
os.system("cp ${GIGAHTML}/res/main.css " + name + "/public/css")
os.system("cp ${GIGAHTML}/res/gigaspec.json " + name + "/config")

# make vars file
file = open(name + "/config/variables.json", "w")
file.write('{\n')
file.write('    "DOMAIN": "' + os.path.join(os.path.abspath("."), name, "BUILD") + '",\n')
file.write('    "DOCS_URL": "https://gigahtml.org/docs",\n')
file.write('    "AUTHOR": "' + author + '"\n')
file.write('}\n')
file.close()

print("\nNew project created")
