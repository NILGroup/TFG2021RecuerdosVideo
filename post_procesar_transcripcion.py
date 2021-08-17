import sys
import json
import os


def deserialize_transcript(array, salto):
    hablante = array[0]["speaker tag"]
    texto = ""
    
    for elem in array:
        if hablante != elem["speaker tag"]:
            word = elem["word"]
            if salto:
                texto += ".\n" + word[0].upper() + word[1:]
            else:
                texto += "." + word[0].upper() + word[1:]
            hablante = elem["speaker tag"]
        else:
            texto += " " + elem["word"]
            
    return texto.lstrip()



if __name__ == "__main__":
    with open(sys.argv[1]) as jsonfile:
        array = json.load(jsonfile)
        texto = deserialize_transcript(array, sys.argv[2])
        base = os.path.basename(sys.argv[1])
        name = os.path.splitext(base)[0]
        with open(os.path.dirname(sys.argv[1]) + "/" + name + "_deserialized.txt", "w",
                  encoding = "ISO-8859-1") as output:
            output.write(texto)
