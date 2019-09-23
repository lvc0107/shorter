from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Shorter(Base):
    __tablename__ = "shorter"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)

    def __init__(self, url, code):
        self.url = url
        self.code = code


class Stats(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True)
    code = Column(String, ForeignKey("shorter.code"), nullable=False)
    usage_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    last_usage = Column(DateTime, default=datetime.utcnow, nullable=True)

    def __init__(self, code, created_at):
        self.code = code
        self.created_at = created_at
        self.last_usage = created_at
        self.usage_count = 0
