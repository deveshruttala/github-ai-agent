from github import Github
from db import SessionLocal
from models import IssueOpportunity
from utils import generate_comment
import os

def run():
    g = Github(os.getenv("GITHUB_TOKEN"))
    repos = [
        "browser-use/browser-use",
        "Skyvern-AI/skyvern",
        "steel-dev/steel-browser",
        "AutomaApp/automa",
        "getmaxun/maxun",
        "lightpanda-io/browser",
    ]
    
    session = SessionLocal()

    for repo_name in repos:
        print(f"Processing repo: {repo_name}")
        try:
            repo = g.get_repo(repo_name)
            for issue in repo.get_issues(state='open'):
                exists = session.query(IssueOpportunity).filter_by(
                    repo=repo_name, issue_number=issue.number
                ).first()
                if exists:
                    print(f"Issue #{issue.number} already in DB, skipping.")
                    continue

                print(f"Generating comment for issue #{issue.number}")
                try:
                    comment = generate_comment(issue.title, issue.body)
                    issue.create_comment(comment)
                except Exception as e:
                    print(f"Error generating/commenting on issue #{issue.number}: {e}")
                    continue  # Skip to next issue

                try:
                    i = IssueOpportunity(
                        repo=repo_name,
                        issue_number=issue.number,
                        title=issue.title,
                        body=issue.body,
                        comment=comment
                    )
                    session.add(i)
                    print(f"Commented and saved to DB: {repo_name} #{issue.number}")
                except Exception as db_err:
                    print(f"Failed to insert issue #{issue.number} into DB: {db_err}")
                    continue
        except Exception as repo_err:
            print(f"Error processing repo {repo_name}: {repo_err}")
    
    session.commit()
    session.close()
    print("Bot run complete.")
