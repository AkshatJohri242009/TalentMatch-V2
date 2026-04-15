class PlannerAgent:
    def create_plan(self, analysis: dict[str, object]) -> dict[str, object]:
        return {
            "focus_skills": analysis.get("required_skills", []),
            "experience_target": analysis.get("min_experience", 0),
            "education_preference": analysis.get("preferred_education", ""),
        }
