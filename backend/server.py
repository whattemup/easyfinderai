from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException from dotenv import load_dotenv from starlette.middleware.cors import CORSMiddleware from motor.motor_asyncio import AsyncIOMotorClient import os import logging from pathlib import Path from pydantic import BaseModel, Field, ConfigDict from typing import List, Optional, Dict, Any import uuid from datetime import datetime, timezone 

Import EasyFinder modules 

from easyfinder.scoring import calculate_lead_score, batch_score_leads from easyfinder.ingestion import parse_csv_content, generate_sample_csv from easyfinder.outreach import send_email, batch_send_emails from easyfinder.logging import activity_logger 

ROOT_DIR = Path(file).parent load_dotenv(ROOT_DIR / '.env') 

MongoDB connection 

mongo_url = os.environ['MONGO_URL'] client = AsyncIOMotorClient(mongo_url) db = client[os.environ['DB_NAME']] 

Create the main app 

app = FastAPI(title="EasyFinder AI", version="1.0.0") 

Create a router with the /api prefix 

api_router = APIRouter(prefix="/api") 

Configure logging 

logging.basicConfig( level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' ) logger = logging.getLogger(name) 

Pydantic Models 

class LeadBase(BaseModel): name: str email: str company: str company_size: str industry: str budget: str phone: Optional[str] = "" website: Optional[str] = "" 

class LeadCreate(LeadBase): pass 

class Lead(LeadBase): model_config = ConfigDict(extra="ignore") 

id: str = Field(default_factory=lambda: str(uuid.uuid4())) 
score: Optional[int] = None 
priority: Optional[str] = None 
breakdown: Optional[List[Dict[str, Any]]] = None 
qualifies_for_outreach: Optional[bool] = None 
email_sent: bool = False 
created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat()) 
 

class LogEntry(BaseModel): model_config = ConfigDict(extra="ignore") 

id: str 
timestamp: str 
event_type: str 
status: str 
data: Dict[str, Any] 
 

class ProcessResult(BaseModel): total_leads: int scored: int qualified: int emails_sent: int leads: List[Lead] 

class StatsResponse(BaseModel): total_leads: int high_priority: int medium_priority: int low_priority: int emails_sent: int average_score: float 

API Routes 

@api_router.get("/") async def root(): return {"message": "EasyFinder AI API v1.0.0", "status": "running"} 

@api_router.get("/health") async def health_check(): return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()} 

@api_router.get("/leads", response_model=List[Lead]) async def get_leads(): """Get all leads with their scores""" leads = await db.leads.find({}, {"_id": 0}).to_list(1000) return leads 

@api_router.get("/leads/stats", response_model=StatsResponse) async def get_leads_stats(): """Get lead statistics""" leads = await db.leads.find({}, {"_id": 0}).to_list(1000) 

total = len(leads) 
high = sum(1 for l in leads if l.get('priority') == 'HIGH') 
medium = sum(1 for l in leads if l.get('priority') == 'MEDIUM') 
low = sum(1 for l in leads if l.get('priority') == 'LOW') 
emails_sent = sum(1 for l in leads if l.get('email_sent')) 
avg_score = sum(l.get('score', 0) for l in leads) / total if total > 0 else 0 
 
return StatsResponse( 
   total_leads=total, 
   high_priority=high, 
   medium_priority=medium, 
   low_priority=low, 
   emails_sent=emails_sent, 
   average_score=round(avg_score, 1) 
) 
 

@api_router.post("/leads", response_model=Lead) async def create_lead(lead: LeadCreate): """Create a new lead and score it""" lead_dict = lead.model_dump() lead_dict['id'] = str(uuid.uuid4()) lead_dict['created_at'] = datetime.now(timezone.utc).isoformat() 

# Score the lead 
scoring_result = calculate_lead_score(lead_dict) 
lead_dict.update(scoring_result) 
lead_dict['email_sent'] = False 
 
# Save to database 
await db.leads.insert_one(lead_dict) 
 
# Log activity 
activity_logger.log_lead_scored(lead_dict['name'], lead_dict['score'], lead_dict['priority']) 
 
# Remove MongoDB _id before returning 
lead_dict.pop('_id', None) 
return lead_dict 
 

@api_router.post("/leads/upload") async def upload_leads(file: UploadFile = File(...)): """Upload leads from CSV file""" if not file.filename.endswith('.csv'): raise HTTPException(status_code=400, detail="File must be a CSV") 

