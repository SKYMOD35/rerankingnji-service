# Use an official Python runtime as the base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the working directory
COPY . .

# Expose the application port (Gunicorn listens on this port)
EXPOSE 5000

# Copy the Gunicorn configuration file into the container
COPY gunicorn.conf.py /app/gunicorn.conf.py

# Add resource limits and preload the app to optimize worker memory usage
CMD ["gunicorn", "--config", "gunicorn.conf.py", "--preload", "app:app"]
