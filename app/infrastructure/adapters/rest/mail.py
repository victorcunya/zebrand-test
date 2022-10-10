from os import getenv
from smtplib import SMTP

from app.config import settings
from app.core.repository.mail import MailRepository
from app.core.schema.mail import MailBase


class   MailSMTPAdapter(MailRepository):

    def send_mail(self, data: MailBase):
        recipients = settings.EMAIL_RECIPIENTS.split(',')
        sender = settings.EMAIL_DEFAULT_SENDER.strip()
        message = (
                f"Subject: {data.subject}\n" +
                f"To: {', '.join(recipients)}\n" +
                f"From: {sender}\n\n" +
                f"{data.body}").encode("utf-8")
        try:
            with SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                if settings.SMTP_USE_TLS:
                    server.starttls()
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                return server.sendmail(
                    sender, recipients, message)
        except Exception as e:
            raise e
