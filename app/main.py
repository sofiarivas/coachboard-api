from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth, coaches, boards, subscriptions, workouts

app = FastAPI(title="Coachboard API", version="1.0.0")

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

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
