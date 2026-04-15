from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from app.models.schemas import (
    CandidateCreate,
    CandidateRead,
    CandidateSearchResponse,
    FeedbackCreate,
    JobMatchRequest,
    JobMatchResponse,
)
from app.services.candidate_service import CandidateService, get_candidate_service
from app.services.learning_service import LearningService, get_learning_service
from app.services.match_service import MatchService, get_match_service
from app.services.resume_service import ResumeService, get_resume_service

router = APIRouter()


@router.get("/candidates", response_model=CandidateSearchResponse)
def list_candidates(
    query: str | None = None,
    skills: list[str] | None = Query(default=None),
    min_experience: int | None = None,
    service: CandidateService = Depends(get_candidate_service),
) -> CandidateSearchResponse:
    candidates = service.search_candidates(
        query=query, skills=skills or [], min_experience=min_experience
    )
    return CandidateSearchResponse(items=candidates, total=len(candidates))


@router.get("/candidates/semantic", response_model=CandidateSearchResponse)
def semantic_candidates(
    query: str,
    top_k: int = 5,
    service: CandidateService = Depends(get_candidate_service),
) -> CandidateSearchResponse:
    candidates = service.semantic_search(query=query, top_k=top_k)
    return CandidateSearchResponse(items=candidates, total=len(candidates))


@router.post("/candidates", response_model=CandidateRead)
def create_candidate(
    payload: CandidateCreate,
    service: CandidateService = Depends(get_candidate_service),
) -> CandidateRead:
    return service.create_candidate(payload)


@router.post("/resume/upload", response_model=CandidateRead)
async def upload_resume(
    file: UploadFile = File(...),
    resume_service: ResumeService = Depends(get_resume_service),
    candidate_service: CandidateService = Depends(get_candidate_service),
) -> CandidateRead:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    parsed = await resume_service.parse_resume(file)
    return candidate_service.create_candidate(parsed)


@router.post("/match", response_model=JobMatchResponse)
def match_job(
    payload: JobMatchRequest,
    service: MatchService = Depends(get_match_service),
) -> JobMatchResponse:
    return service.match_job(payload)


@router.post("/feedback")
def submit_feedback(
    payload: FeedbackCreate,
    service: LearningService = Depends(get_learning_service),
) -> dict[str, str]:
    service.record_feedback(payload)
    return {"status": "accepted"}


@router.get("/learning/weights")
def get_weights(
    service: LearningService = Depends(get_learning_service),
) -> dict[str, float]:
    return service.get_weights()
