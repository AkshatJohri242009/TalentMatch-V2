from app.core.config import get_settings
from app.models.schemas import FeedbackCreate
from app.services.storage import JsonStorage


class FeedbackStore:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.storage = JsonStorage()

    def store_feedback(self, payload: FeedbackCreate) -> None:
        entries = self.storage.read_json(self.settings.learning_feedback_path, default=[])
        entries.append(payload.model_dump(mode="json"))
        self.storage.write_json(self.settings.learning_feedback_path, entries)

    def load_feedback(self) -> list[dict]:
        return self.storage.read_json(self.settings.learning_feedback_path, default=[])
