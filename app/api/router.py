from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services import (
    FlightOptimizationService,
    FlightOptimizationError,
)
from app.core.dependencies import get_flight_optimization_service
from app.domain.models import FlightOptimizeRequest, FlightOptimizationResult


router = APIRouter()


@router.post(
    "/flight/optimize",
    response_model=FlightOptimizationResult,
    summary="Find the Best Flight Deal",
    description="Analyzes flight prices and distances to find the destination with the best value (lowest price per kilometer).",
)
async def optimize_flight(
    request: FlightOptimizeRequest,
    service: FlightOptimizationService = Depends(get_flight_optimization_service),
):
    """
    This endpoint takes a starting city and a list of potential destination cities
    and returns the one that represents the best value for money.
    """
    try:
        result = await service.optimize(
            from_city=request.from_city, to_cities=request.to_cities
        )
        return result
    except FlightOptimizationError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception:
        # For unhandled exceptions, return a generic 500 error
        # In a real app, you would log this exception.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
