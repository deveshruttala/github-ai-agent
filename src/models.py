# models.py
from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime
from db import Base 

class StarUser(Base):
    __tablename__ = 'star_users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    profile_url = Column(String)
    starred_at = Column(DateTime, default=datetime.utcnow)

class IssueOpportunity(Base):
    __tablename__ = 'issue_opportunities'
    id = Column(Integer, primary_key=True)
    repo = Column(String)
    issue_number = Column(Integer)
    title = Column(String)
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    comment = Column(Text)
