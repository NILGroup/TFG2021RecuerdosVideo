import speech_recognition as sr

print("START")

recog = sr.Recognizer()

with sr.AudioFile('speechEfectsScipy2500.wav') as audio_file:
    recog.adjust_for_ambient_noise(audio_file)
    audio_content = recog.record(audio_file, duration=200)

try:
    result = recog.recognize_google(audio_content, language="es-es")
    print(result)

except sr.UnknownValueError:
    print("could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))

with open('transcripciones/recognize_Google200.txt', mode ='w') as file:
  file.write(result)
  print("ready!")


