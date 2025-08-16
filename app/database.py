"""
db.py

Tiny SQLite persistence for saved summaries.
Uses SQLAlchemy for portability.
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DB_PATH = os.getenv("MEETING_SUMMARY_DB", "sqlite:///summaries.db")
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    prompt = Column(Text)
    original_transcript = Column(Text)
    generated_summary = Column(Text)
    edited_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def save_summary(title, prompt, transcript, generated, edited=None):
    session = SessionLocal()
    s = Summary(
        title=title or "Untitled",
        prompt=prompt,
        original_transcript=transcript,
        generated_summary=generated,
        edited_summary=edited or generated,
    )
    session.add(s)
    session.commit()
    session.refresh(s)
    session.close()
    return s.id


def list_summaries(limit=50):
    session = SessionLocal()
    rows = session.query(Summary).order_by(Summary.created_at.desc()).limit(limit).all()
    session.close()
    return rows


def get_summary(summary_id):
    session = SessionLocal()
    row = session.query(Summary).filter(Summary.id == summary_id).first()
    session.close()
    return row


def delete_summary(summary_id):
    session = SessionLocal()
    row = session.query(Summary).filter(Summary.id == summary_id).first()
    if row:
        session.delete(row)
        session.commit()
    session.close()


def delete_all_summaries():
    session = SessionLocal()
    session.query(Summary).delete()
    session.commit()
    session.close()

