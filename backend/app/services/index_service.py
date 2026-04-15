from __future__ import annotations

from functools import lru_cache

from app.core.config import get_settings
from app.models.schemas import CandidateRead
from app.services.storage import JsonStorage
from app.services.vector_service import get_vector_service

try:  # Optional FAISS support
    import faiss  # type: ignore
except ImportError:  # pragma: no cover
    faiss = None


class IndexService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.storage = JsonStorage()
        self.vector_service = get_vector_service()

    def rebuild(self, candidates: list[CandidateRead]) -> None:
        records = []
        for candidate in candidates:
            text = self._candidate_text(candidate)
            records.append(
                {
                    "candidate_id": candidate.id,
                    "text": text,
                    "tokens": dict(self.vector_service.embed_text(text)),
                }
            )
        self.storage.write_json(self.settings.vector_index_path, records)

    def semantic_search(
        self, query: str, candidates: list[CandidateRead], top_k: int = 5
    ) -> list[CandidateRead]:
        if self.settings.use_vector_index:
            self.rebuild(candidates)
        scored = sorted(
            candidates,
            key=lambda candidate: self.vector_service.cosine_similarity(
                query, self._candidate_text(candidate)
            ),
            reverse=True,
        )
        return scored[:top_k]

    def _candidate_text(self, candidate: CandidateRead) -> str:
        return (
            f"{candidate.current_title} {candidate.summary} "
            f"{' '.join(candidate.skills)} {candidate.education.degree}"
        )


@lru_cache
def get_index_service() -> IndexService:
    return IndexService()
