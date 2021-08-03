import os
from messages import messages
import logging
from video2audio import v2a as video2audio
from flask import Flask, render_template, request, make_response, jsonify
from threading import Lock
from collections import defaultdict
import shutil
from pathlib import Path
from requests import HTTPError

import controller
from werkzeug.utils import secure_filename

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

lock = Lock()
chucks = defaultdict(list)
chunk_path = Path(__file__).parent / "chunks"
storage_path = Path(__file__).parent / "input"
converted_path = Path(__file__).parent / "converted"
output_path = Path(__file__).parent / "output"
chunk_path.mkdir(exist_ok=True, parents=True)
storage_path.mkdir(exist_ok=True, parents=True)
converted_path.mkdir(exist_ok=True, parents=True)
output_path.mkdir(exist_ok=True, parents=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/subirFichero', methods=['POST'])
def subir_fichero():
    try:
        result = ""
        file = request.files.get("file")
        if not file:
            raise HTTPError(status=400, body="No file provided")
        dz_uuid = request.form["dzuuid"]
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
                f.close()
            shutil.rmtree(save_dir)
            logging.info(f"{file.filename} has been uploaded")
            input_file = uploaded_file
            try:
                audio_path = video2audio(input_file, converted_path)
                result = controller.process_audio(audio_path)
            finally:
                if audio_path.exists():
                    os.remove(audio_path)
                if input_file.exists():
                    os.remove(input_file)
        return make_response(jsonify(result), 200)
    except Exception as e:
        logging.exception(e)
        return make_response(messages.ERR_UNEXPECTED, 500)


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)
