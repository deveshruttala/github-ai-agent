import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db import SessionLocal
from models import StarUser

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Use an App Password if using Gmail

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def run_email_notifier():
    session = SessionLocal()
    users = session.query(StarUser).filter(StarUser.email != None).all()

    for user in users:
        subject = f"Thanks for starring Hyperbrowser!"
        body = f"Hi {user.username},\n\nThanks for supporting Hyperbrowser!\n\nVisit us again: {user.profile_url}\n\n– Hyperbrowser Team"
        send_email(user.email, subject, body)

    session.close()

if __name__ == "__main__":
    run_email_notifier()
