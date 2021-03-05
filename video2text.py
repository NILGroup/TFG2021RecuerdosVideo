import speech_recognition as sr
import moviepy.editor as mp

clip = mp.VideoFileClip(r"GH010191.mp4")

clip.audio.write_audiofile(r"speech.wav")

print("START")


audio = sr.AudioFile("speech.wav")
recog = sr.Recognizer()


with audio as source:
  recog.adjust_for_ambient_noise(source)
  audio_file = recog.record(source, duration=100, language="es-es")


result = recog.recognize_google(audio_file)

print(result)

# exporting the result
'''
with open('recognized.txt',mode ='w') as file:
  file.write("Recognized Speech:")
  file.write("\n")
  file.write(result)
  print("ready!")
'''


