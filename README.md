# Flight Optimization API

This project provides a backend solution for a "Flight Optimization" coding exercise. It exposes a single API endpoint to find the best flight deal from a given city to a list of potential destinations, based on the lowest price per kilometer. It also includes a command-line interface (CLI) to perform the same function.

The architecture follows Clean Architecture principles, separating concerns into distinct layers: API, Application, Domain, and Infrastructure.

## Technical Requirements

- Python 3.11+
- FastAPI
- Pydantic v2
- httpx
- Haversine for distance calculations
- [Kiwi Tequila API](https://tequila.kiwi.com/portal/docs) for flight data

---

## Setup Instructions

1.  **Clone the repository (or set up the project files):**

    ```bash
    # This step is assumed to be done
    # git clone <repository_url>
    # cd <repository_directory>
    ```

2.  **Create a virtual environment:**

    It's highly recommended to use a virtual environment to manage dependencies.

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    Install all the required Python packages from `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    The application requires an API key for the Kiwi Tequila API.

    a. Copy the example `.env.example` file to a new `.env` file:

    ```bash
    cp .env.example .env
    ```

    b. Open the `.env` file and replace "YOUR_API_KEY_HERE" with your actual Kiwi Tequila API key.

    ```ini
    # .env
    KIWI_API_KEY="sk-xxxxxxxx...xxxxxxxx"
    ```

---

## How to Run the API Server

Once the setup is complete, you can run the FastAPI server using `uvicorn`.

```bash
uvicorn app.main:app --reload
```

The server will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

### Example API Request

You can use `curl` or any API client to send a `POST` request to the `/api/flight/optimize` endpoint.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/flight/optimize' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d
{
  "from_city": "London",
  "to_cities": [
    "Paris",
    "Berlin",
    "Rome"
  ]
}
```

**Example Response:**

```json
{
  "best_city": "Paris",
  "price_per_km": 0.42,
  "currency": "USD",
  "distance_km": 342.1234,
  "total_price": 143.7
}
```

---

## How to Run the CLI

The project also includes a command-line interface to perform the same optimization task directly from your terminal.

The command uses the format `python cli.py --from <city> --to "<city1>, <city2> ..."`.

**Example CLI Command:**

```bash
python cli.py --from "New York" --to "London" --to "Tokyo, Sydney"
```

**Example CLI Output:**

```
Searching for best flight from New York to London, Tokyo, Sydney...

✨ Best deal found! ✨
Best City:      London
Total Price:    350 USD
Distance:       5570.23 km
Price per km:   0.0628 USD/km
```
