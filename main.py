from github import Github, GithubException, RateLimitExceededException
from db import SessionLocal, init_db
from models import IssueOpportunity
from utils import generate_comment
import os
import time
import sys
import sqlalchemy.exc
from sqlalchemy import text

MAX_RETRIES = 10
RETRY_DELAY = 3  # seconds
SLEEP_BETWEEN_RUNS = 300  # seconds

RELEVANT_KEYWORDS = [
    "browser automation", "web automation", "headless browser", "ai automation",
    "ai agent", "ai browser agent", "ai agent framework", "agent-based automation",
    "browser automation app", "web automation app", "headless browser app", "ai browser app",
    "browser automation tool", "web automation tool", "headless browser tool", "ai browser tool",
    "browser automation framework", "web automation framework", "headless browser framework",
    "ai browser framework", "browser automation library", "web automation library",
    "headless browser library", "ai browser library", "browser automation solution",
    "web automation solution", "headless browser solution", "ai browser solution",
    "browser automation platform", "web automation platform", "headless browser platform",
    "ai browser platform", "browser automation service", "web automation service",
    "headless browser service", "ai browser service", "browser automation sdk",
    "web automation sdk", "headless browser sdk", "ai browser sdk", "browser automation api",
    "web scraping", "data scraping", "data extraction", "content extraction",
    "structured extraction", "site crawling", "web crawling", "crawl a site",
    "scrape site", "scrape website", "scrape web page", "scrape data", "scrape content",
    "scrape html", "scrape json", "scrape api", "scrape api data", "scrape web api",
    "scrape web service", "scrape web content", "scrape web data", "scrape web page data",
    "scrape web page content", "scrape web page html", "scrape web page json",
    "scrape web page api", "scrape web page api data",
    "test automation", "web testing", "ui testing", "automated test", "ai test summary",
    "testing framework", "automated browser testing", "browser testing", "ai testing",
    "integration testing", "end-to-end testing", "ai-driven testing", "functional test",
    "captcha solving", "anti-bot", "bot detection", "stealth browser", "proxy rotation",
    "anti-scraping", "browser infra", "browser reliability", "fragile automation scripts",
    "parallel scraping", "scalable scraping", "headless browser cloud", "ai test runner",
    "cloud automation", "test orchestration", "openai agent", "claude agent",
    "langchain agent", "llamaindex agent", "ai browser actions", "agent framework",
    "agent-based testing", "agent-based scraping", "ai agent browser", "agent browser automation",
    "agent browser testing", "ai bot", "agent browser", "ai crawler", "open source automation",
    "testing with ai", "hyperbrowser", "hyperagent",
    "automation", "scrape", "scraping", "test", "ai", "agent", "automated", "testing",
    "framework", "browser", "web", "sdk", "platform", "tool", "app", "infra", "service",
    "api", "headless", "proxy", "stealth", "captcha", "extract", "crawl", "data"
]



def get_db_session():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            session = SessionLocal()
            session.execute(text("SELECT 1"))
            print(f" DB connection established (attempt {attempt})", flush=True)
            return session
        except sqlalchemy.exc.OperationalError:
            print(f" DB not ready (attempt {attempt}/{MAX_RETRIES}) — retrying in {RETRY_DELAY}s...", flush=True)
            time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f" Unexpected DB error: {e} — retrying in {RETRY_DELAY}s...", flush=True)
            time.sleep(RETRY_DELAY)
    raise Exception(" Could not connect to the database after several retries.", flush=True)


def is_relevant_issue(title, body):
    text_combined = f"{title.lower()} {body.lower() if body else ''}".strip()
    return any(keyword in text_combined for keyword in RELEVANT_KEYWORDS)


def run():
    init_db()
    g = Github(os.getenv("GITHUB_TOKEN"))
    session = get_db_session()

    repos = [
        "ab4041/Licence-Plate-Detection-and-Recognition-using-YOLO-V8_EasyOCR",
        "ab4041/qr-scan",
        "ab4041/milan-2024",
    ]

    try:
        for repo_name in repos:
            print(f"\n Processing repo: {repo_name}", flush=True)
            try:
                repo = g.get_repo(repo_name)
                for issue in repo.get_issues(state='open'):
                    try:
                        if not is_relevant_issue(issue.title, issue.body):
                            print(f" Skipping irrelevant issue #{issue.number}: {issue.title}", flush=True)
                            continue

                        exists = session.query(IssueOpportunity).filter_by(
                            repo=repo_name, issue_number=issue.number
                        ).first()
                        if exists:
                            print(f"Issue #{issue.number} in {repo_name} already processed.", flush=True)
                            continue

                        print(f" Generating comment for relevant issue #{issue.number}", flush=True)
                        comment = generate_comment(issue.title, issue.body)
                        issue.create_comment(comment)

                        entry = IssueOpportunity(
                            repo=repo_name,
                            issue_number=issue.number,
                            title=issue.title,
                            body=issue.body,
                            comment=comment
                        )
                        session.add(entry)
                        print(f" Saved and commented on issue #{issue.number}.", flush=True)

                    except RateLimitExceededException as e:
                        reset_time = g.get_rate_limit().core.reset.timestamp()
                        wait_time = max(0, reset_time - time.time())
                        print(f" Rate limit exceeded. Sleeping for {wait_time:.0f}s...", flush=True)
                        time.sleep(wait_time + 5)  # Add buffer
                    except GithubException as e:
                        print(f" GitHub API error on issue #{issue.number}: {e}", flush=True)
                    except Exception as e:
                        print(f" Unexpected error on issue #{issue.number}: {e}", flush=True)
                        session.rollback()

            except Exception as repo_err:
                print(f" Repo error for {repo_name}: {repo_err}", flush=True)

        session.commit()

    except Exception as fatal:
        print(f" Fatal error in bot execution: {fatal}", flush=True)
        session.rollback()
    finally:
        session.close()
        print(" Bot run complete.", flush=True)


if __name__ == "__main__":
    while True:
        print(" Running GitHub issue bot...", flush=True)
        run()
        print(f" Sleeping for {SLEEP_BETWEEN_RUNS // 60} minutes before next run...", flush=True)
        time.sleep(SLEEP_BETWEEN_RUNS)
