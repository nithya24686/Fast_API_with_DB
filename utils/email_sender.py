import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()
sender_email = os.getenv("sender_email")
password = os.getenv("app_password")


def send_email(receiver_email: str, subject: str, content: str) -> str:
    """Send an email to a given receiver with a subject and content."""
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.set_content(content)

    # SMTP server setup
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)

    return f"Email sent successfully to {receiver_email}!"

