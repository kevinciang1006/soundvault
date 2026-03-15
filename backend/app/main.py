from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import engine, Base
import models.schemas  # noqa: F401 — must import before create_all to register ORM models
from routers import packs, samples, analyze
import database.seed as seed_module
from database.db import SessionLocal

# Create all tables (models must be imported above first)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SoundVault API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:80", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(packs.router)
app.include_router(samples.router)
app.include_router(analyze.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        seed_module.seed_database(db)
    finally:
        db.close()
