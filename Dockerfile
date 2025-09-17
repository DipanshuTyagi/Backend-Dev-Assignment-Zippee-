# Use lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (SQLite + curl if needed)
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Install uv and project dependencies
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv pip install --system -r pyproject.toml

# Copy application code
COPY . .

# Copy init script and make executable
COPY init_db.sh ./init_db.sh
RUN chmod +x ./init_db.sh
RUN chmod +x ./gunicorn.sh

# Expose Flask port
EXPOSE 5000

# Start container using init script
CMD ["./init_db.sh"]
