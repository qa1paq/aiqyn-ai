from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.schemas.roadmap import RoadmapGenerateRequest, RoadmapOut, StepCompleteResponse
from app.services.auth_service import get_current_user
from app.services.roadmap_service import RoadmapService

router = APIRouter()


@router.post("/generate", response_model=RoadmapOut, status_code=status.HTTP_201_CREATED)
def generate_roadmap(
    data: RoadmapGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    roadmap = RoadmapService.generate(db, current_user.id, data.target_major, data.target_country)
    return roadmap


@router.get("/me", response_model=RoadmapOut)
def get_my_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    roadmap = RoadmapService.get_latest(db, current_user.id)
    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No roadmap found. Generate one first!",
        )
    return roadmap


@router.post("/steps/{step_id}/complete", response_model=StepCompleteResponse)
def complete_step(
    step_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = RoadmapService.complete_step(db, current_user.id, step_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.get("/daily-tasks")
def get_daily_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tasks = RoadmapService.get_daily_tasks(db, current_user.id)
    return {"tasks": tasks}
