# importing libraries
import shutil

import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence


formato = "%H:%M:%S"


def transcribe(source_file, save_dir):
    
    print('--- Proceso Separar por Silencios ---')

    transcripcion = ""
    msl = 250
    st = -40
    ks = 200
    
    audio = AudioSegment.from_wav(source_file)
    chunks = split_on_silence(audio, min_silence_len = msl,
                              silence_thresh = st,
                              keep_silence = ks)
    
    try:
        
        # Directorio donde se almacena los audios troceados
        if not save_dir.exists():
            save_dir.mkdir(exist_ok = True, parents = True)
        
        print('--- Proceso Transcribir por Silencios ---')
        
        i = 1
    
        # Transcripcion de audios troceados
        for chunk in chunks:
            
            chunk_silent = AudioSegment.silent(600)
            audio_chunk = chunk_silent + chunk + chunk_silent
            audio_chunk.export(f"{save_dir}/parte{i}.wav", format = "wav")
            filename = f"{save_dir}/parte{i}.wav"
            
            r = sr.Recognizer()
            file = filename
            
            # recognize the chunk
            with sr.AudioFile(file) as source:
                audio_listened = r.record(source)
            
            try:
                rec = r.recognize_google(audio_listened, language = "es-ES")
                transcripcion += rec[0].upper() + rec[1:] + ". "
            except sr.UnknownValueError:
                print('\33[33m' + 'No se pudo entender el audio ' + str(i) + '\033[0m')
            except sr.RequestError as e:
                print('\33[31m' + 'Request Error. Comprueba la conexión a internet' + '\033[0m')
            
            i += 1
            
    except FileExistsError:
        print("No existe el directorio")
    finally:
        shutil.rmtree(save_dir)
    
    return transcripcion
