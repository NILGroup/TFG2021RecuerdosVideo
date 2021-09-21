from enum import Enum


class messages(Enum):
    ERR_UNEXPECTED = "Hubo un error inesperado en el servidor"
    ERR_FILE = "El archivo de entrada no existe"
    #-------------------------------------------------------------------------------------
    INFO_UPLOADED =  "ha sido subido con éxito"