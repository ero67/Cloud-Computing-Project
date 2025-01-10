FROM python:3.9-slim

WORKDIR /app

# Install required packages
RUN pip install google-cloud-storage \
    google-cloud-bigquery

# Copy test script
COPY test_gcp.py .

CMD ["python", "test_gcp.py"]