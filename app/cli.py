import asyncio
import typer
from typing_extensions import Annotated
from typing import List

import httpx

from .application.services import FlightOptimizationService, FlightOptimizationError
from .core.config import settings
from .infrastructure.repositories.kiwi_flight_repository import KiwiFlightRepository

def get_service() -> FlightOptimizationService:
    """Manually construct the service for the CLI."""
    client = httpx.AsyncClient()
    if not settings.KIWI_API_KEY or settings.KIWI_API_KEY == "YOUR_API_KEY_HERE":
        typer.secho(
            "Error: KIWI_API_KEY is not configured.",
            fg=typer.colors.RED,
            bold=True
        )
        typer.secho(
            "Please set your Kiwi Tequila API key in the .env file or as an environment variable.",
            fg=typer.colors.YELLOW
        )
        raise typer.Exit(code=1)
    repo = KiwiFlightRepository(settings=settings, client=client)
    return FlightOptimizationService(flight_repository=repo)


def main(
    from_city: Annotated[str, typer.Option("--from", help="The starting city.")],
    to_cities: Annotated[str, typer.Option("--to", help="A comma-separated list of destination cities.")],
):
    """
    Finds the best flight deal from a starting city to a list of destinations.
    """
    service = get_service()
    destinations = [c.strip() for c in to_cities.split(',')]
    typer.echo(f"Searching for best flight from {from_city} to {', '.join(destinations)}...")

    try:
        result = asyncio.run(service.optimize(from_city=from_city, to_cities=destinations))

        typer.secho("\n✨ Best deal found! ✨", fg=typer.colors.CYAN, bold=True)
        typer.echo(f"Best City:      {typer.style(result.best_city, fg=typer.colors.GREEN)}")
        typer.echo(f"Total Price:    {result.total_price} {result.currency}")
        typer.echo(f"Distance:       {result.distance_km} km")
        typer.echo(f"Price per km:   {result.price_per_km} {result.currency}/km")

    except FlightOptimizationError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {e}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
