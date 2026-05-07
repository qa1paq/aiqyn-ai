from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.roadmap import Roadmap, RoadmapStep
from app.models.assessment import AssessmentResult
from app.models.profile import Profile
from app.services.ai_service import get_ai_service
from app.services.gamification_service import GamificationService


class RoadmapService:
    @staticmethod
    def generate(db: Session, user_id: int, target_major: str, target_country: str) -> Roadmap:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        assessment = db.query(AssessmentResult).filter(AssessmentResult.user_id == user_id).first()

        ai = get_ai_service()
        ai_data = {
            "target_major": target_major,
            "target_country": target_country,
            "english_level": profile.english_level if profile else "B1",
            "budget_usd": profile.budget_usd if profile else 15000,
            "top_categories": assessment.top_categories if assessment else [],
            "recommended_majors": assessment.recommended_majors if assessment else [],
            "full_name": "",
        }

        roadmap_data = ai.generate_admission_roadmap(ai_data)

        existing = db.query(Roadmap).filter(
            Roadmap.user_id == user_id,
            Roadmap.target_major == target_major,
        ).first()
        if existing:
            for step in existing.steps:
                db.delete(step)
            db.delete(existing)
            db.commit()

        roadmap = Roadmap(
            user_id=user_id,
            target_major=target_major,
            target_country=target_country,
            roadmap_title=roadmap_data["title"],
            roadmap_summary=roadmap_data["summary"],
            duration_months=roadmap_data["duration_months"],
        )
        db.add(roadmap)
        db.flush()

        for month in roadmap_data["months"]:
            step = RoadmapStep(
                roadmap_id=roadmap.id,
                month_number=month["month_number"],
                week_number=None,
                title=month["title"],
                description=month["description"],
                tasks=month["tasks"],
                xp_reward=month["xp_reward"],
                is_completed=False,
            )
            db.add(step)

        db.commit()
        db.refresh(roadmap)

        GamificationService.award_xp(db, user_id, 100, "roadmap_generated")
        GamificationService.unlock_achievement(db, user_id, "ROADMAP_STARTED")
        return roadmap

    @staticmethod
    def get_latest(db: Session, user_id: int) -> Optional[Roadmap]:
        return (
            db.query(Roadmap)
            .filter(Roadmap.user_id == user_id)
            .order_by(Roadmap.created_at.desc())
            .first()
        )

    @staticmethod
    def complete_step(db: Session, user_id: int, step_id: int) -> dict:
        step = db.query(RoadmapStep).filter(RoadmapStep.id == step_id).first()
        if not step:
            return {"success": False, "xp_earned": 0, "message": "Step not found"}

        roadmap = db.query(Roadmap).filter(Roadmap.id == step.roadmap_id).first()
        if not roadmap or roadmap.user_id != user_id:
            return {"success": False, "xp_earned": 0, "message": "Not authorized"}

        if step.is_completed:
            return {"success": False, "xp_earned": 0, "message": "Step already completed"}

        step.is_completed = True
        db.commit()

        xp = step.xp_reward or 50
        gamification = GamificationService.award_xp(db, user_id, xp, "roadmap_step_completed")
        GamificationService.unlock_achievement(db, user_id, "FIRST_TASK_DONE")

        return {
            "success": True,
            "xp_earned": xp,
            "total_xp": gamification.total_xp,
            "level": gamification.level,
            "message": f"Step completed! +{xp} XP earned. Keep going!",
        }

    @staticmethod
    def get_daily_tasks(db: Session, user_id: int) -> List[dict]:
        roadmap = RoadmapService.get_latest(db, user_id)
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        ai = get_ai_service()

        current_major = roadmap.target_major if roadmap else "your field"
        ai_data = {
            "target_major": current_major,
            "english_level": profile.english_level if profile else "B1",
        }
        return ai.generate_daily_tasks(ai_data)
