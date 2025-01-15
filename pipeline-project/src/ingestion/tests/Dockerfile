FROM python:3.9.5-slim

WORKDIR /app

# Install Python packages
RUN pip install google-cloud-storage \
    google-cloud-bigquery \
    psycopg2-binary

# Copy test script
COPY test_connections.py .

CMD ["python", "test_connections.py"]