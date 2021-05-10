# importing libraries
import os
import shutil
from datetime import datetime

import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

formato = "%H:%M:%S"


def transcribe(fichero = "GH010191.wav"):

    print('--- Proceso Separar por Silencios ---')

    # fichero donde se almacenará la transcripción
    filename = "./filesTranscriptions/transcrip_" + fichero.split(".")[0] + ".txt"
    fh = open(filename, "w+", encoding="ISO-8859-1")

    audio = AudioSegment.from_wav(fichero)
    chunks, not_silence_ranges = split_on_silence(audio, min_silence_len = 1000, silence_thresh = -40, keep_silence = 200)

    # Directorio donde se almacena los audios troceados
    try:
        if os.path.exists('audio_troceado'):
            shutil.rmtree('audio_troceado')
        
        os.mkdir('audio_troceado')
        os.chdir('audio_troceado')
        
    except(FileExistsError):
        pass

    print('\33[32m' + datetime.now().strftime(formato) + ' START MAIN' + '\033[0m')
    print('--- Proceso Transcribir ---')

    i = 1
    tiempo = 0

    for chunk in chunks:

        chunk_silent = AudioSegment.silent(600)
        audio_chunk = chunk_silent + chunk + chunk_silent
        # print("Guardando parte{0}.wav".format(i))
        audio_chunk.export("./parte{0}.wav".format(i), bitrate = '192k', format = "wav")
        filename = 'parte' + str(i) + '.wav'
        # print("Procesando parte " + str(i) + ".  Duracion = {:.2f}".format(chunk.duration_seconds) + " segundos. Inicio: {:.2f}".format(tiempo) + " Final: {:.2f}".format(tiempo + chunk.duration_seconds))

        print("Procesando parte " + str(i) + ".  Duracion = {:.2f}".format(chunk.duration_seconds) +
              " segundos. Inicio: {:.2f}".format(not_silence_ranges[i - 1][0] / 1000) +
              " Final: {:.2f}".format(not_silence_ranges[i - 1][1] / 1000))

        r = sr.Recognizer()
        file = filename

        # recognize the chunk
        with sr.AudioFile(file) as source:
            # r.adjust_for_ambient_noise(source)
            audio_listened = r.record(source)

        try:
            rec = r.recognize_google(audio_listened, language = "es")
            fh.write("Parte " + str(i))
            fh.write(" ({:.2f}) ".format(not_silence_ranges[i - 1][0] / 1000))
            fh.write(rec + ". " + '\n')
        except sr.UnknownValueError:
            print('\33[33m' + 'Could not understand audio' + '\033[0m')
        except sr.RequestError as e:
            print('\33[31m' + 'Could not request results. check your internet connection' + '\033[0m')

        tiempo += chunk.duration_seconds
        i += 1

    fh.write(str(i) + " Partes" + '\n')

    fh.close()
    os.chdir('..')
