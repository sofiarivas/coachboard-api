import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
# Import all models so their tables are registered on Base.metadata before
# create_all is called during startup.
import app.models  # noqa: F401
from app.routes import auth, coaches, boards, subscriptions, workouts

logger = logging.getLogger(__name__)

DB_INIT_TIMEOUT = 10  # seconds


async def init_db() -> None:
    """Create all database tables if they do not already exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Handle application startup and shutdown lifecycle."""
    try:
        await asyncio.wait_for(init_db(), timeout=DB_INIT_TIMEOUT)
        logger.info("Database initialised successfully.")
    except asyncio.TimeoutError:
        logger.error(
            "Database initialisation timed out after %s seconds. "
            "The app will start without pre-created tables; they will be "
            "created on the first successful database connection.",
            DB_INIT_TIMEOUT,
        )
    except Exception as exc:
        logger.error(
            "Database initialisation failed: %s. "
            "The app will start without pre-created tables.",
            exc,
            exc_info=True,
        )
    yield


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
