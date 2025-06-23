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

    async def search_offers(self, origin, destination, depart_date, return_date, adults):
        req = {
            "data": {
                "slices": [{"origin": origin, "destination": destination, "departure_date": depart_date}],
                "passengers": [{"type": "adult", "quantity": adults}],
            }
        }
        if return_date:
            req["data"]["slices"].append({"origin": destination, "destination": origin, "departure_date": return_date})

        resp = await self.client.post(f"{self.base_url}/air/offer_requests", json=req)
        resp.raise_for_status()
        return resp.json()["data"]["offers"]

duffel_client = DuffelClient()
