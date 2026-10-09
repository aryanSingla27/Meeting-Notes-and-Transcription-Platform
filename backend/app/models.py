from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base

class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    duration = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    participants = relationship("Participant", cascade="all, delete-orphan", back_populates="meeting")
    transcript = relationship("TranscriptSegment", cascade="all, delete-orphan", back_populates="meeting", order_by="TranscriptSegment.start_time")
    summary = relationship("Summary", cascade="all, delete-orphan", back_populates="meeting", uselist=False)
    action_items = relationship("ActionItem", cascade="all, delete-orphan", back_populates="meeting", order_by="ActionItem.id")

class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=True)
    meeting = relationship("Meeting", back_populates="participants")

class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"
    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    speaker = Column(String(120), nullable=False)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    text = Column(Text, nullable=False)
    meeting = relationship("Meeting", back_populates="transcript")

class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"), unique=True, nullable=False)
    overview = Column(Text, nullable=False)
    key_topics = Column(Text, nullable=False, default="")
    outline = Column(Text, nullable=False, default="")
    meeting = relationship("Meeting", back_populates="summary")

class ActionItem(Base):
    __tablename__ = "action_items"
    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    assignee = Column(String(120), default="")
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    meeting = relationship("Meeting", back_populates="action_items")
