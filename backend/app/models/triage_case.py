"""
TriageCase Model - SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class TriageCase(Base):
    __tablename__ = "triage_cases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)

    # Patient Input
    symptoms_raw = Column(Text, nullable=False)  # Raw text input
    symptoms_extracted = Column(JSON, nullable=True)  # Extracted symptom keywords
    duration = Column(String(100), nullable=True)
    intensity = Column(Integer, nullable=True)  # 1-10
    medical_history = Column(Text, nullable=True)
    chat_history = Column(JSON, nullable=True)  # Full chat conversation

    # Triage Results
    urgency_level = Column(String(20), nullable=True)  # LOW, MEDIUM, HIGH
    severity_score = Column(Float, nullable=True)  # 0-100
    recommended_action = Column(String(50), nullable=True)  # self-care, consult-doctor, emergency
    triggered_rules = Column(JSON, nullable=True)  # Rules that fired
    reasoning = Column(Text, nullable=True)  # AI explanation

    # Visual Data
    affected_regions = Column(JSON, nullable=True)  # Body regions with severity
    condition_images = Column(JSON, nullable=True)  # Mapped condition images

    # Metadata
    language = Column(String(10), default="en")
    is_emergency = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="triage_cases")
