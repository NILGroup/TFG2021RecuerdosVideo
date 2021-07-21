
from pydub import AudioSegment, effects, scipy_effects

chunk = AudioSegment.from_wav('parte1.wav')
print('--- Proceso Comprimir ---')

chunk_silent = AudioSegment.silent(700)
chunk = effects.compress_dynamic_range(chunk, threshold = -15.0, ratio = 5.0, attack = 1, release = 10.0)
chunk = scipy_effects.band_pass_filter(chunk, 200, 3100)
chunk = effects.normalize(chunk)
audio_chunk = chunk_silent + chunk + chunk_silent
chunk.export("parteComr.wav", bitrate = '320k', format = "wav")