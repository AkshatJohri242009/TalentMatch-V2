def test_candidate_creation_and_search(client):
    response = client.post(
        "/api/candidates",
        json={
            "first_name": "Ava",
            "last_name": "Stone",
            "email": "ava@example.com",
            "current_title": "Backend Developer",
            "years_experience": 5,
            "skills": ["Python", "FastAPI", "Docker"],
            "education": {"degree": "B.S. Computer Science"},
            "summary": "Backend engineer building FastAPI services."
        },
    )
    assert response.status_code == 200

    search_response = client.get("/api/candidates", params={"query": "backend"})
    assert search_response.status_code == 200
    payload = search_response.json()
    assert payload["total"] == 1
    assert payload["items"][0]["first_name"] == "Ava"


def test_resume_upload(client):
    response = client.post(
        "/api/resume/upload",
        files={
            "file": (
                "resume.txt",
                b"Taylor Reed\nEmail: taylor@example.com\n5 years experience with Python FastAPI Docker",
                "text/plain",
            )
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["email"] == "taylor@example.com"
    assert "Python" in payload["skills"]


def test_semantic_search(client):
    client.post(
        "/api/candidates",
        json={
            "first_name": "Nina",
            "last_name": "Ray",
            "email": "nina@example.com",
            "current_title": "Machine Learning Engineer",
            "years_experience": 6,
            "skills": ["Python", "FAISS", "Machine Learning"],
            "education": {"degree": "M.S. Computer Science"},
            "summary": "Builds semantic search and retrieval pipelines."
        },
    )
    response = client.get("/api/candidates/semantic", params={"query": "semantic search faiss"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["items"][0]["first_name"] == "Nina"
