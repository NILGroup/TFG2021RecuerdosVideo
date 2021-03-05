import sys
from moviepy.editor import *

'''
video = VideoFileClip(sys.argv[1]) # 2.
audio = video.audio # 3.cls
audio.write_audiofile(sys.argv[2]) # 4.
'''



-------------------------------
BUSCAR COMO HACERLO CON PYDUB
-------------------------------



video = VideoFileClip('GH010191.mp4')
audio = video.audio
audio.write_audiofile('speech.wav')
print("max_volumne: " + str(audio.max_volume()) + "\nduration : " + str(audio.duration))

# max_volumne: 0.456756591796875

