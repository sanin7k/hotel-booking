import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(to: str, subject: str, body: str) -> None:
    """Send an email using SMTP."""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = to

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
