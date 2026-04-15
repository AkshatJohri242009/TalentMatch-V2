def seed_candidate(client, first_name, skills, years_experience, title):
    client.post(
        "/api/candidates",
        json={
            "first_name": first_name,
            "last_name": "Candidate",
            "email": f"{first_name.lower()}@example.com",
            "current_title": title,
            "years_experience": years_experience,
            "skills": skills,
            "education": {"degree": "B.S. Computer Science"},
            "summary": f"{title} with {' '.join(skills)} experience."
        },
    )


def test_matching_returns_ranked_candidates(client):
    seed_candidate(client, "Ava", ["Python", "FastAPI", "Docker"], 5, "Backend Developer")
    seed_candidate(client, "Liam", ["React", "CSS"], 2, "Frontend Developer")

    response = client.post(
        "/api/match",
        json={
            "job_description": "Looking for a Python FastAPI engineer with Docker experience.",
            "required_skills": ["Python", "FastAPI", "Docker"],
            "min_experience": 3,
            "preferred_education": "B.S."
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["matches"][0]["candidate_name"].startswith("Ava")
    assert payload["matches"][0]["score"] >= payload["matches"][1]["score"]
