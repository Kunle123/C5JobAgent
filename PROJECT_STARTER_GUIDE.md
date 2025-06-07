# AI Job Search Agent — Project Starter Guide

## 1. Project Goal
Build a service (or agent) that:
- Fetches a user's normalized CV/profile data from the Ark service (using their auth token).
- Searches external job boards/APIs for relevant jobs.
- Uses AI (LLM or rules) to match jobs to the user's profile.
- Returns a ranked list of job matches, with explanations.

---

## 2. Key Requirements
- **Access to Ark Data:**
  - Use the `/api/career-ark/profiles/{profile_id}/all_sections` endpoint to fetch user data.
- **User Authentication:**
  - Use the Auth service to validate tokens and get user info.
- **Job Board Integration:**
  - Integrate with one or more job board APIs (e.g., Adzuna, Indeed, LinkedIn, or scrape public boards).
- **AI Matching Logic:**
  - Use OpenAI or similar to compare user data with job descriptions and rank matches.
- **API for Frontend:**
  - Expose endpoints for the frontend to trigger job search and retrieve results.

---

## 3. Recommended Folder Structure

Place the new folder at the root of your monorepo:

```
/CandidateV-clean/
  apps/
    arc/                # Ark service
    ai/                 # AI service
    ...
  job_agent/            # <--- Your new AI job search agent
  ...
```

**Inside `job_agent/`:**
```
job_agent/
  README.md
  requirements.txt
  main.py                # FastAPI app entrypoint
  agent/
    __init__.py
    job_search.py        # Logic for querying job boards
    matcher.py           # AI/rule-based matching logic
    ark_client.py        # Client for fetching Ark data
    auth_client.py       # Client for validating tokens
    schemas.py           # Pydantic models for requests/responses
    utils.py
  tests/
    test_job_search.py
    test_matcher.py
  .env.example           # For API keys, endpoints, etc.
```

---

## 4. Setup Instructions

1. **Clone the repo and create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set environment variables (see `.env.example`):**
   - `ARK_API_URL`
   - `AUTH_API_URL`
   - `OPENAI_API_KEY`
   - `JOB_BOARD_API_KEY` (if needed)

3. **Run the app:**
   ```bash
   uvicorn main:app --reload
   ```

---

## 5. Example `requirements.txt`
```
fastapi
uvicorn
httpx
pydantic
openai
python-dotenv
```

---

## 6. Example `main.py`
```python
from fastapi import FastAPI, Depends, HTTPException, Request
from agent.ark_client import get_user_ark_data
from agent.job_search import search_jobs
from agent.matcher import match_jobs_to_profile
from agent.auth_client import get_user_id_from_token

app = FastAPI()

@app.post("/search_jobs")
async def search_jobs_for_user(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    user_id = await get_user_id_from_token(token)
    ark_data = await get_user_ark_data(user_id, token)
    jobs = await search_jobs()  # implement search params as needed
    matches = await match_jobs_to_profile(ark_data, jobs)
    return {"matches": matches}
```

---

## 7. Implementation Notes

- **Ark Client:** Use HTTPX to call `/api/career-ark/profiles/{profile_id}/all_sections` with the user's token.
- **Auth Client:** Validate the JWT or call your Auth service to get the user's ID/email.
- **Job Search:** Start with a public API (Adzuna, etc.) or scrape a board for prototyping.
- **Matching:** Use OpenAI's API to compare each job description to the user's skills/experience, or use a rules-based approach for cost control.
- **Security:** Never store user tokens; always pass through from frontend.

---

## 8. API Endpoints

- `POST /search_jobs`
  - Auth header: Bearer token
  - Body: `{ "search_params": { ... } }`
  - Returns: `{ "matches": [ ... ] }`

---

## 9. Optional: Monorepo Integration
- If you want to share code (e.g., Pydantic schemas) between services, consider a `shared/` folder at the root.
- Otherwise, keep the agent isolated and communicate via HTTP APIs.

---

## 10. Summary Table

| Component      | Source/Dependency         | Notes                                 |
|----------------|--------------------------|---------------------------------------|
| Ark Data       | Ark service API          | Use user token for auth               |
| Auth           | Auth service API/JWT     | Validate and extract user info        |
| Job Boards     | External API             | Adzuna, Indeed, LinkedIn, etc.        |
| AI Matching    | OpenAI API               | Use for ranking jobs to user profile  |
| Frontend       | Your existing frontend   | Call new agent API for job search     |

---

## 11. Next Steps

1. **Create the `job_agent` folder at the root of your repo.**
2. **Copy the above starter files and structure.**
3. **Implement the clients and logic step by step.**
4. **Test with a real user and real Ark data.**

---

**Need a code template for any module? Want a script to scaffold this folder? Just ask!** 