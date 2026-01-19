import asyncio
from typing import List, Optional

from haversine import haversine, Unit

from app.domain.models import Flight, Location, FlightOptimizationResult
from app.domain.repositories import IFlightRepository


class FlightOptimizationError(Exception):
    """Custom exception for errors during the flight optimization process."""
    pass


class FlightOptimizationService:
    """
    Service responsible for the core logic of finding the best flight deal.
    """

    def __init__(self, flight_repository: IFlightRepository):
        self._repo = flight_repository

    async def optimize(self, from_city: str, to_cities: List[str]) -> FlightOptimizationResult:
        """
        Orchestrates the flight optimization process.

        Args:
            from_city: The name of the departure city.
            to_cities: A list of names for possible destination cities.

        Returns:
            A FlightOptimizationResult with the details of the best flight found.

        Raises:
            FlightOptimizationError: If the origin city is not found or no valid flights
                                     can be found to any of the destinations.
        """
        from_location = await self._repo.get_location_by_city(from_city)
        if not from_location:
            raise FlightOptimizationError(f"Could not find origin city: {from_city}")

        # Concurrently fetch information for all potential flights
        flight_tasks = [
            self._evaluate_flight_option(from_location, to_city) for to_city in to_cities
        ]
        potential_flights = await asyncio.gather(*flight_tasks)

        # Filter out invalid options and find the best one
        valid_flights = [flight for flight in potential_flights if flight]
        if not valid_flights:
            raise FlightOptimizationError("No valid flights found for the given destinations.")

        best_flight = min(valid_flights, key=lambda flight: flight.price_per_km)

        return FlightOptimizationResult(
            best_city=best_flight.to_location.name,
            price_per_km=round(best_flight.price_per_km, 2),
            currency=best_flight.currency,
            distance_km=round(best_flight.distance_km, 4),
            total_price=best_flight.price,
        )

    async def _evaluate_flight_option(
        self, from_location: Location, to_city: str
    ) -> Optional[Flight]:
        """
        Evaluates a single flight route from an origin to a potential destination.
        """
        # 1. Get location data for the destination city
        to_location = await self._repo.get_location_by_city(to_city)
        if not to_location:
            return None

        # 2. Find the cheapest flight price
        price = await self._repo.find_cheapest_flight(
            from_code=from_location.code, to_code=to_location.code
        )
        if price is None:
            return None

        # 3. Calculate distance
        distance_km = haversine(
            (from_location.lat, from_location.lon),
            (to_location.lat, to_location.lon),
            unit=Unit.KILOMETERS,
        )

        if distance_km == 0:
            return None

        # 4. Calculate price per kilometer and create Flight object
        price_per_km = price / distance_km
        return Flight(
            from_location=from_location,
            to_location=to_location,
            price=price,
            distance_km=distance_km,
            price_per_km=price_per_km,
        )
