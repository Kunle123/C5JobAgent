# job_agent

## Purpose
AI-powered job search agent that:
- Fetches a user's profile from the Ark service (using their auth token)
- Searches external job boards (starting with JobServe) for relevant jobs
- Uses AI to match and rank jobs to the user's profile, with explanations
- Exposes an API endpoint for the frontend to trigger job search and retrieve results

## Key Components
- Ark client (fetch user profile)
- Auth client (validate token, get user info)
- JobServe integration
- AI/rule-based matcher (OpenAI or similar)
- FastAPI endpoints
- Pydantic schemas, utils, and tests

## Setup
- Deploy on Railway, using environment variables for service connections
- No local .env required for live testing

## Quickstart
1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   uvicorn main:app --reload
   ```

## API
- `POST /search_jobs` — Triggers job search and returns ranked matches

## Folder Structure
- main.py — FastAPI entrypoint
- agent/ — Core logic (clients, matcher, job search)
- tests/ — Unit tests 