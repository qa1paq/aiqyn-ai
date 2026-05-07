from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.schemas.assessment import (
    AssessmentQuestion, AssessmentSubmit, AssessmentAnalyzeRequest, AssessmentResultOut
)
from app.services.auth_service import get_current_user
from app.services.assessment_service import AssessmentService
from app.services.gamification_service import GamificationService

router = APIRouter()


@router.get("/questions", response_model=List[AssessmentQuestion])
def get_questions(lang: str = Query(default="ru", regex="^(ru|en|kk)$")):
    return AssessmentService.get_questions(lang)


@router.post("/submit", response_model=AssessmentResultOut, status_code=status.HTTP_201_CREATED)
def submit_assessment(
    data: AssessmentSubmit,
    lang: str = Query(default="ru", regex="^(ru|en|kk)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = AssessmentService.save_result(db, current_user.id, data.answers, lang)
    answered_count = len(data.answers)
    GamificationService.award_xp(db, current_user.id, answered_count * 5, "assessment_answers")
    GamificationService.award_xp(db, current_user.id, 100, "assessment_completed")
    GamificationService.unlock_achievement(db, current_user.id, "CAREER_DISCOVERED")
    return result


@router.post("/analyze", response_model=AssessmentResultOut)
def analyze_assessment(
    data: AssessmentAnalyzeRequest,
    lang: str = Query(default="ru", regex="^(ru|en|kk)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AssessmentService.save_result(db, current_user.id, data.answers, lang)


@router.get("/result", response_model=AssessmentResultOut)
def get_result(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from app.models.assessment import AssessmentResult
    result = db.query(AssessmentResult).filter(
        AssessmentResult.user_id == current_user.id
    ).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Результат не найден. Сначала пройди тест.",
        )
    return result
