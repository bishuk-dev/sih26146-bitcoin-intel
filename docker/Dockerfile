# Offline-first build: all deps come from ./wheels, never from PyPI at build time.
# Run docker/build_offline.sh BEFORE building this image (while you still have internet).
FROM python:3.11-slim

WORKDIR /app

COPY wheels/ ./wheels/
COPY requirements.txt .
RUN pip install --no-index --find-links=./wheels -r requirements.txt

COPY src/ ./src/
COPY dashboard/ ./dashboard/
COPY data/schema/ ./data/schema/

EXPOSE 8501

# Streamlit must never call out to a CDN — see dashboard/app.py for cdn_resources='local'
CMD ["streamlit", "run", "dashboard/app.py", "--server.address=0.0.0.0"]
