import asyncio
import typer
from typing_extensions import Annotated
from typing import List

import httpx

from app.application.services import FlightOptimizationService, FlightOptimizationError
from app.core.config import settings
from app.infrastructure.repositories.kiwi_flight_repository import KiwiFlightRepository

# Create a Typer app
cli = typer.Typer()

def get_service() -> FlightOptimizationService:
    """Manually construct the service for the CLI."""
    client = httpx.AsyncClient()
    repo = KiwiFlightRepository(settings=settings, client=client)
    return FlightOptimizationService(flight_repository=repo)


@cli.command()
def optimize(
    from_city: Annotated[str, typer.Option("--from", help="The starting city.")],
    to_cities: Annotated[List[str], typer.Option("--to", help="A destination city. Can be used multiple times.")],
):
    """
    Finds the best flight deal from a starting city to a list of destinations.
    """
    service = get_service()
    typer.echo(f"Searching for best flight from {from_city} to {', '.join(to_cities)}...")

    try:
        result = asyncio.run(service.optimize(from_city=from_city, to_cities=to_cities))

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


if __name__ == "__main__":
    cli()
