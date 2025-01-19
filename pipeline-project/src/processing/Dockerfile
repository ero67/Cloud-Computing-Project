FROM python:3.9.5-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PREFECT_API_URL="http://prefect-server:4200/api"

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Create directory for temporary file storage
RUN mkdir -p /Archive

# Copy source code
COPY flows/deploy.py /deploy.py
COPY flows/taxi_data_flow.py /taxi_data_flow.py

# Command to run the flow
CMD ["python", "/deploy.py"]