from fastapi import FastAPI

from app.api.router import router as api_router

app = FastAPI(
    title="Flight Optimization API",
    description="An API to find the best flight deals based on price per kilometer.",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok"}
