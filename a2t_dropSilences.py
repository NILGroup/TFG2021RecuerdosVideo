# importing libraries
import speech_recognition as sr
import os
import shutil

from pydub import AudioSegment
from pydub.silence import split_on_silence


# a function that splits the audio file into chunks
# and applies speech recognition
def silence_based_conversion(path="speech.wav"):
    # open the audio file stored in
    # the local system as a wav file.

    audio = AudioSegment.from_wav("wavs_prueba/spPrue2.wav")

    # open a file where we will concatenate
    # and store the recognized text
    fh = open("recognized_SphinxTroceado.txt", "w+")

    # split track where silence is 0.5 seconds
    # or more and get chunks
    chunks = split_on_silence(audio, min_silence_len=1000, silence_thresh=-40, keep_silence=1000)

    # create a directory to store the audio chunks.
    try:
        os.mkdir('audio_troceado_sp')
    except(FileExistsError):
        pass

    # move into the directory to
    # store the audio files.
    os.chdir('audio_troceado_sp')

    i = 1
    # process each chunk
    for chunk in chunks:

        # Create 0.5 seconds silence chunk
        chunk_silent = AudioSegment.silent(500)

        audio_chunk = chunk_silent + chunk + chunk_silent

        # export audio chunk and save it in
        # the current directory.
        print("saving parte{0}.wav".format(i))
        # specify the bitrate to be 192 k
        audio_chunk.export("./parte{0}.wav".format(i), bitrate='192k', format="wav")

        # the name of the newly created chunk
        filename = 'parte' + str(i) + '.wav'

        print("Processing parte " + str(i))

        # get the name of the newly created chunk
        # in the AUDIO_FILE variable for later use.
        file = filename

        # create a speech recognition object
        r = sr.Recognizer()

        # recognize the chunk
        with sr.AudioFile(file) as source:
            # remove this if it is not working
            # correctly.
            r.adjust_for_ambient_noise(source)
            audio_listened = r.record(source)

        try:
            # try converting it to text
            rec = r.recognize_sphinx(audio_listened, language="es")
            # write the output to the file.
            fh.write(rec + ". ")

        # catch any errors.
        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError as e:
            print("Could not request results. check your internet connection")

        i += 1

    os.chdir('..')


if __name__ == '__main__':
    print('START')

    if os.path.exists('audio_troceado'):
        shutil.rmtree('audio_troceado')

    silence_based_conversion()