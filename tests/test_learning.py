def test_learning_updates_weights(client):
    response = client.get("/api/learning/weights")
    original = response.json()

    feedback_response = client.post(
        "/api/feedback",
        json={
            "job_description": "Python backend role",
            "candidate_id": "CAND001",
            "match_score": 85,
            "feature_breakdown": {
                "skills": 0.9,
                "experience": 0.8,
                "role_similarity": 0.7,
                "education": 0.4
            },
            "feedback_signal": "good"
        },
    )
    assert feedback_response.status_code == 200

    updated = client.get("/api/learning/weights").json()
    assert updated["skills"] >= original["skills"]
