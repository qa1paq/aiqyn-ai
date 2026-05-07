from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.base import Base


class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    country = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False)
    website = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    ranking = Column(Integer, nullable=True)
    tuition_min_usd = Column(Integer, nullable=True)
    tuition_max_usd = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    majors = relationship("Major", back_populates="university")
    user_choices = relationship("UserUniversityChoice", back_populates="university")


class Major(Base):
    __tablename__ = "majors"

    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)  # IT_ENGINEERING, DATA_AI, etc.
    degree_level = Column(String, nullable=False)          # Bachelor, Master
    language = Column(String, nullable=False)              # English, German, etc.
    tuition_usd = Column(Integer, nullable=True)
    duration_years = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    university = relationship("University", back_populates="majors")
    user_choices = relationship("UserUniversityChoice", back_populates="major")
