# -*- coding: utf-8 -*-
from datetime import datetime

from google.cloud import speech_v1p1beta1
from resources import api_key
import json
import os
from pydub import AudioSegment, effects, scipy_effects


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_key


def transcribe(storage_uri, destination):
    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition
Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """
    client = speech_v1p1beta1.SpeechClient()
    language_code = "es-ES"
    config = {
            "language_code": language_code,
            "enable_speaker_diarization": True,
            "diarization_speaker_count": 2
    }
    audio = { "uri": storage_uri }
    operation = client.long_running_recognize(config = config, audio = audio)
    print(u"--- Proceso Transcribir por Hablantes ---")
    
    response = operation.result()
    
    result = response.results[-1]
    words_info = result.alternatives[0].words
    
    # Printing out the output:
    json_array = []
    
    for word_info in words_info:
        data = { }
        # start_time, end_time, confidence
        data["word"] = word_info.word
        data["speaker tag"] = word_info.speaker_tag
        # data["start_time"] = word_info.start_time
        # data["end_time"] = word_info.end_time
        json_array.append(data)
    
    with open(destination, 'w', encoding = "ISO-8859-1") as output:
        json.dump(json_array, output, ensure_ascii = False)
    return json_array
