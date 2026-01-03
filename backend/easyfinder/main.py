import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load env vars (local .env OR Fly secrets)
load_dotenv()

# ==========================
# Environment Variables
# ==========================
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "easyfinder")
CORS_ORIGINS = os.getenv("CORS_ORIGINS")

if not MONGO_URL:
    raise RuntimeError("MONGO_URL is not set")

# ==========================
# App
# ==========================
app = FastAPI(
    title="EasyFinder AI",
    version="1.0.0",
)

# ==========================
# CORS
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS.split(",") if CORS_ORIGINS else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# Mongo
# ==========================
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

@app.on_event("shutdown")
async def shutdown_db():
    client.close()

# ==========================
# Routes
# ==========================
@app.get("/api/health")
async def health():
    return {"status": "ok"}
