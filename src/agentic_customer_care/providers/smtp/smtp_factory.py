

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

class MailtrapSmtpProvider:
    
    def __init__(self):
        # Initialize the Mailtrap SMTP provider with necessary configurations
        load_dotenv()  # Load environment variables from .env file
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.mailtrap.io")
        self.smtp_port = int(os.getenv("SMTP_PORT", 2525))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")
        self.sender = os.getenv("SMTP_SENDER", "no-reply@yourdomain.com")

    def send_email(self, to_email: str, subject: str, body: str, html_body: str | None = None):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = to_email
        msg.set_content(body)
        if html_body:
            msg.add_alternative(html_body, subtype="html")

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
        except Exception as e:
            raise ValueError(f"Failed to send email: {e}") from e


class SmtpFactory:
    @staticmethod
    def init_smtp_provider(provider_name: str = os.getenv("SMTP_PROVIDER", "mailtrap")):
        if provider_name == "mailtrap":
            return MailtrapSmtpProvider()
        else:
            raise ValueError(f"Unknown SMTP provider: {provider_name}")