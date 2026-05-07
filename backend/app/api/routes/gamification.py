from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.gamification import UserGamification, Achievement, UserAchievement
from app.schemas.gamification import GamificationOut, AchievementOut, DailyCheckinResponse
from app.services.auth_service import get_current_user
from app.services.gamification_service import GamificationService

router = APIRouter()


@router.get("/me", response_model=GamificationOut)
def get_my_gamification(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    gamification = db.query(UserGamification).filter(
        UserGamification.user_id == current_user.id
    ).first()
    if not gamification:
        gamification = GamificationService.initialize_user(db, current_user.id)
    return gamification


@router.get("/achievements", response_model=List[AchievementOut])
def get_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    all_achievements = db.query(Achievement).all()
    unlocked_map = {
        ua.achievement_id: ua.unlocked_at
        for ua in db.query(UserAchievement).filter(
            UserAchievement.user_id == current_user.id
        ).all()
    }
    result = []
    for ach in all_achievements:
        out = AchievementOut(
            id=ach.id,
            code=ach.code,
            title=ach.title,
            description=ach.description,
            xp_reward=ach.xp_reward or 0,
            unlocked=ach.id in unlocked_map,
            unlocked_at=unlocked_map.get(ach.id),
        )
        result.append(out)
    return result


@router.post("/daily-checkin", response_model=DailyCheckinResponse)
def daily_checkin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = GamificationService.daily_checkin(db, current_user.id)
    return DailyCheckinResponse(**result)
