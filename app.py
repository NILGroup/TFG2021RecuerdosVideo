import os
import logging
from video2audio import v2a as video2audio
from flask import Flask, render_template, request, make_response
from threading import Lock
from collections import defaultdict
import shutil
import uuid
from pathlib import Path
from requests import HTTPError

import controller
import a2t_dropSilences as a2
from werkzeug.utils import secure_filename

print("")
app = Flask(__name__)
#app.config['carpetaInputs'] = "./input"

lock = Lock()
chucks = defaultdict(list)
chunk_path = Path(__file__).parent / "chunks"
storage_path = Path(__file__).parent / "input"
converted_path = Path(__file__).parent / "converted"
chunk_path.mkdir(exist_ok=True, parents=True)
storage_path.mkdir(exist_ok=True, parents=True)
converted_path.mkdir(exist_ok=True, parents=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/subirFichero', methods=['POST'])
def subir_fichero():
    result=""
    file = request.files.get("file")
    if not file:
        raise HTTPError(status=400, body="No file provided")
    dz_uuid = request.form["dzuuid"]
    if not dz_uuid:
        # Assume this file has not been chunked
        with open(storage_path / f"{uuid.uuid4()}_{secure_filename(file.filename)}", "wb") as f:
            file.save(f)
        return "File Saved"
    # Chunked download
    try:
        current_chunk = int(request.form["dzchunkindex"])
        total_chunks = int(request.form["dztotalchunkcount"])
    except KeyError as err:
        raise HTTPError(status=400, body=f"Not all required fields supplied, missing {err}")
    except ValueError:
        raise HTTPError(status=400, body=f"Values provided were not in expected format")

    # Create a new directory for this file in the chunks dir, using the UUID as the folder name
    save_dir = chunk_path / dz_uuid
    if not save_dir.exists():
        save_dir.mkdir(exist_ok=True, parents=True)
    # Save the individual chunk
    with open(save_dir / str(request.form["dzchunkindex"]), "wb") as f:
        file.save(f)
    # See if we have all the chunks downloaded
    with lock:
        chucks[dz_uuid].append(current_chunk)
        completed = len(chucks[dz_uuid]) == total_chunks
    # Concat all the files into the final file when all are downloaded
    if completed:
        uploaded_file = storage_path / f"{dz_uuid}_{secure_filename(file.filename)}"
        with open(uploaded_file, "wb") as f:
            for file_number in range(total_chunks):
                f.write((save_dir / str(file_number)).read_bytes())
        shutil.rmtree(save_dir)
        print(f"{file.filename} has been uploaded")
        input_file = uploaded_file
        try:
            audio_path = video2audio(input_file, converted_path)
            result = controller.process_video(audio_path)
        finally:
            os.remove(audio_path)
            os.remove(input_file)
    #save el video en el directorio
    #newpath = os.path.join(app.config['carpetaInputs'], file.filename)
    #file.save(newpath)
    #a2t.transcribe(file.filename)
    #result = controller.process_video(newpath)
    #filename = "./filesTranscriptions/transcrip_" + file.filename.split(".")[0] + ".txt"
    #manejador = open(filename, "r")
    #texto = manejador.read()
    #return make_response((result, 200))
    return result


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)

'''
@app.route('/user/<userId>')
def hello_world(userId):
    return userId
'''

'''
@app.route('/user/<userId>', methods = ['GET'])
def hello_world(userId):
    return userId
'''
