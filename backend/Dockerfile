FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . .

# IMPORTANT: backend/app is the Python package
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
