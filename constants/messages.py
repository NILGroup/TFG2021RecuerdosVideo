from enum import Enum


class messages(Enum):
    # ------------------------------ ERROR -------------------------------------------
    ERR_NO_DIR = "No existe el directorio"
    ERR_BAD_INTERNET = "Error de conexion, comprueba tu internet"
    ERR_UNEXPECTED = "Hubo un error inesperado en el servidor"
    ERR_FILE = "El archivo de entrada no existe"
    ERR_NOT_ALL_FILES_SUPPLIED = "No se han dado todos los ficheros, falta "
    ERR_VALUES_FORMAT = "Los valores dados no están en el fromatoe sperado"
    ERR_FILE_NOT_PROVIDED = "No se ha dado un archivo"
    # ------------------------------ INFO --------------------------------------------
    INFO_UPLOADED = "ha sido subido con éxito"
    INFO_STAGE_JUNTAR = "PROCESO JUNTAR FICHERO"
    INFO_STAGE_VIDEO2AUDIO = "PROCESO VIDEO A AUDIO"
    INFO_JUNTAR_SUCC = 'Fichero Juntado'
    INFO_VIDEO2AUDIO_SUCC = "video convertido a audio en "
    INFO_STAGE_SUMMARY = "PROCESO RESUMEN"
    INFO_SUMMARY_SUCC = "Resumen generado con éxito"
    INFO_CLEAN_SUCC = "Limpieza de audio y video exitosa"
    INFO_STAGE_NORMALIZAR = "PROCESO NORMALIZAR"
    INFO_BLOB_DELETED = "Borrado blob "
    INFO_BLOB_NOT_FOUND = "Blob no encontrado en "
    INFO_FILE_UPLOADED_BUCKET = "Archivo {} subido a bucket {} como {}."
    INFO_MAIL_SENT = "Correo enviado"
    INFO_GOOGLE_TRANSCRIBE_SPEAKER = "PROCESO TRANSCRIPCIÓN HABLANTES GOOGLE"
    INFO_STAGE_SPLIT_SILENCES = "PROCESO SEPARAR POR SILENCIOS"
    INFO_STAGE_TRANSCRIBE_SILENCES = "PROCESO TRANSCRIBIR SILENCIOS"
    AUDIO_NOT_UNDERSTAND = "No se pudo entender el audio "
