
from pydub import AudioSegment, effects, scipy_effects


def normalizar(nombre):

    print('--- Proceso Normalizar ---')

    a1 = AudioSegment.from_wav( "./audios/" + nombre + ".wav")
    a1 = scipy_effects.band_pass_filter(a1, 200, 3100)
    a1 = a1.set_channels(1)
    a1 = effects.normalize(a1)
    fichero = "./audios/" + nombre + "_F+M+Norm" + ".wav"
    #a1.export(fichero, format = 'wav', bitrate = '320k')
    
    a1 = effects.compress_dynamic_range(a1, threshold = -12.0, ratio = 5.0, attack = 0.1, release = 10.0)
    a1 = scipy_effects.band_pass_filter(a1, 200, 3100)
    a1 = effects.normalize(a1)
    
    fichero = "./audios/" + nombre + "_F+M+Norm+Compr+Norm" + ".wav"
    a1.export(fichero, format = 'wav', bitrate = '320k')

    return fichero
