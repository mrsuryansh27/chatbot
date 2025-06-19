from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import FlightSearchRequest, FlightOffer
from app.services.duffel_client import duffel_client

router = APIRouter(prefix="/api/flights", tags=["flights"])

@router.post("/search", response_model=List[FlightOffer])
async def search_flights(req: FlightSearchRequest):
    # 1) Build the slices & passengers payload
    slices = [{
        "origin": req.origin,
        "destination": req.destination,
        "departure_date": req.departure_date,
        **({"return_date": req.return_date} if req.return_date else {})
    }]
    passengers = [{"type": "adult", "count": req.adults}]

    # 2) Call Duffel via our HTTP client
    try:
        offers = await duffel_client.create_offer_request(
            slices=slices,
            passengers=passengers
        )
    except Exception as e:
        raise HTTPException(502, detail=str(e))

    # 3) Map raw offers into your Pydantic model using v2 schema
    results: List[FlightOffer] = []
    for o in offers:
        # Pull the first and last flight segments
        first_seg = o["slices"][0]["segments"][0]
        last_seg = o["slices"][0]["segments"][-1]

        # Extract IATA codes and timestamps
        dep_airport = first_seg["origin"]["iata_code"]       # e.g. "LHR" :contentReference[oaicite:0]{index=0}
        arr_airport = last_seg["destination"]["iata_code"]
        dep_time    = first_seg["departing_at"]
        arr_time    = last_seg["arriving_at"]

        # total_amount is now a string, and currency is in total_currency
        total_amount = float(o["total_amount"])              # e.g. "45.00" :contentReference[oaicite:1]{index=1}
        currency     = o["total_currency"]

        results.append(FlightOffer(
            id=o["id"],
            total_amount=total_amount,
            currency=currency,
            departure_airport=dep_airport,
            arrival_airport=arr_airport,
            departure_time=dep_time,
            arrival_time=arr_time,
        ))

    return results
