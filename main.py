from fastapi import FastAPI, Request, HTTPException
from agent.auth_client import get_user_id_from_token
from agent.ark_client import get_user_ark_data
from agent.job_search import search_jobs
from agent.matcher import match_jobs_to_profile

app = FastAPI()

@app.post("/search_jobs")
async def search_jobs_for_user(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        user_id, user_email = await get_user_id_from_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    try:
        ark_data = await get_user_ark_data(token)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not fetch Ark profile: {e}")
    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    search_params = body.get("search_params", {})
    jobs = await search_jobs(search_params)
    matches = await match_jobs_to_profile(ark_data, jobs)
    return {"ark_data": ark_data, "user_id": user_id, "user_email": user_email, "matches": matches} 