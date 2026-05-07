from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.base import Base


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    target_major = Column(String, nullable=False)
    target_country = Column(String, nullable=False)
    roadmap_title = Column(String, nullable=False)
    roadmap_summary = Column(Text, nullable=True)
    duration_months = Column(Integer, nullable=False, default=6)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="roadmaps")
    steps = relationship("RoadmapStep", back_populates="roadmap", order_by="RoadmapStep.month_number, RoadmapStep.week_number")


class RoadmapStep(Base):
    __tablename__ = "roadmap_steps"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False, index=True)
    month_number = Column(Integer, nullable=False)
    week_number = Column(Integer, nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    tasks = Column(JSON, nullable=True)  # list of task strings
    xp_reward = Column(Integer, default=50)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    roadmap = relationship("Roadmap", back_populates="steps")
