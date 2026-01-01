FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN python -m pip install "pymongo[srv]==3.12"
COPY . .
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
