import os, smtplib
from email.message import EmailMessage

def send_email(subject: str, body: str):
    host = os.getenv("SMTP_HOST","smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT","587"))
    user = os.getenv("SMTP_USER")
    pwd  = os.getenv("SMTP_PASS")
    to   = os.getenv("MAIL_TO", user)
    if not user or not pwd:
        return False, "SMTP_USER/SMTP_PASS not set"
    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(host, port, timeout=10) as s:
        s.starttls()
        s.login(user, pwd)
        s.send_message(msg)
    return True, "sent"