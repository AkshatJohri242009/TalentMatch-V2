from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Education(BaseModel):
    degree: str = ""
    university: str = ""
    graduation_year: int | None = None


class CandidateBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str = ""
    location: str = ""
    current_title: str = ""
    years_experience: int = 0
    education: Education = Field(default_factory=Education)
    skills: list[str] = Field(default_factory=list)
    source: str = "manual"
    open_to_work: bool = True
    summary: str = ""


class CandidateCreate(CandidateBase):
    id: str | None = None
    last_updated: datetime | None = None


class CandidateRead(CandidateBase):
    id: str
    last_updated: datetime


class CandidateSearchResponse(BaseModel):
    items: list[CandidateRead]
    total: int


class JobMatchRequest(BaseModel):
    job_description: str
    required_skills: list[str] = Field(default_factory=list)
    min_experience: int = 0
    preferred_education: str = ""
    top_k: int = 5


class MatchBreakdown(BaseModel):
    candidate_id: str
    candidate_name: str
    score: float
    weighted_score: float
    semantic_score: float
    skill_score: float
    experience_score: float
    role_score: float
    education_score: float
    explanation: str
    features: dict[str, Any]


class JobMatchResponse(BaseModel):
    matches: list[MatchBreakdown]
    weights: dict[str, float]


class FeedbackCreate(BaseModel):
    job_description: str
    candidate_id: str
    match_score: float
    feature_breakdown: dict[str, float]
    feedback_signal: str
