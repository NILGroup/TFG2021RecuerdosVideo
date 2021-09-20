import logging
import os
from pathlib import Path
import shutil
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders


def send_email(to, transcript, summary, name):
    
    sender_email = 'tfg2021ResumenVideoRedNeuronal@gmail.com'
    subject = '[TFG2021: Resumen Video] Resultados'
    text = "En los archivos adjuntos se encuentras los resultado del video que has subido a nuestro servicio web: \n"
    
    filename = name + ".txt"
    transcripcion = f"\nTRANSCRIPCIÓN:\n{transcript}"
    resumen = f"\nRESUMEN:\n{summary}"
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to
    message['Subject'] = subject
    message.attach(MIMEText(text, 'plain'))
    
    try:
        
        if os.path.exists('outputFiles'):
            shutil.rmtree('outputFiles')
        
        os.mkdir('outputFiles')
        os.chdir('outputFiles')
        
        # Creación de ficheros con los resultados que se van a enviar
        f1 = open("transcripcion_" + filename, "w+", encoding = "ISO-8859-1")
        f1.write(transcripcion)
        f1.close()
        f2 = open("resumen_" + filename, "w+", encoding = "ISO-8859-1")
        f2.write(resumen)
        f2.close()
        
        # Adjuntar los ficheros al correo
        files = os.listdir(Path(__file__).parent.parent / "outputFiles")
        for f in files:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(f, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= {0}".format(os.path.basename(f)))
            message.attach(part)
        
        # Conexión al servidor y envío del correo
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, 'transformers2021')
        server.sendmail(sender_email, to, message.as_string())
    
    except Exception as ex:
        logging.exception(ex)
    finally:
        server.quit()
        os.chdir('..')
        if os.path.exists('outputFiles'):
            shutil.rmtree('outputFiles')
    
    return

