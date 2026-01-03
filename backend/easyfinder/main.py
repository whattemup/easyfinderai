from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime

from .ingestion import parse_csv_content
from .scoring import batch_score_leads
from .outreach import batch_send_emails
from .logging import activity_logger

app = FastAPI(
    title="EasyFinder AI API",
    version="1.0.0",
    description="Enterprise Lead Management & Scoring API"
)

# CORS (safe default – tighten later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow()}

@app.post("/leads/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    content = (await file.read()).decode("utf-8")

    leads, error = parse_csv_content(content)
    if error:
        raise HTTPException(status_code=400, detail=error)

    scored = batch_score_leads(leads)

    activity_logger.log_csv_upload(file.filename, len(scored))

    return {
        "total": len(scored),
        "high_priority": sum(1 for l in scored if l["priority"] == "HIGH"),
        "leads": scored
    }

@app.post("/leads/outreach")
def send_outreach():
    logs = activity_logger.get_logs(limit=100)
    return {
        "message": "Mock outreach executed",
        "logs": logs
    }
