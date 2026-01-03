FROM python:3.11-slim

WORKDIR /app/backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "easyfinder.main:app", "--host", "0.0.0.0", "--port", "8080"]
