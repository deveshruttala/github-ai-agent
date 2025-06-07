from star_bot import run as run_star_bot
from issue_bot import run as run_issue_bot
from models import Base
from db import engine
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

Base.metadata.create_all(bind=engine)

DB_URL = "postgresql://postgres:postgres@db:5432/hyperbrowser"
MAX_RETRIES = 10

for i in range(MAX_RETRIES):
    try:
        engine = create_engine(DB_URL)
        connection = engine.connect()
        print("Database connected.")
        break
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
else:
    raise Exception("Could not connect to the database after multiple attempts.")


Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    run_star_bot()
    run_issue_bot()
