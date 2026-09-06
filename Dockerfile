FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY backend/ backend/
COPY frontend/ frontend/
COPY server.py .

EXPOSE 8000

ENV PORT=8000
ENV PYTHONUNBUFFERED=1

CMD ["python", "server.py"]
