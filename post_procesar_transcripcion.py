import sys
import json
import os
with open(sys.argv[1]) as jsonfile:
    array = json.load(jsonfile)
base = os.path.basename(sys.argv[1])
name = os.path.splitext(base)[0]
hablante = array[0]["speaker tag"]
salto = sys.argv[2]
texto=""
for elem in array:
    if hablante != elem["speaker tag"]:
        if(salto):
            texto += ".\n" + elem["word"]
        else:
            texto += "." + elem["word"]
        hablante=elem["speaker tag"]
    else:
        texto += " "+ elem["word"]

with open(os.path.dirname(sys.argv[1])+"/" + name + "_deserialized.txt", "w", encoding="ISO-8859-1") as output:
    output.write(texto)