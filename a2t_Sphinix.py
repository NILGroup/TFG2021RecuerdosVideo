import speech_recognition as sr


print("START")

recog = sr.Recognizer()

with sr.AudioFile('wavs_prueba/spPrue2.wav') as audio_file:
    recog.adjust_for_ambient_noise(audio_file)
    audio_content = recog.record(audio_file)


try:
    result = recog.recognize_sphinx(audio_content, language="es")
    print(result)

except sr.UnknownValueError:
    print("could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))


#with open('transcripciones/recognize_Sphinx.txt',mode ='w') as file:
with open('Sphinx_2.txt',mode ='w') as file:
  file.write(result)
  print("ready!")


