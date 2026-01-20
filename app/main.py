from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.router import router as api_router

app = FastAPI(
    title="Flight Optimization API",
    description="An API to find the best flight deals based on price per kilometer.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

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

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok"}
