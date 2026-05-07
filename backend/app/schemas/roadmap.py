from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class RoadmapGenerateRequest(BaseModel):
    target_major: str
    target_country: str


class RoadmapStepOut(BaseModel):
    id: int
    roadmap_id: int
    month_number: int
    week_number: Optional[int]
    title: str
    description: Optional[str]
    tasks: Optional[List[str]]
    xp_reward: int
    is_completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class RoadmapOut(BaseModel):
    id: int
    user_id: int
    target_major: str
    target_country: str
    roadmap_title: str
    roadmap_summary: Optional[str]
    duration_months: int
    created_at: datetime
    updated_at: datetime
    steps: List[RoadmapStepOut] = []

    model_config = {"from_attributes": True}


class StepCompleteResponse(BaseModel):
    success: bool
    xp_earned: int
    total_xp: int
    level: int
    message: str
