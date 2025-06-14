import logging

import emails

from app.config import SMTPConfig


logger = logging.getLogger(__name__)


#TODO: заменить на асинхронную smtp-библиотеку


class EmailService:
    def __init__(self, config: SMTPConfig, name: str):
        self._config = config
        self.name = name

    async def send_email(self, email_to: str, subject: str, body: str, text: str = None):
        message = emails.Message(
            subject=subject,
            html=body,
            text=text,
            mail_from=(self.name, self._config.user)
        )

        message.send(to=email_to, smtp=self._config.options)

        logger.info(f"Email was sent on email {email_to}")
