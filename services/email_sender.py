import logging
from constants.messages import messages
import os
import shutil
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from resources import sender_email, passw


def send_email(to, transcript, summary, save_dir):
    
    subject = '[TFG2021: Resumen Video] Resultados'
    text = "En los archivos adjuntos se encuentras los resultado del video que has subido a nuestro servicio web: \n"
    
    transcripcion = f"\nTRANSCRIPCIÓN:\n{transcript}"
    resumen = f"\nRESUMEN:\n{summary}"
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to
    message['Subject'] = subject
    message.attach(MIMEText(text, 'plain'))
    
    try:
        
        if not save_dir.exists():
            save_dir.mkdir(exist_ok = True, parents = True)
        
        # Creación de ficheros con los resultados que se van a enviar
        f1 = open(f"{save_dir}/transcripcion.txt", "w+", encoding = "ISO-8859-1")
        f1.write(transcripcion)
        f1.close()
        f2 = open(f"{save_dir}/resumen.txt", "w+", encoding = "ISO-8859-1")
        f2.write(resumen)
        f2.close()
        
        # Adjuntar los ficheros al correo
        files = os.listdir(save_dir)
        for f in files:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(f"{save_dir}/{f}", "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(f)}")
            message.attach(part)
        
        # Conexión al servidor y envío del correo
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, passw)
        server.sendmail(sender_email, to, message.as_string())
        logging.log(messages.INFO_MAIL_SENT.value)
    
    except Exception as ex:
        logging.exception(ex)
    finally:
        server.quit()
        shutil.rmtree(save_dir)
    
    return
