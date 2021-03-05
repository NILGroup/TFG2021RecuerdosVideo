import os
import subprocess
import speech_recognition as sr
import ffmpeg as f

# Se pasa de video a udio utilizando comandos del OS

video = f.input('GH010191.mp4')
audio = video.audio


'''
command2mp3 = "ffmpeg -i GH010191.mp4 speech.mp3"
command2wav = "ffmpeg -i speech.mp3 speech.wav"

os.system(command2mp3);
os.system(command2wav);
'''