import httpx
from typing import List, Dict
from fastapi import HTTPException
import os

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
ADZUNA_URL = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

async def search_jobs(search_params=None) -> List[Dict]:
    if search_params is None:
        search_params = {}
    keywords = search_params.get("keywords", "")
    location = search_params.get("location", "")
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 10,
        "what": keywords,
        "where": location,
        "content-type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(ADZUNA_URL, params=params)
        if response.status_code != 200:
            print("Adzuna API error:", response.text)
            raise HTTPException(status_code=502, detail="Adzuna API error")
        data = response.json()
        jobs = []
        for job in data.get("results", []):
            jobs.append({
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "description": job.get("description"),
                "url": job.get("redirect_url"),
                "created": job.get("created"),
            })
        return jobs 