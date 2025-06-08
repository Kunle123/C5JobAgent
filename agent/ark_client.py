import httpx

API_GW_BASE_URL = "https://api-gw-production.up.railway.app"

async def get_user_ark_data(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        # Step 1: Get the profile ID for the current user
        me_url = f"{API_GW_BASE_URL}/api/career-ark/profiles/me"
        me_response = await client.get(me_url, headers=headers)
        me_response.raise_for_status()
        profile_id = me_response.json()["id"]
        # Step 2: Fetch all sections for that profile
        all_sections_url = f"{API_GW_BASE_URL}/api/career-ark/profiles/{profile_id}/all_sections"
        all_sections_response = await client.get(all_sections_url, headers=headers)
        all_sections_response.raise_for_status()
        return all_sections_response.json() 