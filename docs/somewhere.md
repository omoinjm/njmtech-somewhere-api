You are a senior backend engineer.

Build a Python FastAPI backend for the “Flight Optimization” coding exercise using the architecture and principles from this repository:

https://github.com/omoinjm/njmtech-upload-blob

Important:

- Follow the same structure, layering, and architectural principles from the repo.
- Use the docs folder in that repo to guide:
  - Clean architecture
  - Service / domain separation
  - Dependency inversion
  - API layer vs application layer vs infrastructure layer

Goal:
Expose the flight optimizer script as an API.

CLI Script:
The original script must still work:

./flight-optimizer --from <city> --to <city> [<city> ...]

Backend API:
POST /api/flight/optimize

Body:
{
"from_city": "London",
"to_cities": ["Paris", "Berlin", "Rome"]
}

Response:
{
"best_city": "Paris",
"price_per_km": 0.42,
"currency": "USD",
"distance_km": 3421,
"total_price": 1437
}

Technical Requirements:

- Python 3.11
- FastAPI
- httpx for API calls
- Pydantic v2
- Haversine distance calculation
- Kiwi Tequila API integration:
  - Locations API → resolve city → airport
  - Search API → find cheapest flight
- Currency: USD

Architecture (must follow the GitHub repo):

- app/
  - api/
  - domain/
  - application/
  - infrastructure/
  - core/
- Dependency injection
- Service layer
- Repository layer
- Config via environment variables
- No business logic in controllers

Deliverables:

- Full backend project
- .env.example
- README.md with:
  - Setup instructions
  - How to run the CLI
  - How to run the API
  - Example curl request

Also:

- Implement the CLI script inside the same codebase
- The API must internally call the same service as the CLI
- One single API endpoint only

Finally:
Generate the exact command I must run to start the server and to run the CLI.
