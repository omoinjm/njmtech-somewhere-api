from datetime import datetime, timedelta
from typing import Optional

import httpx

from app.core.config import Settings
from app.domain.models import Location
from app.domain.repositories import IFlightRepository


class KiwiFlightRepository(IFlightRepository):
    """
    Repository implementation for fetching flight data from the Kiwi Tequila API.
    """

    def __init__(self, settings: Settings, client: httpx.AsyncClient):
        self._settings = settings
        self._client = client
        self._headers = {"apikey": self._settings.KIWI_API_KEY}

    async def get_location_by_city(self, city_name: str) -> Optional[Location]:
        """
        Retrieves location information from the Kiwi API for a given city name.
        It specifically looks for airport locations.
        """
        url = f"{self._settings.KIWI_API_URL}/locations/query"
        params = {
            "term": city_name,
            "location_types": "airport",
            "limit": 1,
            "active_only": "true",
        }
        try:
            response = await self._client.get(url, params=params, headers=self._headers)
            response.raise_for_status()
            data = response.json()
            if not data.get("locations"):
                return None

            location_data = data["locations"][0]
            return Location(
                name=location_data["name"],
                code=location_data["code"],
                lat=location_data["location"]["lat"],
                lon=location_data["location"]["lon"],
            )
        except (httpx.HTTPStatusError, httpx.RequestError, KeyError, IndexError):
            # In a real app, log the error
            return None

    async def find_cheapest_flight(self, from_code: str, to_code: str) -> Optional[float]:
        """
        Finds the cheapest flight price from the Kiwi Search API.
        Searches for flights in the next 7 days.
        """
        url = f"{self._settings.KIWI_API_URL}/search"
        today = datetime.utcnow()
        tomorrow = today + timedelta(days=1)
        seven_days_from_now = today + timedelta(days=7)

        params = {
            "fly_from": from_code,
            "fly_to": to_code,
            "date_from": tomorrow.strftime("%d/%m/%Y"),
            "date_to": seven_days_from_now.strftime("%d/%m/%Y"),
            "partner_market": "us",
            "curr": "USD",
            "sort": "price",
            "limit": 1,
        }
        try:
            response = await self._client.get(url, params=params, headers=self._headers)
            response.raise_for_status()
            data = response.json()
            if not data.get("data"):
                return None

            return data["data"][0]["price"]
        except (httpx.HTTPStatusError, httpx.RequestError, KeyError, IndexError):
            # In a real app, log the error
            return None
