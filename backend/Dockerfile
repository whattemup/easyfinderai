FROM python:3.11-slim 

  

WORKDIR /app 

  

# Install system dependencies 

RUN apt-get update && apt-get install -y --no-install-recommends \ 

    gcc \ 

    && rm -rf /var/lib/apt/lists/* 

  

# Copy requirements first for caching 

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt 

  

# Copy application code 

COPY . . 

  

# Create data directory 

RUN mkdir -p data templates 

  

# Expose port - fly.io expects internal_port to match this 

EXPOSE 8001 

  

# Important: Use PORT env variable if set, otherwise default to 8001 

# fly.io sets PORT automatically 

CMD [\"sh\", \"-c\", \"uvicorn server:app --host 0.0.0.0 --port ${PORT:-8001}\"] 
