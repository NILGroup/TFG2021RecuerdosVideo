# importing libraries
import os
import shutil
from datetime import datetime

import a2t_dropSilences as a2t
import normalizar_audio as normAudio
import v2a as v2a


if __name__ == '__main__':

    hourIni = datetime.now()
    formato = "%H:%M:%S"
    nombre = "GH010191"

    print('\33[32m' + hourIni.strftime(formato) + ' START MAIN' + '\033[0m')

    # --- Proceso video2audio ---
    v2a.v2a(nombre)

    # --- Proceso Normalizar ---
    print('\33[32m' + datetime.now().strftime(formato) + '\033[0m')
    fichero = normAudio.normalizar(nombre)

    # --- Procesos Separar por Silencios && Transcribir ---
    print('\33[32m' + datetime.now().strftime(formato) + '\033[0m')
    a2t.transcribe(fichero)

    print('\33[32m' + datetime.now().strftime(formato) + ' FINISH MAIN' + '\033[0m')
    print('\33[32m' + "Duracion --> " + str(datetime.now() - hourIni) + '\033[0m')
