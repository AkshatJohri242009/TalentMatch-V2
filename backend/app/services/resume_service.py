from functools import lru_cache
from pathlib import Path
import re

from fastapi import UploadFile

from app.models.schemas import CandidateCreate, Education

try:
    import fitz  # type: ignore
except ImportError:  # pragma: no cover
    fitz = None


class ResumeService:
    async def parse_resume(self, upload: UploadFile) -> CandidateCreate:
        content = await upload.read()
        suffix = Path(upload.filename).suffix.lower()
        text = self._extract_text(content, suffix)
        return self._parse_text(text, upload.filename)

    def _extract_text(self, content: bytes, suffix: str) -> str:
        if suffix == ".pdf" and fitz is not None:
            document = fitz.open(stream=content, filetype="pdf")
            return "\n".join(page.get_text() for page in document)
        return content.decode("utf-8", errors="ignore")

    def _parse_text(self, text: str, filename: str) -> CandidateCreate:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        first_line = lines[0] if lines else Path(filename).stem.replace("_", " ")
        name_parts = first_line.split()
        first_name = name_parts[0] if name_parts else "Unknown"
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else "Candidate"

        email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
        phone_match = re.search(r"(\+?\d[\d\-\s]{8,}\d)", text)
        exp_match = re.search(r"(\d+)\+?\s+years", text, re.IGNORECASE)
        skills = self._extract_skills(text)

        return CandidateCreate(
            first_name=first_name,
            last_name=last_name,
            email=email_match.group(0) if email_match else f"{first_name.lower()}@example.com",
            phone=phone_match.group(0) if phone_match else "",
            current_title=self._extract_title(text),
            years_experience=int(exp_match.group(1)) if exp_match else 0,
            education=Education(
                degree=self._extract_degree(text),
                university=self._extract_university(text),
            ),
            skills=skills,
            source="resume-upload",
            summary=text[:500],
        )

    def _extract_skills(self, text: str) -> list[str]:
        known_skills = [
            "python",
            "java",
            "javascript",
            "react",
            "fastapi",
            "sql",
            "postgresql",
            "docker",
            "kubernetes",
            "aws",
            "langchain",
            "machine learning",
            "faiss",
        ]
        lowered = text.lower()
        return [skill.title() for skill in known_skills if skill in lowered]

    def _extract_title(self, text: str) -> str:
        for title in [
            "Software Engineer",
            "Data Scientist",
            "Product Manager",
            "Machine Learning Engineer",
            "Backend Developer",
            "Frontend Developer",
        ]:
            if title.lower() in text.lower():
                return title
        return "Candidate"

    def _extract_degree(self, text: str) -> str:
        for degree in ["B.S.", "M.S.", "MBA", "Ph.D", "Bachelor", "Master"]:
            if degree.lower() in text.lower():
                return degree
        return ""

    def _extract_university(self, text: str) -> str:
        lines = text.splitlines()
        for line in lines:
            if "university" in line.lower() or "institute" in line.lower():
                return line.strip()
        return ""


@lru_cache
def get_resume_service() -> ResumeService:
    return ResumeService()
