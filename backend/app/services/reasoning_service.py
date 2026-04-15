from __future__ import annotations

from functools import lru_cache

from app.core.config import get_settings

try:  # Optional LangChain integration
    from langchain_core.prompts import ChatPromptTemplate
except ImportError:  # pragma: no cover
    ChatPromptTemplate = None


class ReasoningService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def enrich_analysis(self, job_description: str, skills: list[str]) -> dict[str, object]:
        if self.settings.use_langchain and ChatPromptTemplate is not None:
            prompt = ChatPromptTemplate.from_template(
                "Summarize the role and return the strongest skills for: {job_description}"
            )
            messages = prompt.format_messages(job_description=job_description)
            synthesized = " ".join(getattr(message, "content", "") for message in messages)
            inferred = list(dict.fromkeys(skills + self._extract_keywords(synthesized)))
            return {"skills": inferred, "summary": synthesized}
        return {
            "skills": list(dict.fromkeys(skills + self._extract_keywords(job_description))),
            "summary": job_description[:300],
        }

    def explain_match(
        self, candidate_name: str, score: float, feature_summary: dict[str, float]
    ) -> str:
        strongest_feature = max(feature_summary, key=feature_summary.get)
        if self.settings.use_langchain and ChatPromptTemplate is not None:
            prompt = ChatPromptTemplate.from_template(
                "Explain why {candidate_name} received {score}% match with strongest factor {feature}."
            )
            messages = prompt.format_messages(
                candidate_name=candidate_name,
                score=score,
                feature=strongest_feature,
            )
            explanation = " ".join(getattr(message, "content", "") for message in messages)
            return explanation[:240]
        return (
            f"{candidate_name} scored {score}% with strongest alignment in "
            f"{strongest_feature.replace('_', ' ')}."
        )

    def _extract_keywords(self, text: str) -> list[str]:
        keywords: list[str] = []
        known = [
            "Python",
            "FastAPI",
            "React",
            "SQL",
            "PostgreSQL",
            "Docker",
            "LangChain",
            "FAISS",
            "AWS",
            "Machine Learning",
        ]
        lowered = text.lower()
        for skill in known:
            if skill.lower() in lowered:
                keywords.append(skill)
        return keywords


@lru_cache
def get_reasoning_service() -> ReasoningService:
    return ReasoningService()
