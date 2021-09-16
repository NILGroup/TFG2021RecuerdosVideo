# TFG - Generación de resúmenes de vídeo-entrevistas utilizando redes neuronales
Este es el repositorio del código del Trabajo de Fin de Grado del año 2020/2021 **Generación de resúmenes de vídeo-entrevistas utilizando redes neuronales** de la Universidad Complutense de Madrid realizado por Francisco Javier Lozano Hernández y Daniel Alcázar Muñoz. La aplicación web se encuentra en [este enlace](https://holstein.fdi.ucm.es/tfg/2021/video/).
## Instrucciones de uso
La web tiene una zona donde puedes arastrar un archivo de vídeo MP4 y un botón para procesarlo. Después de un rato, a la derecha aparecerá una transcripción de lo que se habla en el vídeo y un resumen dependiendo de los parámetros utilizados:
* **Transcribir con separación por silencios:** Realiza la transcripción del audio del archivo mediante los silencios que se detecten utilizando la biblioteca SpeechRecognition.
* **Transcribir con separación por hablantes:** Realiza la transcripción del audio del archivo utilizando la API de SpeechToTExt de Google junto a su funcionalidad de detección de hablantes. Delante de cada intervención aparecen un número y dos puntos: Este número es el ```speaker_tag``` que la API ha puesto a ese interlocutor.
* **Resumir hablantes por separado:** Realiza un resumen de las intervenciones de cada interlocutor por separado. Se puede combinar con la siguiente opción.
* **Resumir por segmentos**: Realiza un resumen segmentando el texto en fragmentos de varias frases. Sí se ha habilitado la opción de ```Resumir hablantes por separado```, se segmentarán las intervenciones de cada interlocutor por separado.
* **Tamaño del segmento:** El número de frases que abarca cada segmento. Va desde 3 hasta 30, pero es ignorado si no se marca la opción de ``` Resumir por segmentos ```
## Cómo ejecutar por tu cuenta
Si quieres ejecutar el código por ti mismo estas son las instrucciones que debes seguir:

Antes de nada instala las dependencias ejecutando el siguiente comando
```
pip install -r requirements.txt
```
Es posible que en algunas versiones de python haya problemas para instalar ciertas dependencias, en cuyo caso simplemente anota el paquete que está causando problemas y elimínalo del archivo ``` requirements.txt```

Ahora debes crear el archivo ``` resources.py ``` en la raíz y añadir lo siguiente:
```
api_key = r'ruta/a/tu/archivo/de/la/clave/API'
```
Esta parte es necesaria para utilizar las funciones de separación por hablantes, ya que utiilza el servicio de [SpeechToText de Google](https://cloud.google.com/speech-to-text?hl=es). Para crear la clave de la API primero habilita [Google Cloud](https://cloud.google.com/) en tu cuenta y sigue el apartado **Configurar la autenticación** de [este tutorial](https://cloud.google.com/speech-to-text/docs/libraries?hl=es#linux-or-macos) hasta que hayas descargado el JSON de la clave.

Después ejecuta ```app.py``` con tu versión de python. Se recomienda Python 3.8 o mayor.
