from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import os
import io
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../api-key/potent-terminal-310416-10055defdf69.json"

#NO SE USA???

def speech_to_text(config, audio):
    client = speech.SpeechClient()
    response = client.recognize(config=config, audio=audio)
    print_sentences(response)


def print_sentences(response):
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        print("-" * 80)
        print("Transcript: {transcript}")
        print("Confidence: {confidence:.0%}")


config = types.RecognitionConfig(language_code="es-US")
file_name = os.path.join(os.path.dirname(__file__),"converted.wav")

#Loads the audio file into memory
with io.open(file_name, "rb") as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
speech_to_text(config, audio)