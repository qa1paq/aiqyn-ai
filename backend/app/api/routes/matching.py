from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.schemas.matching import MatchUserOut, MatchActionRequest, MatchActionResponse
from app.services.auth_service import get_current_user
from app.services.matching_service import MatchingService
from app.services.gamification_service import GamificationService
from app.models.match import MatchAction

router = APIRouter()


@router.get("/feed", response_model=List[MatchUserOut])
def get_matching_feed(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return MatchingService.get_feed(db, current_user.id, limit=limit)


@router.post("/action", response_model=MatchActionResponse)
def perform_match_action(
    data: MatchActionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.action not in ("like", "skip"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Action must be 'like' or 'skip'",
        )
    if data.target_user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot perform action on yourself",
        )
    MatchingService.record_action(db, current_user.id, data.target_user_id, data.action)

    is_first_action = db.query(MatchAction).filter(
        MatchAction.user_id == current_user.id
    ).count() == 1

    xp_earned = 0
    if is_first_action:
        GamificationService.award_xp(db, current_user.id, 30, "first_match_action")
        GamificationService.unlock_achievement(db, current_user.id, "FIRST_MATCH")
        xp_earned = 30

    return MatchActionResponse(success=True, action=data.action, xp_earned=xp_earned)
