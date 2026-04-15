import { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000/api";

const seedJob = "We need a Python and FastAPI engineer with PostgreSQL, Docker, and LangChain experience to build matching systems.";

export default function App() {
  const [candidates, setCandidates] = useState([]);
  const [matches, setMatches] = useState([]);
  const [weights, setWeights] = useState({});
  const [jobDescription, setJobDescription] = useState(seedJob);
  const [status, setStatus] = useState("Loading candidates...");

  useEffect(() => {
    loadCandidates();
  }, []);

  async function loadCandidates() {
    try {
      const response = await fetch(`${API_BASE}/candidates`);
      const data = await response.json();
      setCandidates(data.items || []);
      setStatus("Candidates loaded.");
    } catch (error) {
      setStatus("Backend not reachable yet.");
    }
  }

  async function runMatch() {
    setStatus("Running match...");
    const response = await fetch(`${API_BASE}/match`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        job_description: jobDescription,
        required_skills: ["Python", "FastAPI", "PostgreSQL", "Docker", "LangChain"],
        min_experience: 3,
        preferred_education: "B.S.",
        top_k: 5
      }),
    });
    const data = await response.json();
    setMatches(data.matches || []);
    setWeights(data.weights || {});
    setStatus("Match complete.");
  }

  async function uploadResume(event) {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }
    const form = new FormData();
    form.append("file", file);
    setStatus(`Uploading ${file.name}...`);
    const response = await fetch(`${API_BASE}/resume/upload`, {
      method: "POST",
      body: form,
    });
    if (response.ok) {
      setStatus("Resume uploaded.");
      await loadCandidates();
    } else {
      setStatus("Resume upload failed.");
    }
  }

  return (
    <div className="page-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">TalentMatch AI</p>
          <h1>Recruiting intelligence with search, matching, and learning.</h1>
          <p className="lede">
            Upload resumes, index candidates, run job matching, and refine weights
            over time through feedback.
          </p>
        </div>
        <div className="card actions">
          <label className="upload">
            <span>Upload Resume</span>
            <input type="file" accept=".txt,.pdf" onChange={uploadResume} />
          </label>
          <button onClick={runMatch}>Run Match</button>
          <p className="status">{status}</p>
        </div>
      </section>

      <section className="panel-grid">
        <div className="card">
          <h2>Job Description</h2>
          <textarea
            value={jobDescription}
            onChange={(event) => setJobDescription(event.target.value)}
            rows={8}
          />
          <div className="weights">
            {Object.entries(weights).map(([key, value]) => (
              <span key={key}>
                {key}: {(value * 100).toFixed(1)}%
              </span>
            ))}
          </div>
        </div>

        <div className="card">
          <h2>Candidate Database</h2>
          <div className="list">
            {candidates.slice(0, 8).map((candidate) => (
              <article key={candidate.id} className="list-item">
                <strong>
                  {candidate.first_name} {candidate.last_name}
                </strong>
                <span>{candidate.current_title || "Candidate"}</span>
                <span>{candidate.skills.join(", ")}</span>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="card">
        <h2>Top Matches</h2>
        <div className="list">
          {matches.map((match) => (
            <article key={match.candidate_id} className="match-item">
              <div>
                <strong>{match.candidate_name}</strong>
                <p>{match.explanation}</p>
              </div>
              <div className="score">{match.score}%</div>
            </article>
          ))}
          {matches.length === 0 && <p>No matches yet. Run the engine to compare candidates.</p>}
        </div>
      </section>
    </div>
  );
}
