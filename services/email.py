import smtplib
from email.mime.text import MIMEText
from email.header import Header
import logging


def send_email(to, transcript, summary):
    sender_email = 'tfg2021ResumenVideoRedNeuronal@gmail.com'
    subject = 'Para la mas putita'
    
    text = (f"Este es el resultado obtenido del video que has subido a nuestro servicio web: \n\n"
            f"TRANSCRIPCIÓN:\n\n"
            f"{transcript}\n\n"
            f"RESUMEN:\n\n"
            f"{summary}\n")
    
    message = MIMEText(text, 'plain')
    message['From'] = sender_email
    message['To'] = to
    message['Subject'] = Header(subject, 'utf-8')
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, 'transformers2021')
        server.sendmail(sender_email, to, message.as_string())
    except Exception as ex:
        logging.exception(ex)
    finally:
        server.quit()
    
    return
