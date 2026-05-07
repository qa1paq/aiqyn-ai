from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.choice import UserUniversityChoice
from app.schemas.choice import ChoiceCreate, ChoiceOut
from app.services.auth_service import get_current_user
from app.services.gamification_service import GamificationService

router = APIRouter()


@router.post("/university", response_model=ChoiceOut, status_code=status.HTTP_201_CREATED)
def choose_university(
    data: ChoiceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = db.query(UserUniversityChoice).filter(
        UserUniversityChoice.user_id == current_user.id,
        UserUniversityChoice.university_id == data.university_id,
        UserUniversityChoice.major_id == data.major_id,
    ).first()
    if existing:
        existing.status = data.status
        db.commit()
        db.refresh(existing)
        return existing

    choice = UserUniversityChoice(
        user_id=current_user.id,
        university_id=data.university_id,
        major_id=data.major_id,
        status=data.status,
    )
    db.add(choice)
    db.commit()
    db.refresh(choice)

    GamificationService.award_xp(db, current_user.id, 100, "university_chosen")
    GamificationService.unlock_achievement(db, current_user.id, "UNIVERSITY_PICKED")
    return choice


@router.get("/me", response_model=List[ChoiceOut])
def get_my_choices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(UserUniversityChoice).filter(
        UserUniversityChoice.user_id == current_user.id
    ).all()