content = await file.read() 
content_str = content.decode('utf-8') 
 
leads, error = parse_csv_content(content_str) 
if error: 
   raise HTTPException(status_code=400, detail=error) 
 
# Score and save leads 
scored_leads = batch_score_leads(leads) 
saved_count = 0 
 
for lead in scored_leads: 
   lead['id'] = str(uuid.uuid4()) 
   lead['email_sent'] = False 
   # Check if lead with same email exists 
   existing = await db.leads.find_one({'email': lead['email']}) 
   if not existing: 
       await db.leads.insert_one(lead) 
       saved_count += 1 
 
# Log activity 
activity_logger.log_csv_upload(file.filename, saved_count) 
 
return { 
   \"message\": f\"Successfully uploaded {saved_count} leads\", 
   \"total_in_file\": len(leads), 
   \"new_leads\": saved_count, 
   \"duplicates_skipped\": len(leads) - saved_count 
} 
 

@api_router.post("/leads/process", response_model=ProcessResult) async def process_leads(): """Process all leads: score and send emails to qualified leads""" leads = await db.leads.find({}, {"_id": 0}).to_list(1000) 

if not leads: 
   return ProcessResult( 
       total_leads=0, 
       scored=0, 
       qualified=0, 
       emails_sent=0, 
       leads=[] 
   ) 
 
# Re-score all leads 
scored_leads = batch_score_leads(leads) 
qualified_count = 0 
emails_sent_count = 0 
 
for lead in scored_leads: 
   # Update lead in database 
   update_data = { 
       'score': lead['score'], 
       'priority': lead['priority'], 
       'breakdown': lead['breakdown'], 
       'qualifies_for_outreach': lead['qualifies_for_outreach'] 
   } 
    
   # Send email if qualified and not already sent 
   if lead['qualifies_for_outreach']: 
       qualified_count += 1 
       existing_lead = await db.leads.find_one({'email': lead['email']}, {\"_id\": 0}) 
       if existing_lead and not existing_lead.get('email_sent'): 
           email_result = send_email(lead['email'], lead) 
           if email_result.get('success'): 
               update_data['email_sent'] = True 
               emails_sent_count += 1 
               activity_logger.log_email_sent(lead['name'], lead['email'], 'mock') 
    
   await db.leads.update_one( 
       {'email': lead['email']}, 
       {'$set': update_data} 
   ) 
    
   # Log scoring 
   activity_logger.log_lead_scored(lead['name'], lead['score'], lead['priority']) 
 
# Log processing summary 
activity_logger.log_leads_processed(len(scored_leads), qualified_count, emails_sent_count) 
 
# Fetch updated leads 
updated_leads = await db.leads.find({}, {\"_id\": 0}).to_list(1000) 
 
return ProcessResult( 
   total_leads=len(scored_leads), 
   scored=len(scored_leads), 
   qualified=qualified_count, 
   emails_sent=emails_sent_count, 
   leads=updated_leads 
) 
 

@api_router.delete("/leads/{lead_id}") async def delete_lead(lead_id: str): """Delete a lead by ID""" result = await db.leads.delete_one({'id': lead_id}) if result.deleted_count == 0: raise HTTPException(status_code=404, detail="Lead not found") return {"message": "Lead deleted successfully"} 

@api_router.delete("/leads") async def delete_all_leads(): """Delete all leads""" result = await db.leads.delete_many({}) return {"message": f"Deleted {result.deleted_count} leads"} 

@api_router.get("/logs", response_model=List[LogEntry]) async def get_logs(limit: int = 100, event_type: Optional[str] = None): """Get activity logs""" logs = activity_logger.get_logs(limit=limit, event_type=event_type) return logs 

@api_router.delete("/logs") async def clear_logs(): """Clear all activity logs""" activity_logger.clear_logs() return {"message": "Logs cleared successfully"} 

@api_router.get("/sample-csv") async def get_sample_csv(): """Get sample CSV content""" return {"csv_content": generate_sample_csv()} 

Include the router in the main app 

app.include_router(api_router) 

CORS middleware 

app.add_middleware( CORSMiddleware, allow_credentials=True, allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','), allow_methods=["*"], allow_headers=["*"], ) 

@app.on_event("shutdown") async def shutdown_db_client(): client.close()
