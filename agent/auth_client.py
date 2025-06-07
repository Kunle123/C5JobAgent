import httpx

API_GW_BASE_URL = "https://api-gw-production.up.railway.app"

async def get_user_id_from_token(token: str):
    url = f"{API_GW_BASE_URL}/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["id"], data.get("email") 