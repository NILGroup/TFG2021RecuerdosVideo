
from pydub import AudioSegment, effects, scipy_effects


def normalizar(nombre):

    print('--- Proceso Normalizar ---')
    a1 = AudioSegment.from_wav(nombre + ".wav")
    a1 = scipy_effects.band_pass_filter(a1, 300, 2500)
    a1 = a1.set_channels(1)
    a1 = effects.normalize(a1)
    a1 += 2

    fichero = nombre + "Norm" + ".wav"
    a1.export(fichero, format = 'wav')
    return fichero
