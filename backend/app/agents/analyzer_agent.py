from app.models.schemas import JobMatchRequest
from app.services.reasoning_service import get_reasoning_service


class AnalyzerAgent:
    def __init__(self) -> None:
        self.reasoning_service = get_reasoning_service()

    def analyze(self, payload: JobMatchRequest) -> dict[str, object]:
        text = payload.job_description.lower()
        inferred_skills = list(payload.required_skills)
        for skill in [
            "python",
            "react",
            "fastapi",
            "sql",
            "postgresql",
            "aws",
            "docker",
            "langchain",
        ]:
            if skill in text and skill.title() not in inferred_skills:
                inferred_skills.append(skill.title())
        enriched = self.reasoning_service.enrich_analysis(
            payload.job_description, inferred_skills
        )
        return {
            "required_skills": enriched["skills"],
            "min_experience": payload.min_experience,
            "preferred_education": payload.preferred_education,
            "analysis_summary": enriched["summary"],
        }
