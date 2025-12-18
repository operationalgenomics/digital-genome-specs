# Use an official Python base image
FROM python:3.10-slim

# Image Metadata
LABEL maintainer="Carlos Eduardo Favini <favini@microgenesys.com.br>"
LABEL description="Operational Genomics Simulation Environment"
LABEL version="2.0.0"

# Set the working directory in the container
WORKDIR /app

# Environment variables to prevent .pyc files and stdout buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Add src to PYTHONPATH to ensure imports work correctly
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Install necessary system dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project structure
COPY . .

# Create a non-root user for security purposes
RUN useradd -m researcher
USER researcher

# Default command: execute the demo script
CMD ["python", "examples/demo.py"]