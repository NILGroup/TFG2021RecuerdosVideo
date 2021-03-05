
from pydub import AudioSegment, effects, scipy_effects

speechNormalizado = AudioSegment.from_wav('speech.wav')

#audio = effects.normalize(audio)

#speechNormalizado = audio.band_pass_filter(300, 3000)

speechNormalizado = scipy_effects.band_pass_filter(speechNormalizado, 300, 2500, 5)

speechNormalizado = speechNormalizado + 10

speechNormalizado = speechNormalizado.set_channels(1)

speechNormalizado.export('speechEfectsScipy2500.wav', format='wav')