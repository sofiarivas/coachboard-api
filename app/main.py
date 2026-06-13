import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import Coach, Board, Trainee, Subscription, Workout
from app.routes import auth, coaches, boards, subscriptions, workouts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(application: FastAPI):
    """Handle application startup and shutdown lifecycle."""
    try:
        async with engine.begin() as conn:
            logger.info("Attempting to create database tables...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error during database initialization in lifespan: {e}")
        raise
    yield
    # Shutdown: cleanup happens automatically

app = FastAPI(title="Coachboard API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(coaches.router)
app.include_router(boards.router)
app.include_router(subscriptions.router)
app.include_router(workouts.router)


@app.get("/health")
async def health():
    return {"status": "ok"}