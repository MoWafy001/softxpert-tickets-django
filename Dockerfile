FROM python:3.13-slim

# Set environment variables to prevent Python from writing .pyc files and to ensure output is sent straight to terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# The usual create an app dir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \ 
    postgresql postgresql-contrib \
    && rm -rf /var/lib/apt/lists/* 

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

RUN python manage.py collectstatic --noinput

# Will use port 8000 for the application
EXPOSE 8000

# Running and binding gunicorn to the port
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "support_system.wsgi:application"]