from sqlalchemy.orm import Session
from datetime import date, datetime, timezone
from typing import Optional

from app.models.gamification import UserGamification, Achievement, UserAchievement

LEVEL_THRESHOLDS = [
    (1, 0, "New Applicant"),
    (2, 100, "Explorer"),
    (3, 300, "Career Finder"),
    (4, 600, "University Hunter"),
    (5, 1000, "Future Student"),
    (6, 1500, "Global Applicant"),
]

ACHIEVEMENTS_DATA = [
    {"code": "FIRST_STEP", "title": "First Step", "description": "Completed registration", "xp_reward": 20},
    {"code": "PROFILE_READY", "title": "Profile Ready", "description": "Completed your profile", "xp_reward": 50},
    {"code": "CAREER_DISCOVERED", "title": "Career Discovered", "description": "Completed career assessment", "xp_reward": 100},
    {"code": "UNIVERSITY_PICKED", "title": "University Picked", "description": "Selected a university", "xp_reward": 100},
    {"code": "ROADMAP_STARTED", "title": "Roadmap Started", "description": "Generated your admission roadmap", "xp_reward": 100},
    {"code": "FIRST_TASK_DONE", "title": "First Task Done", "description": "Completed your first roadmap task", "xp_reward": 50},
    {"code": "FIRST_MATCH", "title": "First Match", "description": "First like or skip in matching", "xp_reward": 30},
]


class GamificationService:
    @staticmethod
    def initialize_user(db: Session, user_id: int) -> UserGamification:
        existing = db.query(UserGamification).filter(UserGamification.user_id == user_id).first()
        if existing:
            return existing
        gamification = UserGamification(user_id=user_id, total_xp=0, level=1)
        db.add(gamification)
        db.commit()
        db.refresh(gamification)
        return gamification

    @staticmethod
    def get_level_for_xp(xp: int) -> tuple[int, str]:
        level, name = 1, "New Applicant"
        for lvl, threshold, title in LEVEL_THRESHOLDS:
            if xp >= threshold:
                level, name = lvl, title
        return level, name

    @staticmethod
    def award_xp(db: Session, user_id: int, amount: int, reason: str = "") -> UserGamification:
        gamification = db.query(UserGamification).filter(UserGamification.user_id == user_id).first()
        if not gamification:
            gamification = GamificationService.initialize_user(db, user_id)
        gamification.total_xp = (gamification.total_xp or 0) + amount
        level, _ = GamificationService.get_level_for_xp(gamification.total_xp)
        gamification.level = level
        gamification.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(gamification)
        return gamification

    @staticmethod
    def unlock_achievement(db: Session, user_id: int, achievement_code: str) -> Optional[UserAchievement]:
        achievement = db.query(Achievement).filter(Achievement.code == achievement_code).first()
        if not achievement:
            return None
        existing = db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == achievement.id,
        ).first()
        if existing:
            return existing
        ua = UserAchievement(user_id=user_id, achievement_id=achievement.id)
        db.add(ua)
        if achievement.xp_reward:
            GamificationService.award_xp(db, user_id, achievement.xp_reward, f"achievement:{achievement_code}")
        db.commit()
        db.refresh(ua)
        return ua

    @staticmethod
    def daily_checkin(db: Session, user_id: int) -> dict:
        gamification = db.query(UserGamification).filter(UserGamification.user_id == user_id).first()
        if not gamification:
            gamification = GamificationService.initialize_user(db, user_id)
        today = date.today()
        last = gamification.last_active_date
        xp_earned = 0
        if last is None or last < today:
            xp_earned = 15
            if last is not None and (today - last).days == 1:
                gamification.current_streak = (gamification.current_streak or 0) + 1
            elif last is None or (today - last).days > 1:
                gamification.current_streak = 1
            if gamification.current_streak > (gamification.longest_streak or 0):
                gamification.longest_streak = gamification.current_streak
            gamification.last_active_date = today
            gamification.total_xp = (gamification.total_xp or 0) + xp_earned
            level, _ = GamificationService.get_level_for_xp(gamification.total_xp)
            gamification.level = level
            gamification.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(gamification)
            msg = f"Day {gamification.current_streak} streak! Keep going!"
        else:
            msg = "Already checked in today. Come back tomorrow!"
        return {
            "xp_earned": xp_earned,
            "total_xp": gamification.total_xp,
            "level": gamification.level,
            "current_streak": gamification.current_streak,
            "message": msg,
        }

    @staticmethod
    def seed_achievements(db: Session) -> None:
        for data in ACHIEVEMENTS_DATA:
            existing = db.query(Achievement).filter(Achievement.code == data["code"]).first()
            if not existing:
                db.add(Achievement(**data))
        db.commit()
