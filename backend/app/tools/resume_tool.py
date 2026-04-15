from app.services.resume_service import ResumeService


class ResumeTool:
    def __init__(self) -> None:
        self.service = ResumeService()
