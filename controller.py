# importing libraries
import os
from messages import messages
from pathlib import Path
from datetime import datetime
import services.cloud_storage as cloud_storage
import services.speech_to_text as speech_to_text
import normalizar_audio
import model
from  post_procesar_transcripcion import deserialize_transcript

def process_audio(file):
    hourIni = datetime.now()
    formato = "%H:%M:%S"
    source_file = file
    result=""
    if os.path.exists(source_file):
        print('\33[32m' + hourIni.strftime(formato) + ' START MAIN' + '\033[0m')

        base = os.path.basename(source_file)
        name = os.path.splitext(base)[0]
        output_name = name + "_output.json"
        try:


            # --- Proceso Normalizar ---
            # print('\33[32m' + datetime.now().strftime(formato) + '\033[0m')

            normalizar_audio.normalizar(source_file)

            # --- Procesos Transcribir ---
            print('\33[32m' + datetime.now().strftime(formato) + '\033[0m')

            storage_uri = cloud_storage.upload_blob(source_file, base)

            result_json_array = speech_to_text.transcribe(storage_uri, Path(__file__).parent / "output" /output_name)
            deserialized_text = deserialize_transcript(result_json_array, True)
            summary = model.generate_summary(deserialized_text.replace("\n", ""))
            result = {"summary": summary, "transcript": deserialized_text}
        except Exception as e:
            print(messages.ERR_UNEXPECTED)
            print(e)
        finally:
            cloud_storage.delete_blob(base)

        print('\33[32m' + datetime.now().strftime(formato) + ' FINISH MAIN' + '\033[0m')
        print('\33[32m' + "Duracion --> " + str(datetime.now() - hourIni) + '\033[0m')
    else:
        print("El archivo de entrada no existe")

    return result
