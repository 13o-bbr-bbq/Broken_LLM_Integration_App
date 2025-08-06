# dummy_web/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY static ./static

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
