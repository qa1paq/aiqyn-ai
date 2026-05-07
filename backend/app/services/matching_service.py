from sqlalchemy.orm import Session
from typing import List
from app.models.user import User
from app.models.profile import Profile
from app.models.assessment import AssessmentResult
from app.models.choice import UserUniversityChoice
from app.models.match import MatchAction
from app.schemas.matching import MatchUserOut


class MatchingService:
    @staticmethod
    def calculate_match_score(
        current_user_id: int,
        target_user_id: int,
        db: Session,
    ) -> int:
        score = 0
        my_choices = db.query(UserUniversityChoice).filter(
            UserUniversityChoice.user_id == current_user_id
        ).all()
        their_choices = db.query(UserUniversityChoice).filter(
            UserUniversityChoice.user_id == target_user_id
        ).all()

        my_uni_ids = {c.university_id for c in my_choices}
        my_major_ids = {c.major_id for c in my_choices if c.major_id}
        their_uni_ids = {c.university_id for c in their_choices}
        their_major_ids = {c.major_id for c in their_choices if c.major_id}

        if my_uni_ids & their_uni_ids:
            score += 50
        if my_major_ids & their_major_ids:
            score += 30

        my_assessment = db.query(AssessmentResult).filter(
            AssessmentResult.user_id == current_user_id
        ).first()
        their_assessment = db.query(AssessmentResult).filter(
            AssessmentResult.user_id == target_user_id
        ).first()

        if my_assessment and their_assessment:
            my_cats = set(my_assessment.top_categories or [])
            their_cats = set(their_assessment.top_categories or [])
            if my_cats & their_cats:
                score += 20

        my_profile = db.query(Profile).filter(Profile.user_id == current_user_id).first()
        their_profile = db.query(Profile).filter(Profile.user_id == target_user_id).first()

        if my_profile and their_profile:
            if my_profile.target_country and my_profile.target_country == their_profile.target_country:
                score += 15
            if (my_profile.budget_usd and their_profile.budget_usd and
                    abs(my_profile.budget_usd - their_profile.budget_usd) <= 5000):
                score += 10
            if (my_profile.preferred_study_language and
                    my_profile.preferred_study_language == their_profile.preferred_study_language):
                score += 10
            if (my_profile.city and my_profile.city == their_profile.city) or \
               (my_profile.country and my_profile.country == their_profile.country):
                score += 5

        return score

    @staticmethod
    def get_feed(db: Session, current_user_id: int, limit: int = 20) -> List[MatchUserOut]:
        acted_ids = {
            row.target_user_id
            for row in db.query(MatchAction).filter(MatchAction.user_id == current_user_id).all()
        }
        acted_ids.add(current_user_id)

        candidates = db.query(User).filter(User.id.notin_(acted_ids)).limit(100).all()

        results = []
        for candidate in candidates:
            score = MatchingService.calculate_match_score(current_user_id, candidate.id, db)
            profile = db.query(Profile).filter(Profile.user_id == candidate.id).first()
            assessment = db.query(AssessmentResult).filter(
                AssessmentResult.user_id == candidate.id
            ).first()
            results.append(MatchUserOut(
                user_id=candidate.id,
                full_name=candidate.full_name,
                city=profile.city if profile else None,
                country=profile.country if profile else None,
                target_country=profile.target_country if profile else None,
                english_level=profile.english_level if profile else None,
                match_score=score,
                top_categories=assessment.top_categories if assessment else None,
                recommended_majors=assessment.recommended_majors[:2] if assessment else None,
            ))

        results.sort(key=lambda x: x.match_score, reverse=True)
        return results[:limit]

    @staticmethod
    def record_action(db: Session, user_id: int, target_user_id: int, action: str) -> MatchAction:
        existing = db.query(MatchAction).filter(
            MatchAction.user_id == user_id,
            MatchAction.target_user_id == target_user_id,
        ).first()
        if existing:
            existing.action = action
            db.commit()
            db.refresh(existing)
            return existing
        score = MatchingService.calculate_match_score(user_id, target_user_id, db)
        match_action = MatchAction(
            user_id=user_id,
            target_user_id=target_user_id,
            action=action,
            match_score=score,
        )
        db.add(match_action)
        db.commit()
        db.refresh(match_action)
        return match_action
