import os
import openai
import json
from typing import List, Dict

openai_api_key = os.getenv("OPENAI_API_KEY")
client = openai.AsyncOpenAI(api_key=openai_api_key)

async def match_jobs_to_profile(ark_data, jobs: List[Dict]) -> List[Dict]:
    profile_text = str(ark_data)
    matches = []
    for job in jobs:
        prompt = f"""
Given the following user profile:
{profile_text}

And the following job description:
{job['description']}

Rate how well this job matches the user's profile on a scale from 0 to 1, and explain why. Respond ONLY in valid JSON as: {{"score": <float>, "explanation": <string>}}
"""
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.2,
        )
        content = response.choices[0].message.content
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            result = {"score": 0, "explanation": "Could not parse OpenAI response as JSON."}
        matches.append({
            "job": job,
            "score": result.get("score", 0),
            "explanation": result.get("explanation", "No explanation.")
        })
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches 