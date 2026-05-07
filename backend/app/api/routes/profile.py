from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.database import get_db
from app.models.user import User
from app.models.profile import Profile
from app.schemas.profile import ProfileUpdate, ProfileOut
from app.services.auth_service import get_current_user
from app.services.gamification_service import GamificationService

router = APIRouter()


def get_or_create_profile(db: Session, user_id: int) -> Profile:
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        profile = Profile(user_id=user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.get("/me", response_model=ProfileOut)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_or_create_profile(db, current_user.id)


@router.put("/me", response_model=ProfileOut)
def update_my_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_or_create_profile(db, current_user.id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    profile.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(profile)

    required_fields = ["age", "country", "english_level", "target_country"]
    is_complete = all(getattr(profile, f) is not None for f in required_fields)
    if is_complete:
        GamificationService.award_xp(db, current_user.id, 50, "profile_completed")
        GamificationService.unlock_achievement(db, current_user.id, "PROFILE_READY")

    return profile
