# Import all models here so SQLAlchemy resolves all relationship references
# whenever any model is used. This prevents "failed to locate name" errors.
from app.models.user import User
from app.models.profile import Profile
from app.models.assessment import AssessmentResult
from app.models.university import University, Major
from app.models.choice import UserUniversityChoice
from app.models.match import MatchAction
from app.models.roadmap import Roadmap, RoadmapStep
from app.models.gamification import UserGamification, Achievement, UserAchievement

__all__ = [
    "User", "Profile", "AssessmentResult",
    "University", "Major",
    "UserUniversityChoice",
    "MatchAction",
    "Roadmap", "RoadmapStep",
    "UserGamification", "Achievement", "UserAchievement",
]
