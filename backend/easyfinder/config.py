import os
from dotenv import load_dotenv


load_dotenv()


MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "easyfinder")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "mock_key")
FROM_EMAIL = os.getenv("FROM_EMAIL", "demo@easyfinder.ai")
APP_ENV = os.getenv("APP_ENV", "local")
MOCK_EMAIL_MODE = APP_ENV != "production"
