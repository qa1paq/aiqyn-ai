from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class AssessmentOption(BaseModel):
    value: str
    label: str
    weights: Dict[str, int]


class AssessmentQuestion(BaseModel):
    question_key: str
    text: str
    options: List[AssessmentOption]


class AssessmentSubmit(BaseModel):
    answers: Dict[str, str]  # {"q1": "a", "q2": "c", ...}


class AssessmentAnalyzeRequest(BaseModel):
    answers: Dict[str, str]


class AssessmentResultOut(BaseModel):
    id: int
    user_id: int
    raw_scores: Dict[str, float]
    normalized_scores: Dict[str, float]
    top_categories: List[str]
    recommended_majors: List[str]
    profile_summary: Optional[str]
    answers: Dict[str, str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
