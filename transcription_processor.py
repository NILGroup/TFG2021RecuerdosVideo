def deserialize_transcript(array, salto):
    hablante = array[0]["speaker tag"]
    texto = str(hablante) + ": "
    salto_char= ""
    if salto: salto_char=".\n"

    for elem in array:
        if hablante != elem["speaker tag"]:
            word = elem["word"]
            texto += salto_char + str(elem["speaker tag"]) + ": " + word[0].upper() + word[1:]
            hablante = elem["speaker tag"]
        else:
            texto += " " + elem["word"]
            
    return texto.lstrip()

def divide_by_speaker(text):
    array = text.splitlines()
    speaker1 = []
    speaker2 =[]
    for sentence in array:
      if sentence[0]=="1": speaker1.append(sentence[2:])
      else: speaker2.append(sentence[2:])
    text_spk1 = "\n".join((item for item in speaker1))
    text_spk2 = "\n".join((item for item in speaker2))
    return text_spk1, text_spk2

def split_by_sections(text, n):
    array = text.splitlines()
    text_result=[]
    for i in range(0, len(array), n):
        text_result.append("\n".join((item for item in array[i:i + n])))
    return text_result

#if __name__ == "__main__":
#    with open(sys.argv[1]) as jsonfile:
#        array = json.load(jsonfile)
#        texto = deserialize_transcript(array, sys.argv[2])
#        base = os.path.basename(sys.argv[1])
#        name = os.path.splitext(base)[0]
#        with open(os.path.dirname(sys.argv[1]) + "/" + name + "_deserialized.txt", "w",
#                  encoding = "ISO-8859-1") as output:
#            output.write(texto)
