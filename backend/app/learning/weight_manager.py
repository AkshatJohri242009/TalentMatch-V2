from app.core.config import get_settings
from app.services.storage import JsonStorage


DEFAULT_WEIGHTS = {
    "skills": 0.4,
    "experience": 0.3,
    "role_similarity": 0.2,
    "education": 0.1,
}


class WeightManager:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.storage = JsonStorage()

    def load_weights(self) -> dict[str, float]:
        weights = self.storage.read_json(
            self.settings.learning_weights_path, default=DEFAULT_WEIGHTS
        )
        return self._normalize(weights)

    def save_weights(self, weights: dict[str, float]) -> dict[str, float]:
        normalized = self._normalize(weights)
        self.storage.write_json(self.settings.learning_weights_path, normalized)
        return normalized

    def _normalize(self, weights: dict[str, float]) -> dict[str, float]:
        merged = {**DEFAULT_WEIGHTS, **weights}
        total = sum(merged.values()) or 1.0
        return {key: round(value / total, 4) for key, value in merged.items()}
