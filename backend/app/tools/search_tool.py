from app.services.candidate_service import CandidateService


class SearchTool:
    def __init__(self) -> None:
        self.service = CandidateService()
