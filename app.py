import os
import logging
import a2t_dropSilences as a2t
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['carpetaInputs'] = "./filesInput"
@app.route('/')
def index():
    # print('Hola de nuevo')
    return render_template('index.html')


@app.route('/subirFichero', methods = ['POST'])
def subir_fichero():
    file = request.files['archivo']
    #save el wav en el directorio
    file.save(os.path.join(app.config['carpetaInputs'], file.filename))
    a2t.transcribe(file.filename)
    filename = "./filesTranscriptions/transcrip_" + file.filename.split(".")[0] + ".txt"
    manejador = open(filename, "r")
    texto = manejador.read()
    return texto.replace("\n", "<br>")


if __name__ == '__main__':
    app.run(debug = True, port = 80)

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
