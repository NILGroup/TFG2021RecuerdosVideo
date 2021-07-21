from moviepy.editor import *


def v2a(nombre, extension):
    
    print('--- Proceso video2audio ---')
    
    video = VideoFileClip(nombre + extension)
    audio = video.audio
    audio.write_audiofile(nombre + ".wav")
    return nombre + ".wav"
