# EasyFinder AI - Enterprise Lead Management System 

Enterprise-grade AI system for intelligent lead management, scoring, and automated outreach. 

🎯 Features 

📊 Intelligent Lead Scoring: Rule-based scoring with explainable criteria 

📈 Interactive Dashboard: Real-time lead management and analytics 

📧 Automated Outreach: NDA-gated email campaigns (mock mode for testing) 

📝 Audit Trail: Complete tracking and logging for compliance 

🔒 Enterprise Security: Secure implementation with environment-based configuration 

📤 CSV Import/Export: Easy lead data management 

🚀 Quick Start 

Local Development 

Backend Setup: 

cd backend 
pip install -r requirements.txt 
# Backend runs on port 8001 
 

Frontend Setup: 

cd frontend 
yarn install 
yarn start 
# Frontend runs on port 3000 
 

🌐 fly.io Deployment 

Backend Deployment 

cd backend 
 
# Create the app 
fly launch --name easyfinder-api --no-deploy 
 
# Set secrets (MongoDB URL required) 
fly secrets set MONGO_URL=\"mongodb+srv://user:pass@cluster.mongodb.net/easyfinder\" 
fly secrets set DB_NAME=\"easyfinder\" 
fly secrets set CORS_ORIGINS=\"https://easyfinder-web.fly.dev\" 
fly secrets set APP_ENV=\"production\" 
 
# Deploy 
fly deploy 
 

Frontend Deployment 

cd frontend 
 
# Update .env with backend URL 
echo \"REACT_APP_BACKEND_URL=https://easyfinder-api.fly.dev\" > .env.production 
 
# Create and deploy 
fly launch --name easyfinder-web --no-deploy 
fly deploy 
 

Important fly.io Notes 

PORT Environment Variable: fly.io automatically sets PORT. The backend Dockerfile uses ${PORT:-8001} to handle this. 

Internal vs External Ports:  

internal_port in fly.toml must match what your app listens on 

fly.io handles external routing automatically 

MongoDB: Use MongoDB Atlas or any external MongoDB service. Set MONGO_URL as a fly secret. 

📊 Lead Scoring Logic 

Criteria, Points, Description 

Company Size, 10-40, Enterprise (40), Medium (25), Small (10) 

Budget, 15-30, >$50k (30), >$25k (15) 

Industry, 10-20, Target industries get higher scores 

Email, 10, Valid email format 

Email Threshold: Leads with score >= 70 receive automated outreach 

📧 Email Mode 

Currently running in MOCK MODE - no real emails are sent. All email actions are logged but not delivered. 

To enable real emails, integrate SendGrid and update config.py. 

🔌 API Endpoints 

Method, Endpoint, Description 

GET, /api/leads, Get all leads 

POST, /api/leads, Create a lead 

POST, /api/leads/upload, Upload CSV 

POST, /api/leads/process, Process & score leads 

GET, /api/leads/stats, Get statistics 

DELETE, /api/leads/{id}, Delete a lead 

GET, /api/logs, Get activity logs 

DELETE, /api/logs, Clear logs 

GET, /api/sample-csv, Get sample CSV 

📁 Project Structure 

EasyFinder AI/ 
├── backend/ 
│   ├── easyfinder/          # Core modules 
│   │   ├── config.py        # Configuration 
│   │   ├── ingestion.py     # CSV parsing 
│   │   ├── scoring.py       # Lead scoring 
│   │   ├── outreach.py      # Email (mock) 
│   │   └── logging.py       # Activity logs 
│   ├── templates/           # Email templates 
│   ├── data/                # Sample data 
│   ├── server.py            # FastAPI app 
│   ├── Dockerfile           # Docker config 
│   ├── fly.toml             # fly.io config 
│   └── requirements.txt 
├── frontend/ 
│   ├── src/ 
│   │   ├── App.js           # Dashboard 
│   │   └── components/      # UI components 
│   ├── Dockerfile           # Docker config 
│   ├── fly.toml             # fly.io config 
│   └── nginx.conf           # Nginx config 
└── README.md 
 

🔧 Environment Variables 

Backend (.env) 

MONGO_URL=mongodb://localhost:27017 
DB_NAME=test_database 
CORS_ORIGINS=* 
SENDGRID_API_KEY=mock_key 
FROM_EMAIL=demo@easyfinder.ai 
APP_ENV=local 
 

Frontend (.env) 

REACT_APP_BACKEND_URL=https://your-backend-url.fly.dev 
 

📄 License 

Private/Enterprise License - All Rights Reserved 

 

Built with FastAPI, React, and MongoDB 
Version: 1.0.0 "
