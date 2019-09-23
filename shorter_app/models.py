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

    def __repr__(self):
        return f"<Shorter(url='{self.url}', code='{self.code}')>"


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

    def __repr__(self):
        return f"<Stats(code='{self.code}', usage_count='{self.usage_count}', created_at='{self.created_at}', usage_count='{self.usage_count} )>"
