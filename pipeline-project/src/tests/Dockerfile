FROM python:3.9.5-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install \
    google-cloud-storage \
    google-cloud-bigquery \
    psycopg2-binary \
    cloud-sql-python-connector \
    sqlalchemy \
    pg8000

# Copy test script
COPY test_connections.py .

CMD ["python", "test_connections.py"]