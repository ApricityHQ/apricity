# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run both frontend and backend concurrently
make dev

# Frontend only (http://localhost:3000)
make frontend

# Backend only (http://localhost:8000)
make backend

# Install all dependencies
make install
```

Individual commands:
```bash
# Frontend
cd frontend && bun install
cd frontend && bun run dev
cd frontend && bun run build
cd frontend && bun run lint

# Backend
cd backend && uv sync
cd backend && uv run uvicorn main:app --reload --port 8000
```

Run backend tests:
```bash
cd backend && uv run pytest -v
cd backend && uv run pytest -v tests/test_foo.py  # single file
```

## Architecture

This is an AI-powered startup analysis tool. Founders fill in structured documents about their startup, then the backend's multi-agent system produces a success probability analysis.

### Frontend (`/frontend`)

**Next.js App Router** with these main routes:
- `/` — landing page
- `/workspace` — list of saved workspaces
- `/workspace/[viewId]` — single report/workspace detail
- `/dashboard` — dashboard

**State management** is a single React Context + useReducer in `src/context/DocumentContext.jsx`. This manages all workspace state: documents, uploaded files, views, startup metadata. It auto-saves to **IndexedDB** (via idb-keyval) with a 500ms debounce. On sign-in, it syncs reports from the server.

**API routes** in `src/app/api/` act as authenticated proxies to the FastAPI backend — they attach Clerk JWT tokens before forwarding requests.

**Document templates** (Problem Statement, Founder Profile, Solution, Market Notes, Team, Funding, Risks, References, Custom) are defined in `src/config/artifacts.js`.

### Backend (`/backend`)

**FastAPI** app in `main.py`. The core endpoint is `POST /view` which:
1. Accepts startup description text + optional PDF uploads
2. Chunks documents and builds a per-request **Chroma vector store** for RAG
3. Runs **5 LangGraph agents in parallel** (Financial, VC, CTO, Marketing, Product)
4. Each agent retrieves relevant context from the vector store and analyzes through its lens
5. Also runs competitor search via Exa API in parallel

Supporting services:
- `company_search.py` — Exa API for competitor discovery
- `social_signals.py` — Reddit/HN/Twitter signal aggregation
- `db.py` — async SQLite (aiosqlite) for reports and chat history
- `auth.py` — Clerk JWT verification via JWKS
- `pdf_ingest.py` — PDF text extraction
- `text_chunking.py` — document chunking for RAG

**SQLite schema:** `reports` (id, user_id, prompt, result JSON, created_at) and `messages` (id, report_id, role, content, created_at) with cascade delete.

### Authentication flow

Clerk handles auth. Frontend attaches `Authorization: Bearer <token>` to all backend requests. Backend verifies via Clerk JWKS and extracts `user_id` (sub claim) for data isolation.

### Data persistence

- **Local:** IndexedDB for offline-first document editing (auto-migrates from localStorage on first load)
- **Server:** SQLite for reports and chat message history

## Backend Development Rules

### Testing (backend only)

Every backend change must be accompanied by an integration test. Tests use **real connections** — real SQLite DB, real file I/O, no mocks.

- Test files live in `backend/tests/`
- Use `pytest` with `pytest-asyncio` for async tests
- After writing a test, run `cd backend && uv run pytest -v` and iterate until it passes — that is the success criteria
- Tests should cover the actual behavior end-to-end (e.g., write to DB then read back, not just call the function in isolation)

### Function docstrings (backend only)

Every backend function must have a docstring with three sections:

```python
async def save_report(db: aiosqlite.Connection, user_id: str, prompt: str, result: dict) -> str:
    """
    Persist a new analysis report to the database.

    Args:
        db: Active aiosqlite database connection.
        user_id: Clerk user ID (sub claim from JWT) used for data isolation.
        prompt: The raw startup description text submitted by the user.
        result: Parsed JSON dict containing the multi-agent analysis output.

    Returns:
        The UUID string of the newly created report row.
    """
```

## Environment Setup

Copy `backend/.example.env` to `backend/.env` and fill in:
- `OPENAI_API_KEY` — GPT-4o for agents, GPT-4o-mini for summarization
- `EXA_API_KEY` — competitor search
- `CLERK_SECRET_KEY` / `CLERK_JWKS_URL` — backend JWT verification

Frontend uses Clerk's Next.js SDK — set `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY` in `frontend/.env.local`.
