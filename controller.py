# importing libraries
import os
from pathlib import Path

import model
import normalizar_audio
import services.cloud_storage as cloud_storage
import services.speech_to_text as speech_to_text
import services.speech_to_text_dropSilences as s2t_dropSilence
from messages import messages
from post_procesar_transcripcion import deserialize_transcript


formato = "%H:%M:%S"


def process_audio(file, transcriptMode, divide_by_speaker_option, divide_by_segments_option, size_segments):
    
    source_file = file
    result = {}
    diarize=False
    if(transcriptMode=="hablantes"):
        diarize=True
    
    if os.path.exists(source_file):
        base = os.path.basename(source_file)
        name = os.path.splitext(base)[0]
        output_name = name + "_output.json"
        
        try:
            # Proceso Normalizar
            normalizar_audio.normalizar(source_file)
            # Proceso de Trancribir segun el modo de transcripcion
            if diarize:
                storage_uri = cloud_storage.upload_blob(source_file, base)
                result_json_array = speech_to_text.transcribe(storage_uri, Path(__file__).parent / "output" /output_name)
                transcript = deserialize_transcript(result_json_array, True)
            else:
                transcript = s2t_dropSilence.transcribe(source_file)

            # Generar resumen
            summary = model.summarize(transcript.replace("\n", ""), diarize, divide_by_speaker_option, divide_by_segments_option, size_segments)
            result = {"summary": summary, "transcript": transcript}
            
        except Exception as e:
            print(messages.ERR_UNEXPECTED.value)
            print(e)
        finally:
            if diarize:
                cloud_storage.delete_blob(base)

    else:
        print(messages.ERR_FILE.value)

    return result
