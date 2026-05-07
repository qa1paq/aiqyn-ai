from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    age = Column(Integer, nullable=True)
    grade = Column(Integer, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    native_language = Column(String, nullable=True)
    english_level = Column(String, nullable=True)  # A1, A2, B1, B2, C1, C2
    target_country = Column(String, nullable=True)
    budget_usd = Column(Integer, nullable=True)
    preferred_study_language = Column(String, nullable=True)
    interests = Column(JSON, nullable=True)  # list of strings
    about = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="profile")
