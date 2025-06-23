from fastapi import APIRouter, Depends
from typing import List

from app.auth import get_current_client
from app.services.duffel_client import duffel_client
from app.schemas import FlightSearch, FlightOffer

router = APIRouter(prefix="/v1/flights", tags=["flights"])

@router.post("/search", response_model=List[FlightOffer])
async def search_flights(
    params: FlightSearch,
    _ = Depends(get_current_client)
):
    offers = await duffel_client.search_offers(
        origin=params.origin,
        destination=params.destination,
        depart_date=params.depart_date,
        return_date=params.return_date,
        adults=params.adults
    )
    return [FlightOffer(**o) for o in offers]
