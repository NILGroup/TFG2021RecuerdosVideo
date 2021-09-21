from pydub import AudioSegment, effects, scipy_effects
import logging
from constants.messages import messages

##---SOlO USADO AL TESTEAR----##
## normalización donde la conversación tiene muicha diferencia de volumen ##
## NO USADO DEBIDO A AUMENTO DE TIEMPO De EJECUCIÓN MUY ALTO##
def normalizar_compresion(source_file):
    sound = AudioSegment.from_wav(source_file)
    sound = scipy_effects.band_pass_filter(sound, 200, 3100)
    sound = sound.set_channels(1)
    sound = effects.normalize(sound)
    sound = effects.compress_dynamic_range(sound, threshold = -12.0, ratio = 5.0, attack = 0.1, release = 10.0)
    sound = scipy_effects.band_pass_filter(sound, 200, 3100)
    sound = effects.normalize(sound)
    sound.export(source_file, format = 'wav')


def normalizar(source_file):
    logging.info(messages.INFO_STAGE_NORMALIZAR.value)
    sound = AudioSegment.from_wav(source_file)
    sound = scipy_effects.band_pass_filter(sound, 200, 3100)
    sound = sound.set_channels(1)
    sound = effects.normalize(sound)
    sound.export(source_file, format = 'wav')
