from functools import lru_cache

from app.models.schemas import CandidateCreate, CandidateRead
from app.services.database_service import DatabaseService
from app.services.index_service import get_index_service
from app.services.storage import JsonStorage


class CandidateService:
    def __init__(self) -> None:
        self.storage = JsonStorage()
        self.database = DatabaseService()
        self.index_service = get_index_service()

    def list_candidates(self) -> list[CandidateRead]:
        if self.database.is_available():
            items = self.database.list_candidates()
            if items:
                return items
        return self.storage.load_candidates()

    def create_candidate(self, payload: CandidateCreate) -> CandidateRead:
        if self.database.is_available():
            candidate = self.database.create_candidate(payload)
            candidates = self.database.list_candidates()
        else:
            candidate = self.storage.build_candidate(payload)
            candidates = self.storage.load_candidates()
            candidates.append(candidate)
            self.storage.save_candidates(candidates)
        self.index_service.rebuild(candidates)
        return candidate

    def search_candidates(
        self, query: str | None, skills: list[str], min_experience: int | None
    ) -> list[CandidateRead]:
        items = self.storage.load_candidates()
        normalized_skills = {skill.lower() for skill in skills}
        results: list[CandidateRead] = []
        for candidate in items:
            haystack = " ".join(
                [
                    candidate.first_name,
                    candidate.last_name,
                    candidate.current_title,
                    candidate.summary,
                    " ".join(candidate.skills),
                ]
            ).lower()
            if query and query.lower() not in haystack:
                continue
            if normalized_skills and not normalized_skills.issubset(
                {skill.lower() for skill in candidate.skills}
            ):
                continue
            if min_experience is not None and candidate.years_experience < min_experience:
                continue
            results.append(candidate)
        return results

    def semantic_search(self, query: str, top_k: int = 5) -> list[CandidateRead]:
        items = self.list_candidates()
        return self.index_service.semantic_search(query=query, candidates=items, top_k=top_k)


@lru_cache
def get_candidate_service() -> CandidateService:
    return CandidateService()
