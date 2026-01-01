from .config import MOCK_EMAIL_MODE


def send_email(lead):
if MOCK_EMAIL_MODE:
return {"status": "mocked", "email": lead["email"]}
return {"status": "sent", "email": lead["email"]}
