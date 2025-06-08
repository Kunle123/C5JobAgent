import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict
from fastapi import HTTPException

JOB_SERVE_RSS_URL = "https://www.jobserve.com/gb/en/Job-Search/rss.aspx"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

async def search_jobs(search_params=None) -> List[Dict]:
    if search_params is None:
        search_params = {}
    keywords = search_params.get("keywords", "")
    location = search_params.get("location", "")
    params = {"keywords": keywords, "location": location}
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient() as client:
        response = await client.get(JOB_SERVE_RSS_URL, params=params, headers=headers)
        response.raise_for_status()
        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as e:
            print("JobServe RSS response was not valid XML:", response.text)
            raise HTTPException(status_code=502, detail="JobServe RSS feed is not valid XML or returned an error page.")
        jobs = []
        for item in root.findall(".//item"):
            job = {
                "title": item.findtext("title"),
                "link": item.findtext("link"),
                "description": item.findtext("description"),
                "pubDate": item.findtext("pubDate"),
            }
            jobs.append(job)
        return jobs 