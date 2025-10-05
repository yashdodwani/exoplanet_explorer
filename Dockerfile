# Use an official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .

# Expose only Streamlit port (8501) for public access
EXPOSE 8501

# Start FastAPI in the background, Streamlit in the foreground
CMD uvicorn main:app --host 0.0.0.0 --port 8000 & \
    streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0
