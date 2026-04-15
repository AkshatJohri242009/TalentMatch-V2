import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import get_settings  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def reset_storage():
    settings = get_settings()
    settings.candidate_seed_path.write_text("[]", encoding="utf-8")
    settings.learning_feedback_path.write_text("[]", encoding="utf-8")
    if settings.learning_weights_path.exists():
        settings.learning_weights_path.write_text("{}", encoding="utf-8")
    if settings.vector_index_path.exists():
        settings.vector_index_path.write_text("[]", encoding="utf-8")
    yield


@pytest.fixture
def client():
    return TestClient(app)
