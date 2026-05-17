FROM python:3.12-slim

# System dependencies (psycopg2 uchun)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies — keshlash uchun avval kopiya
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Loyiha kodini kopiya
COPY . .

# Railway $PORT env beradi, default 8000
EXPOSE 8000

# Migration + server
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
