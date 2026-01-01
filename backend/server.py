
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from easyfinder.config import MONGO_URL, DB_NAME
from easyfinder.ingestion import ingest_csv
from easyfinder.scoring import score_lead
from easyfinder.outreach import send_email
from easyfinder.logging import log_event


app = FastAPI()


app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_methods=["*"],
allow_headers=["*"],
)


client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


@app.get("/api/leads")
async def get_leads():
return await db.leads.find().to_list(1000)


@app.post("/api/leads/upload")
async def upload(file: UploadFile = File(...)):
leads = ingest_csv(file.file)
await db.leads.insert_many(leads)
return {"uploaded": len(leads)}


@app.post("/api/leads/process")
async def process():
leads = await db.leads.find().to_list(1000)
results = []
for lead in leads:
score = score_lead(lead)
await db.leads.update_one({"_id": lead["_id"]}, {"$set": {"score": score}})
if score >= 70:
send_email(lead)
results.append({"email": lead.get("email"), "score": score})
return results


@app.get("/api/logs")
async def logs():
return await db.logs.find().to_list(1000)
