from moviepy.editor import *


def v2a(nombre):
    print('--- Proceso video2audio ---')
    video = VideoFileClip(nombre + ".mp4")
    audio = video.audio
    audio.write_audiofile(nombre + ".wav")
    return nombre + ".wav"
