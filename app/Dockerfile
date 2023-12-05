# Build Stage
FROM python:3.9-slim AS build

WORKDIR /app

COPY requirements.txt .
# Create a virtual environment and install dependencies
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Install Gunicorn in the virtual environment
RUN /venv/bin/pip install gunicorn

COPY . .

# Deploy Stage
FROM python:3.9-slim AS deploy

# Copy virtual env from the build stage
COPY --from=build /venv /venv

# Copy Python app from the build stage
COPY --from=build /app /app

# Install Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Nginx configuration
COPY weather.conf /etc/nginx/conf.d/default.conf

# Start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]
