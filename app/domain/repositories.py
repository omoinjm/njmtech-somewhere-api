from abc import ABC, abstractmethod
from typing import Optional

from app.domain.models import Location, Flight


class IFlightRepository(ABC):
    """
    Abstract interface for a flight data repository.
    Defines the contract for fetching flight and location data.
    """

    @abstractmethod
    async def get_location_by_city(self, city_name: str) -> Optional[Location]:
        """
        Retrieves location information for a given city name.

        Args:
            city_name: The name of the city.

        Returns:
            A Location object or None if not found.
        """
        pass

    @abstractmethod
    async def find_cheapest_flight(self, from_code: str, to_code: str) -> Optional[float]:
        """
        Finds the cheapest flight price between two location codes.

        Args:
            from_code: The departure location code.
            to_code: The arrival location code.

        Returns:
            The cheapest price as a float, or None if no flight is found.
        """
        pass
