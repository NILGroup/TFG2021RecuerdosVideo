from moviepy.editor import *
import tempfile
import shutil
from pathlib import Path

def v2a(source_file, output_path):
    print("--- Proceso video2audio ---")
    video = VideoFileClip(str(source_file))
    audio = video.audio
    newpath = Path(output_path) / source_file.stem
    audio.write_audiofile(str(newpath.with_suffix(".wav")))
    video.close()
    return newpath.with_suffix(".wav")