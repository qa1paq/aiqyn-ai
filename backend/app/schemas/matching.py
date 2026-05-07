from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class MatchUserOut(BaseModel):
    user_id: int
    full_name: str
    city: Optional[str]
    country: Optional[str]
    target_country: Optional[str]
    english_level: Optional[str]
    match_score: int
    top_categories: Optional[List[str]]
    recommended_majors: Optional[List[str]]


class MatchActionRequest(BaseModel):
    target_user_id: int
    action: str  # like, skip


class MatchActionResponse(BaseModel):
    success: bool
    action: str
    xp_earned: int = 0
