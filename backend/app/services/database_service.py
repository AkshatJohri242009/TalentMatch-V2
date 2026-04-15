from __future__ import annotations

import sqlite3
from datetime import datetime
import json

from app.core.config import get_settings
from app.models.schemas import CandidateCreate, CandidateRead, Education

try:  # Optional PostgreSQL path
    from sqlalchemy import create_engine, text
except ImportError:  # pragma: no cover
    create_engine = None
    text = None


class DatabaseService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def is_available(self) -> bool:
        if not self.settings.use_database:
            return False
        database_url = self.settings.database_url
        if database_url.startswith("sqlite:///"):
            return True
        return create_engine is not None and database_url.startswith("postgresql")

    def initialize(self) -> None:
        database_url = self.settings.database_url
        if database_url.startswith("sqlite:///"):
            self._initialize_sqlite()
        elif self.is_available():
            self._initialize_postgres()

    def list_candidates(self) -> list[CandidateRead]:
        database_url = self.settings.database_url
        if database_url.startswith("sqlite:///"):
            return self._list_candidates_sqlite()
        if self.is_available():
            return self._list_candidates_postgres()
        return []

    def create_candidate(self, payload: CandidateCreate) -> CandidateRead:
        database_url = self.settings.database_url
        if database_url.startswith("sqlite:///"):
            return self._create_candidate_sqlite(payload)
        if self.is_available():
            return self._create_candidate_postgres(payload)
        raise RuntimeError("Database backend is not available.")

    def _sqlite_path(self) -> str:
        return self.settings.database_url.replace("sqlite:///", "", 1)

    def _initialize_sqlite(self) -> None:
        with sqlite3.connect(self._sqlite_path()) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS candidates (
                    id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT,
                    location TEXT,
                    current_title TEXT,
                    years_experience INTEGER,
                    education_json TEXT,
                    skills_json TEXT,
                    source TEXT,
                    open_to_work INTEGER,
                    summary TEXT,
                    last_updated TEXT
                )
                """
            )
            connection.commit()

    def _list_candidates_sqlite(self) -> list[CandidateRead]:
        self._initialize_sqlite()
        with sqlite3.connect(self._sqlite_path()) as connection:
            rows = connection.execute("SELECT * FROM candidates").fetchall()
        return [self._row_to_candidate_sqlite(row) for row in rows]

    def _create_candidate_sqlite(self, payload: CandidateCreate) -> CandidateRead:
        self._initialize_sqlite()
        existing = self._list_candidates_sqlite()
        candidate = CandidateRead(
            **payload.model_dump(exclude={"id", "last_updated"}),
            id=payload.id or f"CAND{len(existing) + 1:03d}",
            last_updated=payload.last_updated or datetime.utcnow(),
        )
        with sqlite3.connect(self._sqlite_path()) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO candidates (
                    id, first_name, last_name, email, phone, location,
                    current_title, years_experience, education_json, skills_json,
                    source, open_to_work, summary, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    candidate.id,
                    candidate.first_name,
                    candidate.last_name,
                    candidate.email,
                    candidate.phone,
                    candidate.location,
                    candidate.current_title,
                    candidate.years_experience,
                    json.dumps(candidate.education.model_dump()),
                    json.dumps(candidate.skills),
                    candidate.source,
                    int(candidate.open_to_work),
                    candidate.summary,
                    candidate.last_updated.isoformat(),
                ),
            )
            connection.commit()
        return candidate

    def _row_to_candidate_sqlite(self, row: tuple) -> CandidateRead:
        return CandidateRead(
            id=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            phone=row[4] or "",
            location=row[5] or "",
            current_title=row[6] or "",
            years_experience=row[7] or 0,
            education=Education(**json.loads(row[8] or "{}")),
            skills=json.loads(row[9] or "[]"),
            source=row[10] or "database",
            open_to_work=bool(row[11]),
            summary=row[12] or "",
            last_updated=datetime.fromisoformat(row[13]),
        )

    def _initialize_postgres(self) -> None:
        engine = create_engine(self.settings.database_url)
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS candidates (
                        id TEXT PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT,
                        location TEXT,
                        current_title TEXT,
                        years_experience INTEGER,
                        education_json TEXT,
                        skills_json TEXT,
                        source TEXT,
                        open_to_work BOOLEAN,
                        summary TEXT,
                        last_updated TEXT
                    )
                    """
                )
            )

    def _list_candidates_postgres(self) -> list[CandidateRead]:
        self._initialize_postgres()
        engine = create_engine(self.settings.database_url)
        with engine.begin() as connection:
            rows = connection.execute(text("SELECT * FROM candidates")).fetchall()
        return [
            CandidateRead(
                id=row.id,
                first_name=row.first_name,
                last_name=row.last_name,
                email=row.email,
                phone=row.phone or "",
                location=row.location or "",
                current_title=row.current_title or "",
                years_experience=row.years_experience or 0,
                education=Education(**json.loads(row.education_json or "{}")),
                skills=json.loads(row.skills_json or "[]"),
                source=row.source or "database",
                open_to_work=bool(row.open_to_work),
                summary=row.summary or "",
                last_updated=datetime.fromisoformat(row.last_updated),
            )
            for row in rows
        ]

    def _create_candidate_postgres(self, payload: CandidateCreate) -> CandidateRead:
        existing = self._list_candidates_postgres()
        candidate = CandidateRead(
            **payload.model_dump(exclude={"id", "last_updated"}),
            id=payload.id or f"CAND{len(existing) + 1:03d}",
            last_updated=payload.last_updated or datetime.utcnow(),
        )
        engine = create_engine(self.settings.database_url)
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    INSERT INTO candidates (
                        id, first_name, last_name, email, phone, location,
                        current_title, years_experience, education_json, skills_json,
                        source, open_to_work, summary, last_updated
                    ) VALUES (
                        :id, :first_name, :last_name, :email, :phone, :location,
                        :current_title, :years_experience, :education_json, :skills_json,
                        :source, :open_to_work, :summary, :last_updated
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        email = EXCLUDED.email,
                        phone = EXCLUDED.phone,
                        location = EXCLUDED.location,
                        current_title = EXCLUDED.current_title,
                        years_experience = EXCLUDED.years_experience,
                        education_json = EXCLUDED.education_json,
                        skills_json = EXCLUDED.skills_json,
                        source = EXCLUDED.source,
                        open_to_work = EXCLUDED.open_to_work,
                        summary = EXCLUDED.summary,
                        last_updated = EXCLUDED.last_updated
                    """
                ),
                {
                    "id": candidate.id,
                    "first_name": candidate.first_name,
                    "last_name": candidate.last_name,
                    "email": candidate.email,
                    "phone": candidate.phone,
                    "location": candidate.location,
                    "current_title": candidate.current_title,
                    "years_experience": candidate.years_experience,
                    "education_json": json.dumps(candidate.education.model_dump()),
                    "skills_json": json.dumps(candidate.skills),
                    "source": candidate.source,
                    "open_to_work": candidate.open_to_work,
                    "summary": candidate.summary,
                    "last_updated": candidate.last_updated.isoformat(),
                },
            )
        return candidate
