from github import Github, GithubException
from db import SessionLocal
from models import IssueOpportunity
from utils import generate_comment
import os

def run():
    g = Github(os.getenv("GITHUB_TOKEN"))
    repos = [
        "browser-use/browser-use",
        "AutomaApp/automa",
        "Skyvern-AI/skyvern",
        "steel-dev/steel-browser",
        "getmaxun/maxun",
        "lightpanda-io/browser",
    ]

    session = SessionLocal()
    try:
        for repo_name in repos:
            print(f"\n🚀 Processing repo: {repo_name}")
            try:
                repo = g.get_repo(repo_name)
                for issue in repo.get_issues(state='open'):
                    exists = session.query(IssueOpportunity).filter_by(
                        repo=repo_name, issue_number=issue.number
                    ).first()
                    if exists:
                        print(f"⏩ Issue #{issue.number} already in DB, skipping.")
                        continue

                    print(f"💬 Generating comment for issue #{issue.number}")
                    comment = None
                    try:
                        comment = generate_comment(issue.title, issue.body)
                        issue.create_comment(comment)
                    except GithubException as e:
                        if e.status == 403:
                            print(f"🚫 403 Forbidden on issue #{issue.number}, skipping issue.")
                        else:
                            print(f"⚠️ Error commenting on issue #{issue.number}: {e}")
                        # Save even if commenting fails
                    except Exception as e:
                        print(f"⚠️ Unexpected error: {e}")

                    # Save issue info to DB regardless of comment success
                    try:
                        i = IssueOpportunity(
                            repo=repo_name,
                            issue_number=issue.number,
                            title=issue.title,
                            body=issue.body,
                            comment=comment or "Comment failed or not posted due to error."
                        )
                        session.add(i)
                        print(f"✅ Logged issue to DB: {repo_name} #{issue.number}")
                    except Exception as db_err:
                        print(f"❌ DB error on issue #{issue.number}: {db_err}")
                        session.rollback()
                        continue
            except Exception as repo_err:
                print(f"💥 Repo error ({repo_name}): {repo_err}")

        session.commit()
    except Exception as e:
        print(f"🔥 Fatal error: {e}")
        session.rollback()
    finally:
        session.close()
        print("\n🎉 Bot run complete.")
