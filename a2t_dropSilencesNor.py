# importing libraries
import os
import shutil
from datetime import datetime
from datetime import timedelta
import speech_recognition as sr
from pydub import AudioSegment, effects, scipy_effects
from pydub.silence import split_on_silence


formato = "%H:%M:%S"


def transcribe(fichero = "GH010191.wav"):
    
    print('--- Proceso Separar por Silencios ---')

    msl = 400
    st = -40
    ks = 300

    # Fichero donde se almacenará la transcripción
    filename = f"./filesTranscriptions/({st},{msl})transcrip_ComChunck_" + fichero.split(".")[0] + ".txt"
    fh = open(filename, "w+", encoding = "ISO-8859-1")

    audio = AudioSegment.from_wav("./audios/" + fichero)
    chunks, not_silence_ranges = split_on_silence(audio, min_silence_len = msl,
                                                  silence_thresh = st,
                                                  keep_silence = ks)

    # Directorio donde se almacena los audios troceados
    try:
        if os.path.exists('audio_troceado_ComChunck'):
            shutil.rmtree('audio_troceado_ComChunck')
        
        os.mkdir('audio_troceado_ComChunck')
        os.chdir('audio_troceado_ComChunck')
    
    except(FileExistsError):
        pass

    print('\33[32m' + datetime.now().strftime(formato) + '\033[0m')
    print('--- Proceso Transcribir ---')
    
    i = 1
    
    # Transcripcion de audios troceados
    for chunk in chunks:
    
        # Procesamiento de audios troceados
        chunk_silent = AudioSegment.silent(600)
        chunk = effects.compress_dynamic_range(chunk, threshold = -12.0, ratio = 5.0, attack = 1, release = 10.0)
        chunk = scipy_effects.band_pass_filter(chunk, 200, 3100)
        chunk = effects.normalize(chunk)
        audio_chunk = chunk_silent + chunk + chunk_silent
        audio_chunk.export("./parte{0}.wav".format(i), format = "wav")
        filename = 'parte' + str(i) + '.wav'

        r = sr.Recognizer()
        file = filename
        
        # recognize the chunk
        with sr.AudioFile(file) as source:
            audio_listened = r.record(source)
        
        try:
            rec = r.recognize_google(audio_listened, language = "es-ES")
            fh.write(rec[0].upper() + rec[1:] + ". " + '\n')
        except sr.UnknownValueError:
            print('\33[33m' + 'Could not understand audio' + '\033[0m')
        except sr.RequestError as e:
            print('\33[31m' + 'Could not request results. check your internet connection' + '\033[0m')
            
        i += 1
    
    fh.close()
    os.chdir('..')
