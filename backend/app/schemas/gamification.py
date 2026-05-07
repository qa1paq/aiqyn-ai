from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List


class GamificationOut(BaseModel):
    id: int
    user_id: int
    total_xp: int
    level: int
    current_streak: int
    longest_streak: int
    last_active_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AchievementOut(BaseModel):
    id: int
    code: str
    title: str
    description: Optional[str]
    xp_reward: int
    unlocked: bool = False
    unlocked_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class DailyCheckinResponse(BaseModel):
    xp_earned: int
    total_xp: int
    level: int
    current_streak: int
    message: str
