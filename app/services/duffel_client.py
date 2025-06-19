# app/services/duffel_client.py

import httpx
from app.config import settings

class DuffelClient:
    def __init__(self):
        self.base_url = "https://api.duffel.com"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {settings.DUFFEL_API_KEY}",
                "Duffel-Version": "v2",
                "Content-Type": "application/json",
            },
            timeout=30,
        )

    async def create_offer_request(self, slices: list, passengers: list) -> list:
        resp = await self.client.post(
            f"{self.base_url}/air/offer_requests",
            json={
                "data": {
                    "slices": slices,
                    "passengers": passengers
                }
            },
        )
        resp.raise_for_status()
        return resp.json()["data"]["offers"]

# single shared instance
duffel_client = DuffelClient()
