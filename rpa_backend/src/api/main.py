from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import auth, bots, schedules, executions, workflows
from src.core.config import get_settings
from src.db.session import Base, engine

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Ensure tables are created at startup (simple migration strategy for MVP)
    Base.metadata.create_all(bind=engine)
    yield


openapi_tags = [
    {"name": "Health", "description": "Service health and readiness"},
    {"name": "Auth", "description": "Authentication endpoints"},
    {"name": "Workflows", "description": "Manage workflows"},
    {"name": "Bots", "description": "Manage bots"},
    {"name": "Schedules", "description": "Manage workflow schedules"},
    {"name": "Executions", "description": "Track workflow executions"},
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.API_VERSION,
    openapi_tags=openapi_tags,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """Health check endpoint that returns a simple status message."""
    return {"message": "Healthy"}


# Register routers
app.include_router(auth.router)
app.include_router(workflows.router)
app.include_router(bots.router)
app.include_router(schedules.router)
app.include_router(executions.router)
