from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.base import Base


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    raw_scores = Column(JSON, nullable=False)        # {"IT_ENGINEERING": 45, ...}
    normalized_scores = Column(JSON, nullable=False) # {"IT_ENGINEERING": 82.5, ...}
    top_categories = Column(JSON, nullable=False)    # ["IT_ENGINEERING", "DATA_AI", "BUSINESS"]
    recommended_majors = Column(JSON, nullable=False)# ["Software Engineering", ...]
    profile_summary = Column(Text, nullable=True)
    answers = Column(JSON, nullable=False)           # {"q1": "a", "q2": "b", ...}
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="assessment_result")
