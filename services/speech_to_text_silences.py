# importing libraries
import shutil
from constants.messages import messages
import logging
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence


def transcribe(source_file, save_dir):

    logging.info(messages.INFO_STAGE_SPLIT_SILENCES.value)
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
        
        logging.info(messages.INFO_STAGE_TRANSCRIBE_SILENCES.value)
        
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
                logging.info(messages.AUDIO_NOT_UNDERSTAND.value + str(i))
            except sr.RequestError as e:
                logging.info(messages.ERR_BAD_INTERNET.value)

            i += 1
            
    except FileExistsError:
        logging.error(messages.ERR_NO_DIR.value)
    finally:
        shutil.rmtree(save_dir)
    
    return transcripcion
