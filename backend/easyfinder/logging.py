from datetime import datetime


def log_event(db, event):
event["timestamp"] = datetime.utcnow().isoformat()
return db.logs.insert_one(event)
