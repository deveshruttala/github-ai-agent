from db import SessionLocal
from models import StarUser
from utils import send_mail_if_needed

def run():
    session = SessionLocal()
    try:
        users = session.query(StarUser).filter(StarUser.email != None).all()
        for user in users:
            send_mail_if_needed(user.email)
    finally:
        session.close()

if __name__ == "__main__":
    run()
