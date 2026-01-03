print("🚀 EasyFinder API starting...")

import os
import uuid
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, ConfigDict

# EasyFinder modules
from easyfinder.scoring import calculate_lead_score, batch_score_leads
from easyfinder.ingestion import parse_csv_content, generate_sample_csv
from easyfinder.outreach import send_email
from easyfinder.logging import activity_logger


# -------------------------------------------------
# ENV & DATABASE
# -------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "easyfinder")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


# -------------------------------------------------
# APP SETUP
# -------------------------------------------------

app = FastAPI(
    title="EasyFinder AI",
    version="1.0.0",
    description="Enterprise Lead Scoring & Outreach API"
)

api_router = APIRouter(prefix="/api")


# -------------------------------------------------
# LOGGING
# -------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("easyfinder")


# -------------------------------------------------
# MODELS
# -------------------------------------------------

class LeadBase(BaseModel):
    name: str
    email: str
    company: str
    company_size: str
    industry: str
    budget: str
    phone: Optional[str] = ""
    website: Optional[str] = ""


class LeadCreate(LeadBase):
    pass


class Lead(LeadBase):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    score: Optional[int] = None
    priority: Optional[str] = None
    breakdown: Optional[List[Dict[str, Any]]] = None
    qualifies_for_outreach: Optional[bool] = None
    email_sent: bool = False
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class LogEntry(BaseModel):
    id: str
    timestamp: str
    event_type: str
    status: str
    data: Dict[str, Any]


class ProcessResult(BaseModel):
    total_leads: int
    scored: int
    qualified: int
    emails_sent: int
    leads: List[Lead]


class StatsResponse(BaseModel):
    total_leads: int
    high_priority: int
    medium_priority: int
    low_priority: int
    emails_sent: int
    average_score: float


# -------------------------------------------------
# ROUTES
# -------------------------------------------------

@api_router.get("/")
async def root():
    return {"status": "running", "service": "EasyFinder AI"}


@api_router.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


@api_router.get("/leads", response_model=List[Lead])
async def get_leads():
    return await db.leads.find({}, {"_id": 0}).to_list(1000)


@api_router.post("/leads", response_model=Lead)
async def create_lead(lead: LeadCreate):
    data = lead.model_dump()
    data["id"] = str(uuid.uuid4())
    data["created_at"] = datetime.now(timezone.utc).isoformat()

    scoring = calculate_lead_score(data)
    data.update(scoring)
    data["email_sent"] = False

    await db.leads.insert_one(data)

    activity_logger.log_lead_scored(
        data["name"], data["score"], data["priority"]
    )

    return data


@api_router.post("/leads/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV files only")

    content = (await file.read()).decode("utf-8")
    leads, error = parse_csv_content(content)

    if error:
        raise HTTPException(status_code=400, detail=error)

    scored = batch_score_leads(leads)
    saved = 0

    for lead in scored:
        if not await db.leads.find_one({"email": lead["email"]}):
            lead["id"] = str(uuid.uuid4())
            lead["email_sent"] = False
            await db.leads.insert_one(lead)
            saved += 1

    activity_logger.log_csv_upload(file.filename, saved)

    return {
        "total": len(leads),
        "saved": saved,
        "duplicates": len(leads) - saved
    }


@api_router.post("/leads/process", response_model=ProcessResult)
async def process_leads():
    leads = await db.leads.find({}, {"_id": 0}).to_list(1000)

    qualified = 0
    emails_sent = 0

    for lead in batch_score_leads(leads):
        update = {
            "score": lead["score"],
            "priority": lead["priority"],
            "breakdown": lead["breakdown"],
            "qualifies_for_outreach": lead["qualifies_for_outreach"]
        }

        if lead["qualifies_for_outreach"] and not lead.get("email_sent"):
            qualified += 1
            result = send_email(lead["email"], lead)
            if result.get("success"):
                update["email_sent"] = True
                emails_sent += 1
                activity_logger.log_email_sent(
                    lead["name"], lead["email"], "mock"
                )

        await db.leads.update_one(
            {"email": lead["email"]},
            {"$set": update}
        )

    updated = await db.leads.find({}, {"_id": 0}).to_list(1000)

    activity_logger.log_leads_processed(
        len(updated), qualified, emails_sent
    )

    return ProcessResult(
        total_leads=len(updated),
        scored=len(updated),
        qualified=qualified,
        emails_sent=emails_sent,
        leads=updated
    )


@api_router.get("/sample-csv")
async def sample_csv():
    return {"csv": generate_sample_csv()}


# -------------------------------------------------
# FINALIZE APP
# -------------------------------------------------

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown():
    client.close()
