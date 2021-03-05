
from pydub import AudioSegment, effects, scipy_effects

speechNormalizado = AudioSegment.from_wav('speech.wav')

#speechNormalizado = audio.band_pass_filter(300, 3000)
filtrado = scipy_effects.band_pass_filter(speechNormalizado, 400, 4000, 5)
speechNormalizado = filtrado.set_channels(1)

speechNormalizado = effects.normalize(speechNormalizado)
#speechNormalizado = speechNormalizado + 5

speechNormalizado.export('spPrue2.wav', format='wav')

