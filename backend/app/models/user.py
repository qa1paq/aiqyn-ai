from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    profile = relationship("Profile", back_populates="user", uselist=False)
    assessment_result = relationship("AssessmentResult", back_populates="user", uselist=False)
    university_choices = relationship("UserUniversityChoice", back_populates="user")
    match_actions = relationship("MatchAction", back_populates="user", foreign_keys="MatchAction.user_id")
    roadmaps = relationship("Roadmap", back_populates="user")
    gamification = relationship("UserGamification", back_populates="user", uselist=False)
    user_achievements = relationship("UserAchievement", back_populates="user")
