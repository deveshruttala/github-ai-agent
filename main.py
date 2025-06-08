import os
import time
from github import Github
from db import SessionLocal, engine
from models import StarUser, Base
from utils import send_mail_if_needed
from sqlalchemy.exc import OperationalError

def wait_for_db(max_retries=10, delay=5):
    retries = 0
    while retries < max_retries:
        try:
            Base.metadata.create_all(bind=engine)  # Will fail if DB isn't ready
            print("✅ Database connection established.")
            return
        except OperationalError as e:
            retries += 1
            print(f"⏳ Waiting for database... ({retries}/{max_retries}) | {e}")
            time.sleep(delay)
    raise Exception("❌ Could not connect to database after multiple retries.")

def run():
    wait_for_db()

    g = Github(os.getenv("GITHUB_TOKEN"))
    repo_name = os.getenv("GITHUB_REPO")

    session = SessionLocal()

    try:
        repo = g.get_repo(repo_name)
        print(f"🔍 Processing stargazers for repo: {repo_name}")

        for stargazer in repo.get_stargazers():
            username = stargazer.login
            profile_url = stargazer.html_url
            email = getattr(stargazer, "email", None)

            exists = session.query(StarUser).filter_by(username=username).first()
            if exists:
                print(f"🔁 Already stored: {username}")
                continue

            user = StarUser(username=username, profile_url=profile_url, email=email)
            session.add(user)
            session.commit()

            print(f"⭐ Added user: {username} | Email: {email or 'N/A'}")

            if email:
                try:
                    send_mail_if_needed(email)
                    print(f"📧 Email sent to {email}")
                except Exception as mail_err:
                    print(f"❌ Failed to send email to {email}: {mail_err}")

    except Exception as e:
        print(f"❌ Bot run failed: {e}")
        session.rollback()
    finally:
        session.close()
        print("✅ Bot run complete.")

if __name__ == "__main__":
    run()
