from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StarUser(Base):
    __tablename__ = "star_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    profile_url = Column(String)
    starred_at = Column(DateTime)
    email = Column(String, nullable=True)

