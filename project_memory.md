# Project Memory

## Completed Modules
- Initial repository inspection completed on 2026-04-15.
- Identified existing assets: empty backend scaffold and `data/generate_mock_data.py`.
- FastAPI backend scaffolded with candidate CRUD, resume upload, job matching, feedback, and weights endpoints.
- Agent pipeline implemented with analyzer, planner, and matcher stages.
- Learning subsystem implemented with feedback storage, adaptive weight updates, and persistent JSON weights.
- React/Vite frontend implemented for upload, candidate viewing, job matching, and weight display.
- Backend tests passing and frontend production build verified.
- Added optional database-backed persistence, semantic-search index snapshots, and LangChain-style reasoning hooks.
- Added semantic candidate search endpoint and final usage documentation in `README.md`.
- Verified upgraded backend cycle with `5 passed` tests on 2026-04-15.

## Active Bugs
- No known backend test failures.
- Real LangChain and PostgreSQL execution still depends on extra packages being available in the runtime.

## Fix History
- Resolved missing runtime validation by creating a repo-local Python dependency path in `.deps`.
- Resolved Windows test cleanup failure by resetting fixture files with writes instead of unlink operations.
- Resolved learning-weight drift by adjusting positive feedback amplification before normalization.
- Resolved frontend sandbox build failure by running Vite build outside sandbox constraints.
- Resolved database-mode instability by making real database persistence explicit opt-in via `TALENTMATCH_USE_DATABASE`.

## Architecture Decisions
- Use FastAPI backend with SQLite fallback and optional PostgreSQL connection.
- Use local JSON persistence for learning weights and mock candidate data to keep the MVP runnable without external infrastructure.
- Wrap advanced AI features behind deterministic fallbacks so the app still works if optional libraries are unavailable.
- Keep vector search persistence in `data/vector_index.json` so semantic search has a durable snapshot even without FAISS binaries.

## Model Improvements
- Start with deterministic weighted scoring plus token-similarity fallback.
- Positive match feedback now increases reinforced feature weights more directly.

## Next Steps
- Add real database persistence and migration support.
- Upgrade semantic search from token similarity to full embedding storage and FAISS indexing.
- Wire frontend feedback submission and richer search filters.
- Add containerization and deployment configuration for production hosting.
