from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class MajorOut(BaseModel):
    id: int
    university_id: int
    name: str
    category: str
    degree_level: str
    language: str
    tuition_usd: Optional[int]
    duration_years: Optional[float]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UniversityOut(BaseModel):
    id: int
    name: str
    country: str
    city: str
    website: Optional[str]
    description: Optional[str]
    ranking: Optional[int]
    tuition_min_usd: Optional[int]
    tuition_max_usd: Optional[int]
    created_at: datetime
    updated_at: datetime
    majors: List[MajorOut] = []

    model_config = {"from_attributes": True}


class UniversityListOut(BaseModel):
    id: int
    name: str
    country: str
    city: str
    ranking: Optional[int]
    tuition_min_usd: Optional[int]
    tuition_max_usd: Optional[int]

    model_config = {"from_attributes": True}
