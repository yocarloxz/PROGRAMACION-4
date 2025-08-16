from celery_app import celery
from flask_mail import Message
from extensions import mail


@celery.task
def send_email_task(to, subject, body):
    """
    Envía un email usando Flask-Mail.
    `to` debe ser una lista de correos.
    """
    if not to:
        return "No hay destinatarios"

    msg = Message(subject=subject, recipients=to, body=body)
    mail.send(msg)
    return f"Email enviado a {to}"
