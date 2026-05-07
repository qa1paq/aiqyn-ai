from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    grade: Optional[int] = None
    city: Optional[str] = None
    country: Optional[str] = None
    native_language: Optional[str] = None
    english_level: Optional[str] = None
    target_country: Optional[str] = None
    budget_usd: Optional[int] = None
    preferred_study_language: Optional[str] = None
    interests: Optional[List[str]] = None
    about: Optional[str] = None


class ProfileOut(BaseModel):
    id: int
    user_id: int
    age: Optional[int]
    grade: Optional[int]
    city: Optional[str]
    country: Optional[str]
    native_language: Optional[str]
    english_level: Optional[str]
    target_country: Optional[str]
    budget_usd: Optional[int]
    preferred_study_language: Optional[str]
    interests: Optional[List[str]]
    about: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
