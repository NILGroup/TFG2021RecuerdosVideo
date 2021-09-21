from moviepy.editor import *
from pathlib import Path


def v2a(source_file, output_path):
    video = VideoFileClip(str(source_file))
    audio = video.audio
    newpath = Path(output_path) / source_file.stem
    audio.write_audiofile(str(newpath.with_suffix(".wav")), logger=None)
    video.close()
    return newpath.with_suffix(".wav")