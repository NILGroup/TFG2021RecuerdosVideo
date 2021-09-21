# importing libraries
import os
import logging
import model
import audio_processor
import services.cloud_storage as cloud_storage
import services.speech_to_text_google as speech_to_text
import services.speech_to_text_silences as speech_to_text_silence
import services.email_sender as sm
from constants.messages import messages
from transcription_processor import deserialize_transcript
from constants.paths import output_email_path, chunks_audio_path


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
            audio_processor.normalizar(audio_path)
            # Proceso de Trancribir segun el modo de transcripcion
            if diarize:
                storage_uri = cloud_storage.upload_blob(audio_path, base)
                result_json_array = speech_to_text.transcribe(storage_uri)
                transcript = deserialize_transcript(result_json_array)
            else:
                transcript = speech_to_text_silence.transcribe(audio_path, chunks_audio_path / name)
            
            # Generar resumen
            summary = model.summarize(transcript.replace("\n", ""), diarize, divide_by_speaker_option, divide_by_segments_option, size_segments)
            result = {"summary": summary, "transcript": transcript}
            
            # Enviar correo con resultados
            if email:
                sm.send_email(email, transcript.replace(". ", ".\n"), summary, output_email_path / name)
        
        except Exception as e:
            logging.error(messages.ERR_UNEXPECTED.value)
        finally:
            if diarize:
                cloud_storage.delete_blob(base)
                
    else:
        logging.error(messages.ERR_FILE.value)
    
    return result
