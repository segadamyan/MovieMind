# Write Dockerfile for back-end service
# Use the official Python 3.11  image as a base image
# Set the working directory in the container to /app
# Copy the current directory contents into the container at /app
# Install any needed packages specified in requirements.txt
# Expose port 5000
# Run run.py when the container launches

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV env=development

EXPOSE 5000

CMD ["python", "run.py"]