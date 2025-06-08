from github import Github, GithubException
from db import SessionLocal, init_db
from models import IssueOpportunity
from utils import generate_comment
import os
import time
import sqlalchemy.exc
from sqlalchemy import text


MAX_RETRIES = 10
RETRY_DELAY = 3  # seconds

def get_db_session():
    """Retries creating a DB session up to MAX_RETRIES."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            session = SessionLocal()
            session.execute(text("SELECT 1"))  # Use SQLAlchemy text to avoid errors
            print(f"✅ DB connection established (attempt {attempt})")
            return session
        except sqlalchemy.exc.OperationalError:
            print(f"⏳ DB not ready (attempt {attempt}/{MAX_RETRIES}) — retrying in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"❌ Unexpected DB error: {e} — retrying in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
    raise Exception("🚫 Could not connect to the database after several retries.")

def run():
    init_db()
    g = Github(os.getenv("GITHUB_TOKEN"))
    
    repos = [
        "deveshruttala-edu/trivia",
        "deveshruttala-edu/tic-tac-toe-python-college-",
        "deveshruttala-edu/image-gallery-web-php",
    ]

    session = get_db_session()

    try:
        for repo_name in repos:
            print(f"\n🚀 Processing repo: {repo_name}")
            try:
                repo = g.get_repo(repo_name)
                for issue in repo.get_issues(state='open'):
                    # Check for duplicate entry
                    exists = session.query(IssueOpportunity).filter_by(
                        repo=repo_name, issue_number=issue.number
                    ).first()
                    if exists:
                        print(f"⏩ Issue #{issue.number} in {repo_name} already processed.")
                        continue

                    print(f"💬 Generating comment for issue #{issue.number}")
                    comment = None
                    try:
                        comment = generate_comment(issue.title, issue.body)
                        issue.create_comment(comment)
                    except GithubException as e:
                        if e.status == 403:
                            print(f"🚫 GitHub 403 Forbidden on issue #{issue.number}, skipping comment.")
                        else:
                            print(f"⚠️ GitHub API error: {e}")
                    except Exception as e:
                        print(f"⚠️ Error while generating/commenting: {e}")

                    try:
                        entry = IssueOpportunity(
                            repo=repo_name,
                            issue_number=issue.number,
                            title=issue.title,
                            body=issue.body,
                            comment=comment or "Comment failed or not posted."
                        )
                        session.add(entry)
                        print(f"✅ Saved issue #{issue.number} to DB.")
                    except Exception as db_err:
                        print(f"❌ DB error on issue #{issue.number}: {db_err}")
                        session.rollback()

            except Exception as repo_err:
                print(f"💥 Repo error for {repo_name}: {repo_err}")

        session.commit()
    except Exception as fatal:
        print(f"🔥 Fatal error in bot execution: {fatal}")
        session.rollback()
    finally:
        session.close()
        print("🎉 Bot run complete.")

if __name__ == "__main__":
    run()
