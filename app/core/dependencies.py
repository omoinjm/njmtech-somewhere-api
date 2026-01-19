import httpx
from fastapi import Depends
from functools import lru_cache

from app.core.config import Settings, settings as app_settings
from app.application.services import FlightOptimizationService
from app.domain.repositories import IFlightRepository
from app.infrastructure.repositories.kiwi_flight_repository import KiwiFlightRepository


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Returns the application settings."""
    return app_settings


def get_http_client() -> httpx.AsyncClient:
    """Returns a singleton httpx.AsyncClient."""
    # In a real app, you might want to manage the client's lifecycle,
    # for example, by creating it in the app's startup event.
    return httpx.AsyncClient()


def get_flight_repository(
    settings: Settings = Depends(get_settings),
    client: httpx.AsyncClient = Depends(get_http_client),
) -> IFlightRepository:
    """
    Dependency provider for the flight repository.
    Returns an instance of the KiwiFlightRepository.
    """
    return KiwiFlightRepository(settings=settings, client=client)


def get_flight_optimization_service(
    flight_repository: IFlightRepository = Depends(get_flight_repository),
) -> FlightOptimizationService:
    """
    Dependency provider for the flight optimization service.
    """
    return FlightOptimizationService(flight_repository=flight_repository)
