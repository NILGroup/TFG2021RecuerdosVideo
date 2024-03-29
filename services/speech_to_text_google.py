# -*- coding: utf-8 -*-

import os

from google.cloud import speech_v1p1beta1

from resources import api_key

from constants.messages import messages
import logging
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_key


def transcribe(storage_uri):
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
    logging.info(messages.INFO_GOOGLE_TRANSCRIBE_SPEAKER.value)
    operation = client.long_running_recognize(config = config, audio = audio)
    response = operation.result()
    
    result = response.results[-1]
    words_info = result.alternatives[0].words
    
    # Printing out the output:
    json_array = []
    
    for word_info in words_info:
        data = {}
        data["word"] = word_info.word
        data["speaker tag"] = word_info.speaker_tag
        json_array.append(data)
    return json_array
