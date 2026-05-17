# Backend Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy Django project
COPY . .

# Expose port
EXPOSE 8000

# Run Django
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
