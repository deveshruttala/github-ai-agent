from github import Github
from db import SessionLocal
from models import StarUser
import os

def run():
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(os.getenv("GITHUB_REPO"))
    session = SessionLocal()
    
    for user in repo.get_stargazers():
        if session.query(StarUser).filter_by(username=user.login).first():
            continue
        u = StarUser(
            username=user.login,
            profile_url=user.html_url
        )
        session.add(u)
        print(f"Added star user: {user.login}")
    session.commit()
    session.close()
