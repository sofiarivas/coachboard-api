from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
# Import all models so their tables are registered on Base.metadata before
# create_all is called during startup.
import app.models  # noqa: F401
from app.routes import auth, coaches, boards, subscriptions, workouts


async def init_db() -> None:
    """Create all database tables if they do not already exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Handle application startup and shutdown lifecycle."""
    await init_db()
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
