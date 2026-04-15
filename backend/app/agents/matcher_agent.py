from app.models.schemas import CandidateRead, JobMatchRequest, MatchBreakdown
from app.services.reasoning_service import get_reasoning_service
from app.services.vector_service import get_vector_service


class MatcherAgent:
    def __init__(self, learning_service) -> None:
        self.learning_service = learning_service
        self.vector_service = get_vector_service()
        self.reasoning_service = get_reasoning_service()

    def match(
        self,
        payload: JobMatchRequest,
        candidates: list[CandidateRead],
        plan: dict[str, object],
    ) -> list[MatchBreakdown]:
        weights = self.learning_service.get_weights()
        results: list[MatchBreakdown] = []
        required_skills = {skill.lower() for skill in payload.required_skills or []}
        if not required_skills:
            required_skills = {skill.lower() for skill in plan.get("focus_skills", [])}

        for candidate in candidates:
            candidate_skills = {skill.lower() for skill in candidate.skills}
            skill_score = (
                len(required_skills & candidate_skills) / len(required_skills)
                if required_skills
                else 0.5
            )
            experience_score = min(
                candidate.years_experience / max(payload.min_experience or 1, 1), 1.0
            )
            role_score = self.vector_service.cosine_similarity(
                payload.job_description,
                f"{candidate.current_title} {candidate.summary} {' '.join(candidate.skills)}",
            )
            education_score = 1.0 if (
                not payload.preferred_education
                or payload.preferred_education.lower()
                in candidate.education.degree.lower()
            ) else 0.3
            semantic_score = self.vector_service.cosine_similarity(
                payload.job_description, candidate.summary or candidate.current_title
            )
            weighted = (
                skill_score * weights["skills"]
                + experience_score * weights["experience"]
                + role_score * weights["role_similarity"]
                + education_score * weights["education"]
            )
            score = round(((weighted * 0.8) + (semantic_score * 0.2)) * 100, 2)
            results.append(
                MatchBreakdown(
                    candidate_id=candidate.id,
                    candidate_name=f"{candidate.first_name} {candidate.last_name}",
                    score=score,
                    weighted_score=round(weighted * 100, 2),
                    semantic_score=round(semantic_score * 100, 2),
                    skill_score=round(skill_score * 100, 2),
                    experience_score=round(experience_score * 100, 2),
                    role_score=round(role_score * 100, 2),
                    education_score=round(education_score * 100, 2),
                    explanation=self.reasoning_service.explain_match(
                        candidate_name=f"{candidate.first_name} {candidate.last_name}",
                        score=score,
                        feature_summary={
                            "skills": skill_score,
                            "experience": experience_score,
                            "role_similarity": role_score,
                            "education": education_score,
                            "semantic": semantic_score,
                        },
                    ),
                    features={
                        "skills": round(skill_score, 4),
                        "experience": round(experience_score, 4),
                        "role_similarity": round(role_score, 4),
                        "education": round(education_score, 4),
                        "semantic": round(semantic_score, 4),
                    },
                )
            )
        return sorted(results, key=lambda item: item.score, reverse=True)
