# Backend Dockerfile example

# Use a Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the backend application code to the container
COPY . /app

# Install dependencies (assuming you have requirements.txt)
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Run the backend application
CMD ["python", "app/app.py"]
