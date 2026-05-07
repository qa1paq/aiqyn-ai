from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChoiceCreate(BaseModel):
    university_id: int
    major_id: Optional[int] = None
    status: str = "interested"


class ChoiceOut(BaseModel):
    id: int
    user_id: int
    university_id: int
    major_id: Optional[int]
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
