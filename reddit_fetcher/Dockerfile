# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY main.py .

# Set environment variables (if needed)
# ENV GOOGLE_CLOUD_PROJECT=ai-radar-465910

# Expose the Flask port
EXPOSE 8080

# Start the app
CMD ["python", "main.py"]