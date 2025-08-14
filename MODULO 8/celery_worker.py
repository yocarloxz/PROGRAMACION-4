from celery_app import celery, app, mail
from flask_mail import Message

@celery.task(bind=True, max_retries=3)
def send_email_task(self, recipients, subject, body):
    try:
        with app.app_context():  # Necesario para usar Flask-Mail dentro de Celery
            if not recipients:
                return "No hay destinatarios definidos."

            # Asegurarse de que recipients sea una lista
            if isinstance(recipients, str):
                recipients = [recipients]

            msg = Message(
                subject=subject,
                recipients=recipients,
                body=body,
                sender=app.config.get("MAIL_DEFAULT_SENDER")
            )
            mail.send(msg)
            return f"Correo enviado a {recipients}"

    except Exception as e:
        # Reintenta hasta 3 veces si falla
        raise self.retry(exc=e, countdown=10)
