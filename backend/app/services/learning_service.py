from functools import lru_cache

from app.learning.feedback_store import FeedbackStore
from app.learning.learning_engine import LearningEngine
from app.learning.weight_manager import WeightManager
from app.models.schemas import FeedbackCreate


class LearningService:
    def __init__(self) -> None:
        self.weight_manager = WeightManager()
        self.feedback_store = FeedbackStore()
        self.learning_engine = LearningEngine(self.weight_manager, self.feedback_store)

    def get_weights(self) -> dict[str, float]:
        return self.weight_manager.load_weights()

    def record_feedback(self, payload: FeedbackCreate) -> None:
        self.feedback_store.store_feedback(payload)
        self.learning_engine.update_weights()


@lru_cache
def get_learning_service() -> LearningService:
    return LearningService()
