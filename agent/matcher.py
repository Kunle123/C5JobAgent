import os
import openai
from typing import List, Dict

openai.api_key = os.getenv("OPENAI_API_KEY")

async def match_jobs_to_profile(ark_data, jobs: List[Dict]) -> List[Dict]:
    profile_text = str(ark_data)
    matches = []
    for job in jobs:
        prompt = f"""
Given the following user profile:
{profile_text}

And the following job description:
{job['description']}

Rate how well this job matches the user's profile on a scale from 0 to 1, and explain why. Respond in JSON as: {{'score': <float>, 'explanation': <string>}}
"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.2,
        )
        content = response.choices[0].message['content']
        try:
            result = eval(content) if content.strip().startswith('{') else {}
        except Exception:
            result = {"score": 0, "explanation": "Could not parse OpenAI response."}
        matches.append({
            "job": job,
            "score": result.get("score", 0),
            "explanation": result.get("explanation", "No explanation.")
        })
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches 