from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.university import University
from app.schemas.university import UniversityOut, UniversityListOut, MajorOut
from app.services.auth_service import get_current_user
from app.services.recommendation_service import RecommendationService
from app.services.gamification_service import GamificationService

router = APIRouter()


@router.get("/universities", response_model=List[UniversityListOut])
def list_universities(
    country: str = None,
    db: Session = Depends(get_db),
):
    query = db.query(University)
    if country:
        query = query.filter(University.country.ilike(f"%{country}%"))
    return query.order_by(University.ranking).all()


@router.get("/universities/{university_id}", response_model=UniversityOut)
def get_university(
    university_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    university = db.query(University).filter(University.id == university_id).first()
    if not university:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="University not found")
    GamificationService.award_xp(db, current_user.id, 10, "university_viewed")
    return university


@router.get("/majors/recommended", response_model=List[MajorOut])
def get_recommended_majors(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RecommendationService.get_recommended_majors(db, current_user.id)
