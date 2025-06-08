# from github import Github
# from db import SessionLocal
# from models import StarUser
# import os

# def run():
#     g = Github(os.getenv("GITHUB_TOKEN"))
#     repo = g.get_repo(os.getenv("GITHUB_REPO"))
#     session = SessionLocal()
    
#     for user in repo.get_stargazers():
#         if session.query(StarUser).filter_by(username=user.login).first():
#             continue
#         u = StarUser(
#             username=user.login,
#             profile_url=user.html_url
#         )
#         session.add(u)
#         print(f"Added star user: {user.login}")
#     session.commit()
#     session.close()


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
        try:
            gh_user = g.get_user(user.login)
            email = gh_user.email  # May be None if private
        except Exception as e:
            print(f"Error fetching email for {user.login}: {e}")
            email = None

        u = StarUser(
            username=user.login,
            profile_url=user.html_url,
            email=email  # Will be None if not public
        )
        session.add(u)
        print(f"Added star user: {user.login} | Email: {email}")
        
    try:
        session.commit()
    except Exception as e:
        print(f"Commit failed: {e}")
        session.rollback()
    finally:
        session.close()
