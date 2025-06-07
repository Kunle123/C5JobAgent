import httpx

API_GW_BASE_URL = "https://api-gw-production.up.railway.app"

async def get_user_ark_data(profile_id: str, token: str):
    url = f"{API_GW_BASE_URL}/api/career-ark/profiles/{profile_id}/all_sections"
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json() 