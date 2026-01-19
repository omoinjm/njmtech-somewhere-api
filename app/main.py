from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router as api_router

app = FastAPI(
    title="Flight Optimization API",
    description="An API to find the best flight deals based on price per kilometer.",
    version="1.0.0",
)

# CORS configuration
origins = [
    "https://somewhere.vercel.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok"}
