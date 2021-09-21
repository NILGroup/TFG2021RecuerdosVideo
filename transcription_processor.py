def deserialize_transcript(array):
    hablante = array[0]["speaker tag"]
    texto = str(hablante) + ": "
    salto_char = ".\n"
    
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
    speaker2 = []
    for sentence in array:
        if sentence[0] == "1":
            speaker1.append(sentence[2:])
        else:
            speaker2.append(sentence[2:])
    text_spk1 = "\n".join((item for item in speaker1))
    text_spk2 = "\n".join((item for item in speaker2))
    return text_spk1, text_spk2


def split_by_sections(text, n):
    array = text.splitlines()
    text_result = []
    for i in range(0, len(array), n):
        text_result.append("\n".join((item for item in array[i:i + n])))
    return text_result
