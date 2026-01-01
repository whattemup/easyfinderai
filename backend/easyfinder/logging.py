""""Activity Logging for EasyFinder""" import json from datetime import datetime, timezone from pathlib import Path from typing import Dict, Any, List, Optional import uuid 

from .config import DATA_DIR 

class ActivityLogger: """Log activities to JSON file and memory""" 

def __init__(self, log_file: Optional[Path] = None): 
   self.log_file = log_file or (DATA_DIR / 'logs.json') 
   self._ensure_log_file() 
 
def _ensure_log_file(self): 
   \"\"\"Create log file if it doesn't exist\"\"\" 
   if not self.log_file.exists(): 
       self.log_file.write_text('[]') 
 
def _read_logs(self) -> List[Dict[str, Any]]: 
   \"\"\"Read all logs from file\"\"\" 
   try: 
       content = self.log_file.read_text() 
       return json.loads(content) if content else [] 
   except (json.JSONDecodeError, FileNotFoundError): 
       return [] 
 
def _write_logs(self, logs: List[Dict[str, Any]]): 
   \"\"\"Write logs to file\"\"\" 
   self.log_file.write_text(json.dumps(logs, indent=2)) 
 
def log(self, event_type: str, data: Dict[str, Any], status: str = 'success') -> Dict[str, Any]: 
   \"\"\" 
   Log an activity 
    
   Args: 
       event_type: Type of event (e.g., 'lead_scored', 'email_sent', 'csv_upload') 
       data: Event data 
       status: Event status ('success', 'error', 'warning') 
        
   Returns: 
       The created log entry 
   \"\"\" 
   entry = { 
       'id': str(uuid.uuid4()), 
       'timestamp': datetime.now(timezone.utc).isoformat(), 
       'event_type': event_type, 
       'status': status, 
       'data': data 
   } 
    
   logs = self._read_logs() 
   logs.insert(0, entry)  # Add to beginning (newest first) 
    
   # Keep only last 1000 entries 
   logs = logs[:1000] 
    
   self._write_logs(logs) 
   return entry 
 
def get_logs(self, limit: int = 100, event_type: Optional[str] = None) -> List[Dict[str, Any]]: 
   \"\"\" 
   Get activity logs 
    
   Args: 
       limit: Maximum number of logs to return 
       event_type: Filter by event type 
        
   Returns: 
       List of log entries 
   \"\"\" 
   logs = self._read_logs() 
    
   if event_type: 
       logs = [l for l in logs if l.get('event_type') == event_type] 
    
   return logs[:limit] 
 
def clear_logs(self): 
   \"\"\"Clear all logs\"\"\" 
   self._write_logs([]) 
 
def log_lead_scored(self, lead_name: str, score: int, priority: str): 
   \"\"\"Log lead scoring event\"\"\" 
   return self.log('lead_scored', { 
       'lead_name': lead_name, 
       'score': score, 
       'priority': priority 
   }) 
 
def log_email_sent(self, lead_name: str, email: str, mode: str = 'mock'): 
   \"\"\"Log email sent event\"\"\" 
   return self.log('email_sent', { 
       'lead_name': lead_name, 
       'email': email, 
       'mode': mode 
   }) 
 
def log_csv_upload(self, filename: str, lead_count: int): 
   \"\"\"Log CSV upload event\"\"\" 
   return self.log('csv_upload', { 
       'filename': filename, 
       'lead_count': lead_count 
   }) 
 
def log_leads_processed(self, total: int, qualified: int, emails_sent: int): 
   \"\"\"Log batch processing event\"\"\" 
   return self.log('leads_processed', { 
       'total_leads': total, 
       'qualified_leads': qualified, 
       'emails_sent': emails_sent 
   }) 
 

Global logger instance 

activity_logger = ActivityLogger()
