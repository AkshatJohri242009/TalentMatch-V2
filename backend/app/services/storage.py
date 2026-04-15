import json
from datetime import datetime
from pathlib import Path
from typing import Any

from app.core.config import get_settings
from app.models.schemas import CandidateCreate, CandidateRead


class JsonStorage:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.settings.candidate_seed_path.parent.mkdir(parents=True, exist_ok=True)

    def load_candidates(self) -> list[CandidateRead]:
        path = self.settings.candidate_seed_path
        if not path.exists():
            return []
        payload = json.loads(path.read_text(encoding="utf-8"))
        return [CandidateRead(**item) for item in payload]

    def save_candidates(self, candidates: list[CandidateRead]) -> None:
        path = self.settings.candidate_seed_path
        serializable = [candidate.model_dump(mode="json") for candidate in candidates]
        path.write_text(json.dumps(serializable, indent=2), encoding="utf-8")

    def create_candidate_id(self, existing: list[CandidateRead]) -> str:
        return f"CAND{len(existing) + 1:03d}"

    def build_candidate(self, payload: CandidateCreate) -> CandidateRead:
        candidates = self.load_candidates()
        candidate_id = payload.id or self.create_candidate_id(candidates)
        return CandidateRead(
            **payload.model_dump(exclude={"id", "last_updated"}),
            id=candidate_id,
            last_updated=payload.last_updated or datetime.utcnow(),
        )

    def read_json(self, path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))

    def write_json(self, path: Path, payload: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
