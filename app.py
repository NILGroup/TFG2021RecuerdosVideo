import os
from constants.messages import messages
import logging

from constants.paths import temp_path, chunk_video_path, input_video_path, normalized_audio_path, output_email_path, \
    chunks_audio_path
from video_to_audio import v2a as video2audio
from flask import Flask, render_template, request, make_response, jsonify
from threading import Lock
from collections import defaultdict
import shutil
from requests import HTTPError
from datetime import datetime

import controller
from werkzeug.utils import secure_filename


app = Flask(__name__,
            static_url_path = "",
            static_folder = "web/static",
            template_folder = "web/templates")

lock = Lock()
chunks = defaultdict(list)

# Creacion de directorios si no existen
temp_path.mkdir(exist_ok = True, parents = True)
chunk_video_path.mkdir(exist_ok = True, parents = True)
input_video_path.mkdir(exist_ok = True, parents = True)
normalized_audio_path.mkdir(exist_ok = True, parents = True)
output_email_path.mkdir(exist_ok = True, parents = True)
chunks_audio_path.mkdir(exist_ok = True, parents = True)

formato = "%H:%M:%S"

os.environ["TOKENIZERS_PARALLELISM"] = "false"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/subirFichero', methods = ['POST'])
def subir_fichero():
    try:
        result = ""
        audio_path = ""
        input_file = ""
        file = request.files.get("file")
        mode_trancript = request.form.get('modoTrancript')
        divide_by_speaker = request.form.get('divideBySpeaker')
        divide_by_segments = request.form.get('divideBySegments')
        size_segments = int(request.form.get('sizeSegments'))
        email = request.form.get('email')
        
        if divide_by_segments == 'on':
            divide_by_segments = True
        else:
            divide_by_segments = False
        
        if divide_by_speaker == 'on':
            divide_by_speaker = True
        else:
            divide_by_speaker = False
        
        if not file:
            raise HTTPError(status = 400, body = "No file provided")
        dz_uuid = request.form["dzuuid"]
        # Descarga con chunks
        try:
            current_chunk = int(request.form["dzchunkindex"])
            total_chunks = int(request.form["dztotalchunkcount"])
        except KeyError as err:
            raise HTTPError(status = 400, body = f"Not all required fields supplied, missing {err}")
        except ValueError:
            raise HTTPError(status = 400, body = f"Values provided were not in expected format")

        # Crea un nuevo directorio para este archivo  en el dir de los chunks, usando el UUID como nombre de carpeta
        save_dir = chunk_video_path / dz_uuid
        if not save_dir.exists():
            save_dir.mkdir(exist_ok = True, parents = True)
        # Guarda el chunk individual
        with open(save_dir / str(request.form["dzchunkindex"]), "wb") as f:
            file.save(f)
        # Ver si tenemos todos los chunks guardados
        with lock:
            chunks[dz_uuid].append(current_chunk)
            completed = len(chunks[dz_uuid]) == total_chunks
        # Concatenar todos los archivos si se han subido todos
        if completed:
            print('\33[32m' + 'JUNTAR FICHERO' + '\033[0m')
            logging.info('Fichero Juntado')
            uploaded_file = input_video_path / f"{dz_uuid}_{secure_filename(file.filename)}"
            with open(uploaded_file, "wb") as f:
                for file_number in range(total_chunks):
                    f.write((save_dir / str(file_number)).read_bytes())
                f.close()
            shutil.rmtree(save_dir)
            logging.info(f"{file.filename}" + messages.INFO_UPLOADED.value)
            input_file = uploaded_file
            try:
                hour_ini = datetime.now()
                print('\33[32m' + hour_ini.strftime(formato) + ' START MAIN' + '\033[0m')
                audio_path = ""
                audio_path = video2audio(input_file, normalized_audio_path)
                result = controller.process_audio(audio_path, mode_trancript, divide_by_speaker, divide_by_segments,
                                                  size_segments, email)
                
                print('\33[32m' + datetime.now().strftime(formato) + ' FINISH MAIN' + '\033[0m')
                print('\33[32m' + "Duracion --> " + str(datetime.now() - hour_ini) + '\033[0m')
            
            finally:
                if audio_path != "" and audio_path.exists():
                    os.remove(audio_path)
                if audio_path != "" and input_file.exists():
                    os.remove(input_file)
            print('\33[32m' + datetime.now().strftime(formato) + ' TODO CORRECTO' + '\033[0m')
            
            return make_response(jsonify(result), 200)
    except Exception as e:
        logging.exception(e)
        return make_response(messages.ERR_UNEXPECTED.value, 500)
    
    return make_response(jsonify(result), 206)


if __name__ == '__main__':
    app.run(debug = True)
