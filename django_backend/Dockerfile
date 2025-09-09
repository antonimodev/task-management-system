FROM python:3.12-slim

WORKDIR /app

# Prevent .pyc files generation
ENV PYTHONDONTWRITEBYTECODE=1
# Direct log output (no buffering)
ENV PYTHONUNBUFFERED=1

# Install only minimal system dependencies required for the app
RUN apt-get update && apt-get install -y \
	postgresql-client \
	redis-tools

COPY requirements.txt .

# Install Python dependencies without caching to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Giving execute permissions to script entrypoint.sh
RUN chmod +x /app/scripts/entrypoint.sh