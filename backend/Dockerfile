FROM python:3.11-slim

WORKDIR /app

# Install system deps (optional but safe)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy backend code ONLY (this folder is the build context)
COPY . .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Expose Fly port
EXPOSE 8080

# Start FastAPI
CMD ["uvicorn", "easyfinder.main:app", "--host", "0.0.0.0", "--port", "8080"]
