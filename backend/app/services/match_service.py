from functools import lru_cache

from app.agents.analyzer_agent import AnalyzerAgent
from app.agents.matcher_agent import MatcherAgent
from app.agents.planner_agent import PlannerAgent
from app.models.schemas import JobMatchRequest, JobMatchResponse
from app.services.candidate_service import get_candidate_service
from app.services.learning_service import get_learning_service


class MatchService:
    def __init__(self) -> None:
        self.candidate_service = get_candidate_service()
        self.learning_service = get_learning_service()
        self.analyzer = AnalyzerAgent()
        self.planner = PlannerAgent()
        self.matcher = MatcherAgent(self.learning_service)

    def match_job(self, payload: JobMatchRequest) -> JobMatchResponse:
        candidates = self.candidate_service.list_candidates()
        analysis = self.analyzer.analyze(payload)
        plan = self.planner.create_plan(analysis)
        matches = self.matcher.match(payload, candidates, plan)
        return JobMatchResponse(
            matches=matches[: payload.top_k],
            weights=self.learning_service.get_weights(),
        )


@lru_cache
def get_match_service() -> MatchService:
    return MatchService()
