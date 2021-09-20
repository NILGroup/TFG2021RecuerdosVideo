# importing libraries
import os
from pathlib import Path

import model
import normalizar_audio
import services.cloud_storage as cloud_storage
import services.speech_to_text as speech_to_text
import services.speech_to_text_dropSilences as s2t_dropSilence
import services.send_email as sm
from messages import messages
from post_procesar_transcripcion import deserialize_transcript
from app import chunks_audio_path, output_email_path

formato = "%H:%M:%S"


def process_audio(audio_path, transcriptMode, divide_by_speaker_option, divide_by_segments_option, size_segments, email):

    result = {}
    diarize = False
    
    if transcriptMode == "hablantes":
        diarize = True
    
    if os.path.exists(audio_path):
        base = os.path.basename(audio_path)
        name = os.path.splitext(base)[0]
        
        try:
            # Proceso Normalizar
            normalizar_audio.normalizar(audio_path)
            # Proceso de Trancribir segun el modo de transcripcion
            if diarize:
                storage_uri = cloud_storage.upload_blob(audio_path, base)
                result_json_array = speech_to_text.transcribe(storage_uri)
                transcript = deserialize_transcript(result_json_array, True)
            else:
                transcript = s2t_dropSilence.transcribe(audio_path, chunks_audio_path / name)
            
            # Generar resumen
            summary = model.summarize(transcript.replace("\n", ""), diarize, divide_by_speaker_option, divide_by_segments_option, size_segments)
            result = {"summary": summary, "transcript": transcript}
            
            # Enviar correo con resultados
            if email:
                sm.send_email(email, transcript.replace(". ", ".\n"), summary, output_email_path / name)
        
        except Exception as e:
            print(messages.ERR_UNEXPECTED.value)
            print(e)
        finally:
            if diarize:
                cloud_storage.delete_blob(base)
                
    else:
        print(messages.ERR_FILE.value)
    
    return result
