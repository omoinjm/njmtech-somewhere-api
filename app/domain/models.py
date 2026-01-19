from pydantic import BaseModel, Field
from typing import List


class FlightOptimizeRequest(BaseModel):
    """API request model for flight optimization."""
    from_city: str = Field(..., description="The starting city.", examples=["London"])
    to_cities: List[str] = Field(..., description="List of destination cities.", examples=[["Paris", "Berlin", "Rome"]])


class FlightOptimizationResult(BaseModel):
    """API response model for the best flight option."""
    best_city: str = Field(..., description="The city with the best price per kilometer.", examples=["Paris"])
    price_per_km: float = Field(..., description="The cost per kilometer for the flight.", examples=[0.42])
    currency: str = Field(..., description="The currency of the price.", examples=["USD"])
    distance_km: float = Field(..., description="The distance of the flight in kilometers.", examples=[342.1])
    total_price: float = Field(..., description="The total price of the flight.", examples=[143.70])


class Location(BaseModel):
    """Represents a geographical location with coordinates."""
    name: str
    code: str
    lat: float
    lon: float


class Flight(BaseModel):
    """Represents a flight between two locations."""
    from_location: Location
    to_location: Location
    price: float
    currency: str = "USD"
    distance_km: float
    price_per_km: float
