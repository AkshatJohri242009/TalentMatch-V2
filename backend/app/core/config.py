from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = BASE_DIR.parent
DATA_DIR = PROJECT_DIR / "data"


class Settings(BaseSettings):
    app_name: str = "TalentMatch AI"
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )
    database_url: str = f"sqlite:///{(DATA_DIR / 'talentmatch.db').as_posix()}"
    candidate_seed_path: Path = DATA_DIR / "mock_candidates.json"
    learning_weights_path: Path = PROJECT_DIR / "learning_weights.json"
    learning_feedback_path: Path = DATA_DIR / "learning_feedback.json"
    vector_index_path: Path = DATA_DIR / "vector_index.json"
    use_database: bool = False
    use_langchain: bool = False
    use_vector_index: bool = True
    llm_provider: str = "fallback"
    llm_model: str = "deterministic"
    model_config = SettingsConfigDict(
        env_prefix="TALENTMATCH_",
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return settings
