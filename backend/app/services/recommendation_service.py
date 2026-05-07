from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.university import University, Major
from app.models.assessment import AssessmentResult
from app.models.profile import Profile


class RecommendationService:
    @staticmethod
    def get_recommended_universities(
        db: Session,
        user_id: int,
        limit: int = 20,
    ) -> List[University]:
        assessment = db.query(AssessmentResult).filter(AssessmentResult.user_id == user_id).first()
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()

        query = db.query(University)
        results = query.all()

        if not assessment and not profile:
            return results[:limit]

        def score_university(uni: University) -> int:
            score = 0
            if profile:
                if profile.target_country and uni.country.lower() == profile.target_country.lower():
                    score += 50
                if profile.budget_usd:
                    if uni.tuition_min_usd and uni.tuition_min_usd <= profile.budget_usd:
                        score += 30
            if assessment and uni.majors:
                top_cats = assessment.top_categories or []
                for major in uni.majors:
                    if major.category in top_cats:
                        score += 20
                        break
                if profile and profile.preferred_study_language:
                    for major in uni.majors:
                        if major.language.lower() == profile.preferred_study_language.lower():
                            score += 10
                            break
            if uni.ranking:
                score += max(0, 10 - uni.ranking // 100)
            return score

        ranked = sorted(results, key=score_university, reverse=True)
        return ranked[:limit]

    @staticmethod
    def get_recommended_majors(db: Session, user_id: int) -> List[Major]:
        assessment = db.query(AssessmentResult).filter(AssessmentResult.user_id == user_id).first()
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()

        if not assessment:
            return db.query(Major).limit(20).all()

        top_cats = assessment.top_categories or []
        query = db.query(Major).filter(Major.category.in_(top_cats))

        if profile and profile.budget_usd:
            query = query.filter(
                (Major.tuition_usd == None) | (Major.tuition_usd <= profile.budget_usd)
            )
        if profile and profile.preferred_study_language:
            query = query.filter(Major.language == profile.preferred_study_language)

        return query.limit(30).all()
