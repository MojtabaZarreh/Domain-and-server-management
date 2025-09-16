import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from services.setting import settings
    
def send_email(body: str, subject="notification", recipients=None) -> None:
    if recipients is None:
        recipients = ["YOUR_EMAIL@example.com"]

    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    sender_email = settings.SENDER_EMAIL
    password = settings.PASSWORD

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipients, msg.as_string())