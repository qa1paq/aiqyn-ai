from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.base import Base


class UserUniversityChoice(Base):
    __tablename__ = "user_university_choices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=True)
    status = Column(String, default="interested")  # interested, applying, applied, accepted
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="university_choices")
    university = relationship("University", back_populates="user_choices")
    major = relationship("Major", back_populates="user_choices")
