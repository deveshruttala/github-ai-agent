from sqlalchemy import Column, Integer, String, Text
from db import Base

class IssueOpportunity(Base):
    __tablename__ = "issue_opportunities"

    id = Column(Integer, primary_key=True, index=True)
    repo = Column(String, index=True)
    issue_number = Column(Integer)
    title = Column(String)
    body = Column(Text)
    comment = Column(Text)
