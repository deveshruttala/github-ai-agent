import smtplib
from email.mime.text import MIMEText
import os

def send_mail_if_needed(email):
    try:
        smtp_server = os.getenv("MAIL_SERVER")
        smtp_port = int(os.getenv("MAIL_PORT", 587))
        smtp_user = os.getenv("MAIL_USER")
        smtp_pass = os.getenv("MAIL_PASSWORD")

        msg = MIMEText("Thanks for starring our GitHub repo! ❤️\n\nStay tuned for updates!")
        msg["Subject"] = "Thank You from HyperBrowser"
        msg["From"] = smtp_user
        msg["To"] = email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [email], msg.as_string())
            print(f"Email sent to {email}")
    except Exception as e:
        print(f"Email failed for {email}: {e}")
