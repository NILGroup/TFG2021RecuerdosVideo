# importing libraries
from datetime import datetime

import a2t_dropSilences as a2t
import a2t_dropSilencesNor as a2tN
import normalizar_audio as normAudio
import v2a as v2a


if __name__ == '__main__':

    hourIni = datetime.now()
    formato = "%H:%M:%S"
    archivo = "GH010191.wav"
    
    nombre = archivo.split(".")[0]
    extension = "." + archivo.split(".")[1]

    print('\33[32m' + hourIni.strftime(formato) + ' START PROCESS' + '\033[0m')
    
    # --- Proceso video2audio ---
    #v2a.v2a(nombre, extension)s
    
    # --- Proceso Normalizar ---
    print('\33[32m' + datetime.now().strftime(formato) + '\033[0m')
    #fichero = normAudio.normalizar(nombre)
    
    # --- Procesos Separar por Silencios && Transcribir ---
    print('\33[32m' + datetime.now().strftime(formato) + '\033[0m')
    a2t.transcribe(archivo)
    
    print('\33[32m' + datetime.now().strftime(formato) + ' FINISH PROCESS' + '\033[0m')
    print('\33[32m' + "Duracion --> " + str(datetime.now() - hourIni) + '\033[0m')
