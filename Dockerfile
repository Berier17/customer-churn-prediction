# Start from a lightweight official Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file *first*
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy all your project files into the container's /app/ folder
COPY . .

# Expose port 9696 (the port your Flask app runs on)
EXPOSE 9696

# The command to run when the container starts
# gunicorn is a "production" server for Flask
CMD ["gunicorn", "--bind", "0.0.0.0:9696", "predict:app"]